---
name: database-integration
description: Integrate with a database to search for active real estate listings and sold houses. Always usue this skill to find listings or comps in the database, and never use a search engine or other skill to find listings or comps.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
---

# Database Integration

Takes in a json object of propery filters, constructs sql queries from it, and returns a list of active listings or sold comps from the database.


## When to use

Use this skill, when you have structured property filters and want to search for active listings or sold comps in the database. The skill will return a list of listings that match the filters, along with relevant details such as price, beds, baths, sqft, and more.

Depending on if you active listings or sold comps, you need different inputs.


### Active Listings Example Inputs
For active listings, the input should be a json object with the following structure:

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

Optionally, a page number and limit can be passed in as well to paginate the results.


### Sold Comps Example Inputs
For sold comps, the input should be a city and number of months to look back for sold listings.

example: "Fresno", 12


## How to run

This skill should contain a folder called `scripts` with the following scripts:

- active_cli.ts: A command line interface to search for active listings. It takes in a json  of property filters, page number, and limit as arguments, and returns a list of active listings that match the filters.

```bash
npx tsx {baseDir}/scripts/active_cli.ts "<json_of_filters_as_string>" <page_number> <limit>
```

The output of it is saved to a file in the following location:
```bash
{baseDir}\scripts\storage\active-listings.json
```
Remember its location to use it for future use.


- sold_cli.ts: A command line interface to search for sold comps. It takes in a city and number of months as arguments, and returns a list of sold comps in that city within the specified time frame.

```bash
npx tsx {baseDir}/scripts/sold_cli.ts "<city>" <months>
```

The output of it is saved to a file in the following location:

```bash
{baseDir}\scripts\storage\sold-comps.json
```
Remember its location to use it for future use.

Its up to you to decide if you need only active, or only sold, or both, based on the query and situation.




### IMPORTANT NOTE
When you pass in the json object of filters, make sure to escape any double quotes inside the json string. For example, if you want to pass in the following json object:

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

You should pass it in as:
```bash
 '{\"city\":\"Fresno\",\"maxPrice\":500000,\"beds\":3,\"baths\":null,\"sqft\":null,\"type\":\"Condominium\",\"pool\":\"True\",\"hasView\":null}' 1 10
```

