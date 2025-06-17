import { z } from "zod";
import { createEnv } from "@t3-oss/env-core";

export const env = createEnv({
  server: {
    NODE_ENV: z
      .enum(["development", "test", "production"])
      .default("development"),
    DATABASE_URL: z.string().url(),
    DISCORD_TOKEN: z.string(),
    SENTRY_DSN: z.string().url(),
  },
  runtimeEnv: process.env,
});
