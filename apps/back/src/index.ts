import "dotenv/config";
import { drizzle } from "drizzle-orm/libsql";
import { env } from "~/env";

const db = drizzle(env.DATABASE_URL!);

function main() {
  console.log("Hello, world!");
}
