import 'dotenv/config';
import {neon} from '@neondatabase/serverless';
import {drizzle} from 'drizzle-orm/neon-http';
import {migrate} from 'drizzle-orm/neon-http/migrator';
import {MangaServerTable, MangaTable, ServerTable} from './schema';

const sql = neon(process.env.DATABASE_URL as string);
const db = drizzle(sql);

async function main() {
  // await db.delete(MangaTable);
  // await db.delete(ServerTable);
  // await db.delete(MangaServerTable);

  try {
    await migrate(db, {
      migrationsFolder: './drizzle/migrations',
    });

    console.log('Migration successful');
  } catch (error) {
    console.error(error);
    throw new Error(error as string);
  }
}

main().then(r => r);
