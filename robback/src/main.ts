import 'dotenv/config';

import {server} from '@src/server.js';

async function main() {
  return await server();
}

main().then();
