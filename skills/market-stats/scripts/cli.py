import sys
from trend_analysis import get_price_trend, general_market_summary


function = sys.argv[1]


if function == "price_trend":
    city = sys.argv[2]
    months = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    df = get_price_trend(city, months)
    print(df.to_json(orient="records"))
elif function == "general_market_summary":
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    df = general_market_summary(limit)
    print(df.to_json(orient="records"))