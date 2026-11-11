from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sqlalchemy import text, create_engine
from dotenv import load_dotenv

import os
load_dotenv()

USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
IP = os.getenv("MYSQL_IP") 
DATABASE = os.getenv("MYSQL_DATABASE")
engine = create_engine(f'mysql+mysqlconnector://{USER}:{PASSWORD}@{IP}/{DATABASE}')

def calcaute_all_sim(targets, candiates, target_embs, candiates_emb):
    all_sim = {}
    for target, candiate, target_emb, candiate_emb in zip(targets, candiates, target_embs, candiates_emb):
        all_sim[target] = (calculate_similarity_score(target, candiate, target_emb, candiate_emb))

    return sorted(all_sim, key=lambda i: all_sim[i])


def calculate_similarity_score(target: dict, candidate: dict, target_emb: list[float], candidate_emb: list[float]) -> float:
    score = 0.0

    price_diff = abs(target["L_SystemPrice"] - candidate["L_SystemPrice"])
    if price_diff < 50_000: score += 20
    elif price_diff < 150_000: score += 12
    elif price_diff < 300_000: score += 5
    if target["L_Keyword2"] == candidate["L_Keyword2"]: score += 15
    if target["L_City"] == candidate["L_City"]: score += 15
    sqft_diff = abs(target["LM_Int2_3"] - candidate["LM_Int2_3"])
    if sqft_diff < 300: score += 10
    elif sqft_diff < 700: score += 5
    
    sem_sim = cosine_similarity(
    np.array(target_emb).reshape(1,-1),
    np.array(candidate_emb).reshape(1,-1)
    )[0][0]
    score += sem_sim * 40
    return round(score, 2)


def validate_with_comps(city: str, sqft: int, price: int) -> dict:
    sql = text("""
        SELECT
            AVG(ClosePrice / LivingArea) AS avg_ppsf,
            COUNT(*) AS comp_count
        FROM california_sold
        WHERE City = :city
          AND PropertyType = 'Residential'
          AND LivingArea BETWEEN :lower_bound AND :upper_bound
          AND LivingArea > 0
          AND ClosePrice > 0
          AND CloseDate >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
    """)

    with engine.connect() as conn:
        row = conn.execute(sql, {
            "city": city,
            "lower_bound": int(sqft * 0.8),
            "upper_bound": int(sqft * 1.2),
        }).mappings().first()

    comp_count = row["comp_count"] or 0
    avg_ppsf = float(row["avg_ppsf"]) if row["avg_ppsf"] is not None else None

    if not comp_count or avg_ppsf is None:
        return {
            "comp_price": None,
            "list_price": price,
            "comp_count": 0,
            "delta_pct": None,
        }

    comp_price = avg_ppsf * sqft
    return {
        "comp_price": round(comp_price),
        "list_price": price,
        "comp_count": comp_count,
        "delta_pct": round((price - comp_price) / comp_price * 100, 1),
    }

def validate_all(targets, candiates, target_embs, candiates_emb, k=3):

    sims = calcaute_all_sim(targets, candiates, target_embs, candiates_emb)
    valid = {}
    for target in sims.keys():
        city = target['L_City']
        sqft = target['LM_Int2_3']
        validiation = validate_with_comps(city, sqft)
        valid[target] = validiation['comp_price']

    recoms = []
    i = 0
    for target in valid.keys():
        if i == k:
            break
        if valid[target]:
            recoms.append(target)
            i += 1

    return recoms
