import * as Sentry from "@sentry/bun";

Sentry.init({
  dsn: "https://c8943d562c929c7fd9c0fb92d9df627f@o4509508299718656.ingest.de.sentry.io/4509508301160528",
});

function main() {
  console.log("Hello, world!");
}

main();
try {
  throw new Error("Sentry Bun test");
} catch (e) {
  Sentry.captureException(e);
}
