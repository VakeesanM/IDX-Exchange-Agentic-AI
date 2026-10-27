---
name: property-parser
description: Parse a natural-language real estate search (e.g. "3 bed condo in Fresno under 500k with pool") into structured filters (city, max price, beds, baths, sqft, property type, pool, view) as JSON.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
---

# Property Query 

Turns a free-text property search into structured JSON filters by running the bundled using the `parsePropertyQuery` function.

## When to use

Use this skill when the user describes a home or property search in plain English and you need structured search criteria, for use in searching a database, embedding, or passing to another skill. The parser is regex-based and only recognizes simple phrasing, so it may not understand complex queries.

Examples of inputs:
- "3 bedroom condo in Fresno under 500k"
- "single family home in Clovis with pool and view under $1.2m"
- "2.5 bath townhome in Sacramento 1800 sqft"

## How to run

The skill folder must contain a scripts folder which contains `cli.ts` and `parser.ts`. Run from the skill folder:

```bash
npx tsx {baseDir}/scripts/cli.ts --query "<the user's search text>"
```

Rules:
- Pass the user's search text verbatim as the `--query` value, wrapped in double quotes.
- Escape any double quotes inside the text.
- The short flag `-q` is equivalent to `--query`.
- If `query` is missing, the script prints usage and exits with code 1.

## Output

The script prints a JSON object to stdout. Any field it could not find is `null`.

Example output for the input "3 bed condo in Fresno under 500k with pool":

```json
{
  "city": "Fresno",
  "maxPrice": 500000,
  "beds": 3,
  "baths": null,
  "sqft": null,
  "type": "Condominium",
  "pool": "True",
  "hasView": null
}
```