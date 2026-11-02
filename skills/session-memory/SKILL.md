---
name: session-memory
description: Stores, updates, and retrieves per-user session memory so interactions stay context-aware. Use this skill to gather the user's real estate requirements before querying the property database.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
---

# Session Memory

Stores and retrieves session memory for users. Use it to maintain state across multiple interactions so responses stay personalized and relevant.

## When to use

Use this skill to maintain context across multiple turns with a user.

Example: a user searching for real estate listings gives only a city and a max price. Store those values in session memory, then retrieve them when the user provides more filters, so you can build a complete query.

Before searching the property database, you need these fields:

```json
{
  "city": null,
  "maxPrice": null,
  "beds": null,
  "baths": null,
  "sqft": null,
  "type": null,
  "pool": null,
  "hasView": null
}
```

If any field is null:

1. Save all non-null values to session memory using this skill.
2. Ask the user a clarifying question for each null value.

## Asking for missing values

Ask in this order, skipping any field that already has a value:

`city` → `maxPrice` → `beds` → `baths` → `sqft` → `type` → `pool` → `hasView`

Ask one question at a time, update session memory after each answer, and repeat until no null values remain.

## Starting a new search

If the user begins a new search, clear their session first, then save the newly parsed values.

## Example

**User:** Find me houses in San Jose with 3 bedrooms and 2000 sqft.

Using the property-parser skill, you get:

```json
{
  "city": "San Jose",
  "maxPrice": null,
  "beds": 3,
  "baths": null,
  "sqft": 2000,
  "type": null,
  "pool": null,
  "hasView": null
}
```

Save this to session memory, then continue:

**AI:** What is your max price?
**User:** 2 million.

Update session memory with `maxPrice: 2000000`, then ask about the next null value (`baths`), and so on.

## How to run

This skill includes a `scripts` folder containing `cli.ts`, a command line interface for reading and writing session memory for a specific user. It supports three commands: `get`, `update`, and `clear`.

### Get a session

```bash
npx ts-node {base_dir}/scripts/cli.ts get <user_id>
```

### Update a session

```bash
npx ts-node {base_dir}/scripts/cli.ts update <user_id> <path_to_json_file>
```

### Clear a session

```bash
npx ts-node {base_dir}/scripts/cli.ts clear <user_id>
```