
import { promises as fs } from "fs";
import path from "path";
import { getSoldComps } from "./sold_listing_search"; 

async function main() {
  const [city, months = "12"] = process.argv.slice(2);
  if (!city) {
    console.error('Usage: npx ts-node sold-cli.ts "<city>" [months]');
    process.exit(1);
  }

  const rows = await getSoldComps(city, Number(months));

  const storageDir = path.join(__dirname, "storage");
  await fs.mkdir(storageDir, { recursive: true });
  const filePath = path.join(storageDir, "sold-comps.json");
  await fs.writeFile(filePath, JSON.stringify(rows, null, 2), "utf-8");
  await console.log(`Saved ${rows.length} sold comps to ${filePath}`);

  process.exit(0); 
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});