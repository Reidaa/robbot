import {pgTable, uuid, varchar, integer, timestamp} from 'drizzle-orm/pg-core';
// import {relations} from 'drizzle-orm';

export const MangaTable = pgTable('mangas', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: varchar('title').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});

export const ServerTable = pgTable('servers', {
  id: integer('id').primaryKey().notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});
