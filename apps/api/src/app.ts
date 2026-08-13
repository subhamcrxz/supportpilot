import Fastify from "fastify";
import cors from "@fastify/cors";
import { env, isDev } from "./config/env.js";
import { healthRoutes } from "./routes/health.js";

export async function buildApp() {
  const app = Fastify({
    logger: isDev,
  });

  await app.register(cors, {
    origin: env.corsOrigin,
    methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  });

  await app.register(healthRoutes);

  return app;
}
