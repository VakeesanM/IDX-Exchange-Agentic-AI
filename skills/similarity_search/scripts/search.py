from openai import AsyncOpenAI
import numpy as np
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import asyncio

load_dotenv()

client = AsyncOpenAI()
MAX_CONCURRENCY = 10
_sem = asyncio.Semaphore(MAX_CONCURRENCY)

async def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    text = text.replace("\n", " ").strip()[:8000]
    async with _sem:
        response = await client.embeddings.create(model=model, input=text)
    return response.data[0].embedding


async def build_listing_embedding(row: dict) -> list[float]:
    text = f"""
    {row["type"]} in {row["L_City"]}, CA.
    {row["beds"]} beds, {row["baths"]} baths.
    {row["sqft"]} sq ft. Built {row["YearBuilt"]}.
    Price: ${row["price"]:,}.
    {row.get("L_Remarks", "")}
    """.strip()
    return await get_embedding(text)


def build_all_listing_embeddings(listings: list[dict]) -> list[tuple[str, list[float]]]:

    async def _run() -> list[list[float]]:
        sem = asyncio.Semaphore(MAX_CONCURRENCY)  # created inside the running loop
        return await asyncio.gather(
            *(build_listing_embedding(row, sem) for row in listings)
        )

    embeddings = asyncio.run(_run())
    return [(row["L_ID"], emb) for row, emb in zip(listings, embeddings)]




def find_similar_listings(
 query: str,
 listing_embeddings: list[tuple[str, list[float]]],
 top_k: int = 5
) -> list[str]:
    """Return top_k listing IDs most similar to the query."""
    query_vec = np.array(get_embedding(query)).reshape(1, -1)
    scores = []
    for listing_id, emb in listing_embeddings:
        sim = cosine_similarity(query_vec, np.array(emb).reshape(1, -1))[0][0]
        scores.append((listing_id, float(sim)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [lid for lid, _ in scores[:top_k]]