import 'dotenv/config';

import {db} from './db';

async function main() {
  console.log('hello Node.js and Typescript world :]');

  const manga = await db.query.MangaTable.findFirst();

  console.log(manga);
}

main();
