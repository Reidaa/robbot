import {neon} from '@neondatabase/serverless';
import {drizzle} from 'drizzle-orm/neon-http';
import * as schema from '@drizzle/schema';
import { env } from "@src/env"

// const client = neon(process.env.DATABASE_URL as string);
const client = neon(env.POSTGRES_URL);
export const db = drizzle(client, {schema: schema, logger: true});

export async function addManga(title: string, mangadex_id: string) {
  try {
    await db.insert(schema.MangaTable).values({
      title: title,
      mangadexId: mangadex_id,
    });
  } catch (error) {
    console.error(error);
    throw new Error('Failed to insert data');
  }
}
