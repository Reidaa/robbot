import dotenv from 'dotenv';
import {z} from 'zod';

dotenv.config();

const envSchema = z.object({
  POSTGRES_URL: z
    .string()
    .url()
    .refine(
      str => !str.includes('POSTGRES_URL'),
      'You forgot to change the default value'
    ),
  NODE_ENV: z
    .enum(['development', 'production', 'test'])
    .default('development'),
  PORT: z
    .string()
    .refine(
      port => parseInt(port) > 0 && parseInt(port) < 65536,
      'Invalid port number'
    )
    .default('3000'),
});

const result = envSchema.safeParse(process.env);

if (!result.success) {
  for (const issue of result.error.issues) {
    console.error(`${issue.path.join(',')}: ${issue.message}`);
  }
  throw new Error('Failed environment variables validation');
}

export const env = result.data;
