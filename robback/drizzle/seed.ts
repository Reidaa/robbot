import 'dotenv/config';

import {neon} from '@neondatabase/serverless';
import {drizzle} from 'drizzle-orm/neon-http';
import {MangaTable, ServerTable} from './schema';

const sql = neon(process.env.DATABASE_URL as string);
const db = drizzle(sql);

async function main() {
  try {
    console.log('Seeding database');

    await db.delete(MangaTable);
    await db.delete(ServerTable);

    await db.insert(MangaTable).values([
      {
        title: 'Chainsaw Man',
      },
      {
        title: 'Boku no Hero Academia',
      },
    ]);
  } catch (error) {
    console.error(error);
    throw new Error('Failed to seed database');
  }
}

main();
