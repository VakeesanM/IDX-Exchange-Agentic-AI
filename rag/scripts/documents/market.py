import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DATABASE")


print(f"Connecting to MySQL database '{database}' on host '{host}' with user '{user}'")
engine = create_engine(
    f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
)


sql = """SELECT
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
LIMIT 50;
"""

df = pd.read_sql(sql, engine)

df.to_csv('market_summary   .txt', sep='\t', index=False)