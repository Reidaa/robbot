import {neon} from '@neondatabase/serverless';
import {drizzle} from 'drizzle-orm/neon-http';
import * as schema from '@drizzle/schema';

const client = neon(process.env.DATABASE_URL as string);
export const db = drizzle(client, {schema: schema, logger: true});
