from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

client = OpenAI()

def get_embedding(text: str, model="text-embedding-3-small") -> list[float]:
    text = text.replace("\n", " ").strip()[:8000]
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding

def build_listing_embedding(row: dict) -> list[float]:
    text = f"""
    {row["L_Type_"]} in {row["L_City"]}, CA.
    {row["L_Keyword2"]} beds, {row["LM_Dec_3"]} baths.
    {row["LM_Int2_3"]} sq ft. Built {row["YearBuilt"]}.
    Price: ${row["L_SystemPrice"]:,}.
    {row.get("L_Remarks", "")}
    """.strip()
    return get_embedding(text)

def build_all_listing_embeddings(listings: list[dict]) -> list[tuple[str, list[float]]]:
    result = []
    for row in listings:
        embedding = build_listing_embedding(row)
        result.append((row["L_ID"], embedding))
    return result

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