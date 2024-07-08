import 'dotenv/config';

import Fastify from 'fastify';

import fp from 'fastify-plugin';
import App from './app';

async function main() {
  const fastify = Fastify({
    logger: true,
  });

  try {
    await fastify.register(fp(App));
    await fastify.listen({port: 3000});
  } catch (err) {
    fastify.log.error(err);
    throw new Error(err as string);
  }
}

main();
