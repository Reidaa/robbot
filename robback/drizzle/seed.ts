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

    await db.insert(ServerTable).values([
      {
        id: BigInt('1082820297876574239'),
      },
    ]);
  } catch (error) {
    console.error(error);
    throw new Error('Failed to seed database');
  }
}

main();
