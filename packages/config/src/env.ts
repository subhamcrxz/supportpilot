/**
 * Read a required environment variable.
 * Throws at startup if missing — use for values the service cannot run without.
 */
export function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

/**
 * Read an optional environment variable with a default fallback.
 */
export function getEnv(name: string, defaultValue: string): string {
  return process.env[name] ?? defaultValue;
}

/**
 * Parse an integer environment variable with validation.
 */
export function getEnvInt(name: string, defaultValue: number): number {
  const raw = process.env[name];
  if (raw === undefined) {
    return defaultValue;
  }
  const parsed = Number.parseInt(raw, 10);
  if (Number.isNaN(parsed)) {
    throw new Error(`Environment variable ${name} must be an integer, got: ${raw}`);
  }
  return parsed;
}

/** Shared default ports for local development */
export const DEFAULT_PORTS = {
  web: 3000,
  api: 3001,
  aiEngine: 8000,
} as const;

/** Shared service URL keys used across apps */
export const ENV_KEYS = {
  databaseUrl: "DATABASE_URL",
  redisUrl: "REDIS_URL",
  apiUrl: "API_URL",
  aiEngineUrl: "AI_ENGINE_URL",
  openaiApiKey: "OPENAI_API_KEY",
} as const;
