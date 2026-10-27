import pandas as pd
import numpy as np
from sqlalchemy import create_engine

import os

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST", "localhost")


engine = engine = create_engine(
 f"mysql+mysqlconnector://{user}:{password}@{host}/idx_exchange"
)

def get_price_trend(city:str, month: int = 24):
    query = """
        SELECT
        DATE_FORMAT(CloseDate, "%Y-%m") AS month,
        COUNT(*) AS sales,
        ROUND(AVG(ClosePrice), 0) AS avg_price,
        ROUND(AVG(DaysOnMarket), 1) AS avg_dom
        FROM california_sold
        WHERE City = %s
        AND PropertyType = "Residential"
        AND CloseDate >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
        GROUP BY DATE_FORMAT(CloseDate, "%Y-%m")
        ORDER BY month
        """
    df = pd.read_sql(query, engine, params=[city, month])
    df["price_change_pct"] = df["avg_price"].pct_change() * 100
    return df

def general_market_summary(limit: int = 25):
    """Return general summary of the market for the last 12 months, by city."""

    query = """
        SELECT
        City,
        COUNT(*) AS sold_count,
        ROUND(AVG(ClosePrice), 0) AS avg_close_price,
        ROUND(AVG(ClosePrice / NULLIF(LivingArea,0)),0) AS avg_price_per_sqft,
        ROUND(AVG(DaysOnMarket), 1) AS avg_dom,
        ROUND(AVG(ClosePrice / NULLIF(ListPrice,0)) * 100, 1) AS list_to_close_pct
        FROM california_sold
        WHERE PropertyType = 'Residential'
        AND CloseDate >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        AND LivingArea > 0
        GROUP BY City
        ORDER BY sold_count DESC
        LIMIT %s;
    """
    df = pd.read_sql(query, engine, params=[limit])
    return df