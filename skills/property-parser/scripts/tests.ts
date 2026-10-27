import { parsePropertyQuery } from "./parser";
import { isDeepStrictEqual } from "node:util";


type Parsed = Awaited<ReturnType<typeof parsePropertyQuery>>;

interface TestCase {
  name: string;
  query: string;
  expected: Partial<Parsed>;
}

const EMPTY: Parsed = {
  city: null,
  maxPrice: null,
  beds: null,
  baths: null,
  sqft: null,
  type: null,
  pool: null,
  hasView: null,
};

const tests: TestCase[] = [
  {
    name: "basic condo with k-suffixed price",
    query: "3 bed condo in Fresno under 500k",
    expected: { city: "Fresno", maxPrice: 500_000, beds: 3, type: "Condominium" },
  },
  {
    name: "dollar sign, commas, and pool",
    query: "4 bedroom single family home in Clovis under $850,000 with pool",
    expected: {
      city: "Clovis",
      maxPrice: 850_000,
      beds: 4,
      type: "SingleFamilyResidence",
      pool: "True",
    },
  },
  {
    name: "half bath",
    query: "2.5 bath townhome in Sacramento under 650k",
    expected: { city: "Sacramento", maxPrice: 650_000, baths: 2.5, type: "Townhouse" },
  },
  {
    name: "decimal price with m suffix, land type",
    query: "land in Madera under 1.2m",
    expected: { city: "Madera", maxPrice: 1_200_000, type: "UnimprovedLand" },
  },
  {
    name: "multi-word city, beds + baths + view",
    query: "2 bed 2 bath condo in San Diego under 700k with view",
    expected: {
      city: "San Diego",
      maxPrice: 700_000,
      beds: 2,
      baths: 2,
      type: "Condominium",
      hasView: "True",
    },
  },
  {
    name: "sqft with plain number and plain price",
    query: "1800 sqft house in Visalia under 400,000",
    expected: { city: "Visalia", maxPrice: 400_000, sqft: 1800 },
  },
  {
    name: "hyphenated beds, pool and view, no price",
    query: "5-bed home in Bakersfield with pool and view",
    expected: { city: "Bakersfield", beds: 5, pool: "True", hasView: "True" },
  },
  {
    name: "no recognizable filters returns all nulls",
    query: "studio apartment",
    expected: {},
  },
  {
    // KNOWN BUG: "land" is matched as a substring of "Oakland", so type becomes UnimprovedLand.
    name: "city name containing a type keyword (Oakland)",
    query: "3 bed in Oakland under 900k",
    expected: { city: "Oakland", maxPrice: 900_000, beds: 3, type: null },
  },
  {
    // KNOWN BUG: the sqft regex's [\s,]* lets "1,500 sqft" match as 500 instead of 1500.
    name: "sqft with thousands separator",
    query: "1,500 sqft townhome in Reno at the lake",
    expected: { city: "Reno", sqft: 1500, type: "Townhouse" },
  },
];

async function run(): Promise<void> {
  let passed = 0;
  const failures: string[] = [];

  for (const [i, t] of tests.entries()) {
    const actual = await parsePropertyQuery(t.query);
    const expected: Parsed = { ...EMPTY, ...t.expected };
    const label = `${String(i + 1).padStart(2, "0")}. ${t.name}`;

    if (isDeepStrictEqual(actual, expected)) {
      passed++;
      console.log(`PASS  ${label}`);
    } else {
      console.log(`FAIL  ${label}`);
      console.log(`      query:    "${t.query}"`);
      for (const key of Object.keys(expected) as (keyof Parsed)[]) {
        if (!isDeepStrictEqual(actual[key], expected[key])) {
          console.log(
            `      ${key}: expected ${JSON.stringify(expected[key])}, got ${JSON.stringify(actual[key])}`
          );
        }
      }
      failures.push(label);
    }
  }

  console.log(`\n${passed}/${tests.length} passed`);
  if (failures.length > 0) process.exit(1);
}

run().catch((err) => {
  console.error("Test runner crashed:", err);
  process.exit(1);
});