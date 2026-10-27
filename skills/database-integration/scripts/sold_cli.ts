// sold-cli.ts
import { getSoldComps } from "./sold_listing_search"; // adjust to your filename

async function main() {
  const [city, months = "12"] = process.argv.slice(2);
  if (!city) {
    console.error('Usage: npx ts-node sold-cli.ts "<city>" [months]');
    process.exit(1);
  }

  const rows = await getSoldComps(city, Number(months));

  console.log(JSON.stringify(rows, null, 2));
  process.exit(0); 
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});