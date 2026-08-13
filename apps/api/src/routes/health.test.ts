import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { buildApp } from "../app.js";

describe("GET /health", () => {
  it("returns ok status", async () => {
    const app = await buildApp();

    const response = await app.inject({
      method: "GET",
      url: "/health",
    });

    assert.equal(response.statusCode, 200);
    assert.deepEqual(response.json(), {
      status: "ok",
      service: "api",
    });

    await app.close();
  });
});
