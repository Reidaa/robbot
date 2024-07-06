import 'dotenv/config';

import {db} from './db';
import {MangaServerTable} from 'drizzle/schema';
import {eq} from 'drizzle-orm';

async function main() {
  console.log('hello Node.js and Typescript world :]');

  const manga = await db.query.MangaTable.findFirst();

  console.log(manga);

  const subs = await db
    .select({id: MangaServerTable.serverId})
    .from(MangaServerTable)
    .where(eq(MangaServerTable.serverId, BigInt('1082820297876574239')));

  console.log(subs);
}

main();
