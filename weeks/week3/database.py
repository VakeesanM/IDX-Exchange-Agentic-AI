import mysql.connector
import os 
from dotenv import load_dotenv
import asyncio


def active_list_search(parsed_text, limit: int = 10, offset: int = 0):

    sql = """SELECT
            L_ListingID, L_DisplayId, L_Address, L_City, L_Zip,
            L_SystemPrice AS price, L_Keyword2 AS beds, LM_Dec_3 AS baths,
            LM_Int2_3 AS sqft, L_Type_ AS type, L_Status AS status,
            LMD_MP_Latitude AS lat, LMD_MP_Longitude AS lng,
            YearBuilt, AssociationFee, DaysOnMarket,
            PoolPrivateYN, ViewYN, FireplaceYN, PhotoCount,
            LA1_UserFirstName, LA1_UserLastName, LO1_OrganizationName
            FROM rets_property WHERE L_Status = "Active"
            """

    for key in parsed_text:
        if parsed_text[key] is not None:
            sql += f" AND {key} = '{parsed_text[key]}'"

    sql += f"ORDER BY L_SystemPrice ASC LIMIT {limit} OFFSET {offset};"

    return sql





def run_sql(sql_query):
    load_dotenv()

    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    database = os.getenv("MYSQL_DATABASE")

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    print("Connected to the database successfully!")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM california_sold LIMIT 1;")
    print(cursor)