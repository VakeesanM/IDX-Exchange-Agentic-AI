---
name: session-memory
description: Manages, stores and reterieve session memory for users, allowing for context-aware interactions.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
---


# Session Memory

Stores and retrieves session memory for users, allowing for context-aware interactions. This skill is useful for maintaining state across multiple interactions with a user, enabling more personalized and relevant responses.

## When to use

Use this skill when you want to maintain context across multiple interactions with a user. 

For example, if a user is searching for real estate listings, however, they only give you a city and max price, you can store that information in the session memory. Then, when the user provides additional filters, you can retrieve the stored information and use it to construct a more complete query.


# How to run

This skill should contain a folder called `scripts` with a script called `cli.ts` that provides a command line interface for interacting with the session memory.

The `cli.ts` script allows you to get, update, and clear session memory for a specific user.

## Get Session
To get a existing session, run:

```bash
npx ts-node scripts/cli.ts get <user_id>
```

### Update Session
To update a session run:

```bash
npx ts-node scripts/cli.ts update <user_id> <path_to_json_file>
```

### Clear Session
To clear a session run:

```bash
npx ts-node scripts/cli.ts clear <user_id>
```
