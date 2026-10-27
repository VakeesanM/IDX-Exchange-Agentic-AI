import { parsePropertyQuery } from "./parser";

async function main() {
  const query = process.argv[2];

  if (!query) {
    console.error('Usage: npx tsx cli.ts "<property query>"');
    console.error('Example: npx tsx cli.ts "3 bed condo in Fresno under 500k with pool"');
    process.exit(1);
  }

  const result = await parsePropertyQuery(query);
  console.log(JSON.stringify(result, null, 2));
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});