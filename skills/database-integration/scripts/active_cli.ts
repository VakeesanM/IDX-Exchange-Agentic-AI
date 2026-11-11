import { promises as fs } from "fs";
import path from "path";
import { searchActiveListings } from "./active_listing_search"; 
async function main() {
  const filtersJson = process.argv[2];
  const page = Number(process.argv[3]) || 1;
  const limit = Number(process.argv[4]) || 10;

  if (!filtersJson) {
    console.error("Usage: npx tsx cli.ts '<filters-json>' [page] [limit]");
    console.error(`Example: npx tsx cli.ts '{"city":"Manteca","beds":2,"pool":"True"}' 1 5`);
    process.exit(1);
  }

  const filters = JSON.parse(filtersJson);
  const result = await searchActiveListings(filters, page, limit);

  const storageDir = path.join(__dirname, "storage");
  await fs.mkdir(storageDir, { recursive: true });
  const filePath = path.join(storageDir, "active-listings.json");
  await fs.writeFile(filePath, JSON.stringify(result, null, 2), "utf-8");
  console.log(`Saved ${result.length} active listings to ${filePath}`);

  process.exit(0);
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});