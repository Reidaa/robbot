CREATE TABLE IF NOT EXISTS "manga" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"title" varchar NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "server" (
	"id" integer PRIMARY KEY NOT NULL
);
