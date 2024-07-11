import 'dotenv/config';

import {server} from '@src/server';

async function main() {
  return await server();
}

main();
