import Fastify from 'fastify';
import fp from 'fastify-plugin';

import App from '@src/app.js';
import { env } from "@src/env";

export async function server() {
  const fastify = Fastify({
    logger: {
      transport: {
        target: '@fastify/one-line-logger',
      },
    },
  });

  try {
    await fastify.register(require('@fastify/sensible'));
    await fastify.register(fp(App));
    await fastify.listen({port: parseInt(env.PORT)});
  } catch (err) {
    fastify.log.error(err);
    throw new Error(err as string);
  }
}
