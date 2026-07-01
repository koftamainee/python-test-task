import asyncio
import csv
import json
import os
import uuid
from ast import literal_eval
from datetime import datetime

from elasticsearch import AsyncElasticsearch
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def parse_rubrics(raw: str) -> list[str]:
    parsed = literal_eval(raw)
    return parsed if isinstance(parsed, list) else []


def read_csv(path: str) -> list[dict]:
    documents = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            documents.append(
                {
                    "id": uuid.uuid4(),
                    "text": row["text"],
                    "rubrics": parse_rubrics(row["rubrics"]),
                    "created_date": datetime.strptime(
                        row["created_date"], "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )
    return documents


async def load_to_postgres(docs: list[dict], dsn: str) -> bool:
    engine = create_async_engine(dsn)
    session_factory = async_sessionmaker(engine)
    async with session_factory() as session:
        result = await session.execute(text("SELECT id FROM documents LIMIT 1"))
        if result.scalar() is not None:
            print("Postgres already has data, skipping")
            await engine.dispose()
            return False

        for d in docs:
            rubrics_json = json.dumps(d["rubrics"], ensure_ascii=False)
            await session.execute(
                text(
                    "INSERT INTO documents (id, text, rubrics, created_date) "
                    "VALUES (:id, :text, CAST(:rubrics AS JSONB), :created_date)"
                ),
                {
                    "id": d["id"],
                    "text": d["text"],
                    "rubrics": rubrics_json,
                    "created_date": d["created_date"],
                },
            )
        await session.commit()
    print(f"Inserted {len(docs)} documents into Postgres")
    await engine.dispose()
    return True


async def load_to_es(
    docs: list[dict], es_url: str, es_user: str, es_pass: str, index: str
):
    es = AsyncElasticsearch(es_url, basic_auth=(es_user, es_pass))

    exists = await es.indices.exists(index=index)
    if not exists:
        await es.indices.create(
            index=index,
            mappings={
                "properties": {
                    "id": {"type": "keyword"},
                    "text": {"type": "text"},
                }
            },
        )

    count = await es.count(index=index)
    if count["count"] > 0:
        print("ES already has data, skipping")
        await es.close()
        return

    actions = []
    for d in docs:
        actions.append({"index": {"_index": index, "_id": str(d["id"])}})
        actions.append({"id": str(d["id"]), "text": d["text"]})

    batch_size = 500
    inserted = 0
    for i in range(0, len(actions), batch_size * 2):
        batch = actions[i : i + batch_size * 2]
        await es.bulk(operations=batch, refresh=True)
        inserted += len(batch) // 2
        print(f"Indexed {inserted}/{len(docs)}")

    total = await es.count(index=index)
    print(f"Total documents in ES: {total['count']}")
    await es.close()


async def main():
    csv_path = os.environ["CSV_PATH"]
    dsn = os.environ["DATABASE_URL"]
    es_url = os.environ["ELASTICSEARCH_URL"]
    es_user = os.environ.get("ELASTICSEARCH_USER", "elastic")
    es_pass = os.environ["ELASTICSEARCH_PASSWORD"]
    es_index = os.environ.get("ELASTICSEARCH_INDEX", "documents")

    docs = read_csv(csv_path)
    print(f"Loaded {len(docs)} documents from CSV")

    await load_to_postgres(docs, dsn)
    await load_to_es(docs, es_url, es_user, es_pass, es_index)

    print("Done")


asyncio.run(main())
