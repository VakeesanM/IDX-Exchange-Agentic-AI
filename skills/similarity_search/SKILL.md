---
name: similarity-search
description: Provides similarity search functionality between user query and found real state listings from database, allowing you to find the most relevant listings.
version: 1.0 .0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---


# Similarity Search

This skill takes a list of already-found listings and reranks them by relevance to the user's query. Not every listing returned by the initial database lookup will be truly relevant, so this skill helps you surface the most relevant ones from that set.

## When to Use

Use this skill, after you have already looked up listings using the Database Integration skill and now want to find which of listing are actually relevant to the user's query.


## How to Run

This Skill requires two things; Listings from the database(As a Json) and the user's query.

This skill contain a folder called scripts with `cli.py`.

To use this skill, run this command in the command line:

```bash

python3 scripts/cli.py "User's Query" "Feed the entire JSON"

```


