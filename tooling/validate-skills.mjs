import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const repositoryRoot = resolve(import.meta.dirname, "..");
const registry = JSON.parse(readFileSync(join(repositoryRoot, "registry.json"), "utf8"));
const names = registry.skills.map((entry) => entry.name);
if (new Set(names).size !== names.length) throw new Error("registry contains duplicate Skill names");

const directories = readdirSync(join(repositoryRoot, "skills"))
  .filter((entry) => statSync(join(repositoryRoot, "skills", entry)).isDirectory())
  .sort();
if (JSON.stringify(directories) !== JSON.stringify([...names].sort())) {
  throw new Error(`registry/directory mismatch: registry=${names.sort()} directories=${directories}`);
}

for (const entry of registry.skills) {
  const directory = join(repositoryRoot, "skills", entry.name);
  const source = readFileSync(join(directory, "SKILL.md"), "utf8");
  if (!source.startsWith("---\n") || !source.includes(`\nname: ${entry.name}\n`) || !/\ndescription: .+/.test(source)) {
    throw new Error(`${entry.name}: invalid SKILL.md frontmatter`);
  }
  if (readdirSync(directory).some((file) => /^readme\.md$/i.test(file))) {
    throw new Error(`${entry.name}: repository documentation must not be inside the installable Skill`);
  }
  if (/(?:sk_live_|sk_test_|github_pat_|ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)/.test(source)) {
    throw new Error(`${entry.name}: possible credential in SKILL.md`);
  }
}
console.log(`Validated ${registry.skills.length} public Skills.`);
