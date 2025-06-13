import { pgTable, integer, varchar } from "drizzle-orm/pg-core";

export const server = pgTable("servers", {
  id: integer(),
  name: varchar(),
});
