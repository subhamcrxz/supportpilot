import { getEnv, getEnvInt, DEFAULT_PORTS } from "@supportpilot/config";

export const env = {
  nodeEnv: getEnv("NODE_ENV", "development"),
  host: getEnv("API_HOST", "0.0.0.0"),
  port: getEnvInt("API_PORT", DEFAULT_PORTS.api),
  corsOrigin: getEnv("CORS_ORIGIN", "http://localhost:3000"),
} as const;

export const isDev = env.nodeEnv !== "production";
