import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const playwrightPath = process.env.PLAYWRIGHT_PACKAGE || "playwright";
const { chromium } = require(playwrightPath);

const baseUrl = process.env.ARTIFACT_URL || "http://127.0.0.1:4173";

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });

await page.goto(baseUrl, { waitUntil: "networkidle" });
await page.locator(".command-surface").screenshot({ path: "docs/images/command-center.png" });
await page.locator("#prd-studio").screenshot({ path: "docs/images/prd-studio.png" });
await page.locator("#model-lab").screenshot({ path: "docs/images/model-trust-lab.png" });

await browser.close();
console.log("Captured portfolio artifact screenshots.");
