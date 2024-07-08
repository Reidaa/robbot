import {
  pgTable,
  uuid,
  varchar,
  timestamp,
  primaryKey,
  bigint,
} from 'drizzle-orm/pg-core';
// import {relations} from 'drizzle-orm';

export const MangaTable = pgTable('manga', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: varchar('title').notNull(),
  mangadexId: uuid('mangadex_id').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});

export const ServerTable = pgTable('server', {
  id: bigint('id', {mode: 'bigint'}).primaryKey().notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});

export const MangaServerTable = pgTable(
  'mangaServer',
  {
    mangaId: uuid('manga_id')
      .references(() => MangaTable.id, {onDelete: 'cascade'})
      .notNull(),
    serverId: bigint('server_id', {mode: 'bigint'})
      .references(() => ServerTable.id, {onDelete: 'cascade'})
      .notNull(),
  },
  table => {
    return {
      pk: primaryKey({columns: [table.mangaId, table.serverId]}),
    };
  }
);
