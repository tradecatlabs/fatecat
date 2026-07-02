const baseUrl = process.env.FATECAT_API_URL || "http://127.0.0.1:8001";

const response = await fetch(`${baseUrl.replace(/\/$/, "")}/capabilities/almanac/calculate`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    dateRange: { start: "2026-05-08", end: "2026-05-08" },
    eventType: "出行",
    place: "北京",
  }),
});

if (!response.ok) {
  throw new Error(`FateCat request failed: ${response.status}`);
}

console.log(JSON.stringify(await response.json(), null, 2));
