ALTER TABLE "manga" RENAME TO "mangas";--> statement-breakpoint
ALTER TABLE "server" RENAME TO "servers";--> statement-breakpoint
ALTER TABLE "mangas" ADD COLUMN "created_at" timestamp DEFAULT now() NOT NULL;--> statement-breakpoint
ALTER TABLE "mangas" ADD COLUMN "updated_at" timestamp DEFAULT now() NOT NULL;--> statement-breakpoint
ALTER TABLE "servers" ADD COLUMN "created_at" timestamp DEFAULT now() NOT NULL;--> statement-breakpoint
ALTER TABLE "servers" ADD COLUMN "updated_at" timestamp DEFAULT now() NOT NULL;