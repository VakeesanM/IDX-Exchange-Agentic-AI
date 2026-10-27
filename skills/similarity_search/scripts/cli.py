import sys
import json

from skills.similarity_search.scripts.search import build_listing_embedding, find_similar_listings

query = sys.argv[1]
listing = json.loads(sys.argv[2])
listing_embedding = build_listing_embedding(listing)
k = 5 if sys.argv[3] is None else int(sys.argv[3])
print(find_similar_listings(query, listing_embedding, k))
