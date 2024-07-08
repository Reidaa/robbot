import 'dotenv/config';

import {neon} from '@neondatabase/serverless';
import {drizzle} from 'drizzle-orm/neon-http';
import {MangaTable, ServerTable} from './schema';
import {uuid} from 'drizzle-orm/pg-core';

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
        mangadexId: 'a77742b1-befd-49a4-bff5-1ad4e6b0ef7b',
      },
      {
        title: 'Boku no Hero Academia',
        mangadexId: '4f3bcae4-2d96-4c9d-932c-90181d9c873e',
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
