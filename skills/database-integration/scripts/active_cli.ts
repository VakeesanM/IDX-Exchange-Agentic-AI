// search-cli.ts
import { readFileSync } from "fs";
import { searchActiveListings } from "./active_listing_search"; // adjust to your filename

async function main() {
  const [file, page = "1", limit = "10"] = process.argv.slice(2);
  if (!file) {
    console.error("Usage: npx ts-node search-cli.ts <filters.json> [page] [limit]");
    process.exit(1);
  }

  const filters = JSON.parse(readFileSync(file, "utf-8"));
  const rows = await searchActiveListings(filters, Number(page), Number(limit));

  console.log(JSON.stringify(rows, null, 2));
  process.exit(0); // closes the DB pool
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});