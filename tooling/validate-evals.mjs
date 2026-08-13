import { readFileSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";

const evalsDirectory = resolve(import.meta.dirname, "../tests/evals");
for (const file of readdirSync(evalsDirectory).filter((entry) => entry.endsWith(".json"))) {
  const value = JSON.parse(readFileSync(join(evalsDirectory, file), "utf8"));
  if (!value || typeof value !== "object") throw new Error(`${file}: expected a JSON object or array`);
}
console.log("Evaluation JSON is valid.");
