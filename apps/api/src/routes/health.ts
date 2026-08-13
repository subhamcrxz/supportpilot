import type { FastifyInstance } from "fastify";
import type { ServiceHealth } from "@supportpilot/types";

export async function healthRoutes(app: FastifyInstance): Promise<void> {
  app.get("/health", async (): Promise<ServiceHealth> => {
    return {
      status: "ok",
      service: "api",
    };
  });
}
