---
name: memory
description: Remembers each user's home-search preferences (city, max price, beds, baths, property type, pool) and the last listings shown, across messages. Use this skill whenever a user is searching for homes, houses, apartments, condos or rentals, gives or changes a search filter, asks a follow-up like "show me the second one", "anything cheaper?", "what about 4 beds?", or says "start over" or "new search", even if they never mention memory or sessions.
metadata: {"openclaw":{"emoji":"🏠","requires":{"bins":["node","npx"]}}}
---

# Real Estate Session Memory

This skill keeps a small per-user state record so the conversation does not
start from zero on every message. It is a script, not a search engine: it only
stores and returns what you give it. Run the listing search with whatever
other tool or skill you normally use.

## Session fields

| Field | Type | Meaning |
|---|---|---|
| `city` | string | Where the user wants to buy or rent |
| `maxPrice` | number | Budget ceiling, as a plain number (`650000`, not `"$650k"`) |
| `beds` | number | Minimum bedrooms |
| `baths` | number | Minimum bathrooms |
| `type` | string | `house`, `condo`, `apartment`, `townhouse`, etc. |
| `pool` | string | Pool preference, e.g. `"yes"`, `"no"`, `"any"` |
| `lastResults` | array | Listings most recently shown to the user |
| `conversationStep` | number | `0` new, `1` collecting filters, `2` results shown, `3` refining |

All filters are optional. Users fill them in gradually.

## Commands

Run from anywhere. Replace `<userId>` with a stable identifier for the person
(sender ID or chat ID from the channel). Always use the same ID for the same
person. If none is available, use `default`.

```bash

npx tsx {baseDir}/scripts/memory.ts get <userId>

npx tsx {baseDir}/scripts/memory.ts update <userId> '{"city":"Austin","beds":3}'

npx tsx {baseDir}/scripts/memory.ts clear <userId>
```

Every command prints the resulting session as JSON on stdout. Exit code is
non-zero with a message on stderr if something is wrong (bad JSON, unknown
command).

## Workflow

1. **At the start of any home-search message, run `get`.** Use the stored
   filters instead of asking the user again. Only ask for what is missing.
2. **When the user states or changes a filter, run `update` immediately**
   with just that field. Convert values first: "under 700k" becomes
   `"maxPrice":700000`, "three bedroom" becomes `"beds":3`.
3. **Run the listing search** using the stored filters, then show results.
4. **After showing results, run `update`** with `lastResults` (the listings
   you displayed, at most 10, keeping their ids/addresses/prices) and
   `"conversationStep":2`.
5. **For follow-ups** ("the second one", "any cheaper?", "same but 4 beds"),
   run `get`, resolve the reference against `lastResults` or adjust the
   relevant filter, update, and search again if filters changed.
6. **On "start over", "new search", or "forget that"**, run `clear`, then
   greet them as a fresh search.

## Rules

- Never invent filter values the user did not give. Leave fields unset.
- Do not read or write the state file directly. Always go through the CLI.
- Do not tell the user about sessions or JSON. Just say things like "Still
  looking in Austin with 3+ beds?"
- If a command fails, continue the conversation normally and ask the user for
  the details again rather than blocking on the error.
- Sessions expire after 24 hours of inactivity.