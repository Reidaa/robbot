import 'dotenv/config';
// import { migrate } from 'drizzle-orm/postgres-js/migrator';
// import { drizzle } from 'drizzle-orm/postgres-js';
// import postgres from 'postgres';

// const migrationClient = postgres(process.env.DATABASE_URL as string, { ssl: 'require', max: 1 })
//
// async function main() {
//   await migrate(drizzle(migrationClient), {
//     migrationsFolder: "./drizzle/migrations"
//   });
//   await migrationClient.end()
// }

import {neon} from '@neondatabase/serverless';
import {drizzle} from 'drizzle-orm/neon-http';
import {migrate} from 'drizzle-orm/neon-http/migrator';

const sql = neon(process.env.DATABASE_URL as string);
const db = drizzle(sql);

async function main() {
  try {
    await migrate(db, {
      migrationsFolder: './drizzle/migrations',
    });

    console.log('Migration successful');
  } catch (error) {
    console.error(error);
    throw new Error(error);
  }
}

main();
