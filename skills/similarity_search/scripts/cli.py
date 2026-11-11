import sys
import json

from search import build_all_listing_embeddings, find_similar_listings

query = sys.argv[1]
json_path = sys.argv[2]
k = int(sys.argv[3]) if len(sys.argv) > 3 else 5

with open(json_path, "r") as f:
    listings = json.load(f)

listing_embeddings = build_all_listing_embeddings(listings)
top_ids = find_similar_listings(query, listing_embeddings, k)

by_id = {row["L_ListingID"]: row for row in listings}
top_listings = [by_id[lid] for lid in top_ids]

print(json.dumps(top_listings, indent=2))