---
name: market-stats
description: Provides market statistics for real estate listings, including average prices, trends, and other relevant data.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Market Stats
Provides information about market trends in a given city, including average closing price, amount of houses sold, and average days on market by date.

It also allows you understand the general market summary for top cities in the US, including average price, average days on market, average price per sqft, and % of how close closing day was to the listing day.

This skill can be used to get a better understanding of the real estate market in a specific area, and can help inform decisions about buying or selling property.

## When to Use

Use this skill when you want to get a better understanding of the real estate market in a specific area, or when you want to compare market trends across different cities to help answer the user's questions about real estate market trends, like if its a good time to buy or sell in a particular city.

## How to run

This skill has two main functions: `price_trend` and `general_market_summary`.

### City Summary
The `price_trend` function provides data a dataframe that shows the general trend of the real estate market in a given city, including average closing price, amount of houses sold, and average days on market by date over the last N months.

To use it, run this command:
```bash
python3 scripts/cli.py "price_trend" <city_name> <month>
```

Note: The `month` parameter is optional and can be used to specify the number of months to look back for the trend data. If not provided, it will default to 24 months.
### General Market Summary

The `general_market_summary` function provides a summary of the real estate market for top cities in the US, including average price, average days on market, average price per sqft, and % of how close closing day was to the listing day.

To use it, run this command:
```bash
python3 scripts/cli.py "general_market_summary" <limit>
```

Note: The `limit` parameter is optional and can be used to limit the number of cities returned in the summary. If not provided, it will return the top 25 cities by default.