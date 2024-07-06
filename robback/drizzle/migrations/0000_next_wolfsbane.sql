CREATE TABLE IF NOT EXISTS "mangaServer" (
	"manga_id" uuid NOT NULL,
	"server_id" bigint NOT NULL,
	CONSTRAINT "mangaServer_manga_id_server_id_pk" PRIMARY KEY("manga_id","server_id")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "manga" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"title" varchar NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "server" (
	"id" bigint PRIMARY KEY NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "mangaServer" ADD CONSTRAINT "mangaServer_manga_id_manga_id_fk" FOREIGN KEY ("manga_id") REFERENCES "public"."manga"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "mangaServer" ADD CONSTRAINT "mangaServer_server_id_server_id_fk" FOREIGN KEY ("server_id") REFERENCES "public"."server"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
