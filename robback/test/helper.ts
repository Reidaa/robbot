import Fastify, {FastifyPluginOptions} from 'fastify';
import fp from 'fastify-plugin';
import {Test} from 'tap';

import App from '../src/app';

export async function build(t: Test, opts: FastifyPluginOptions = {}) {
  const fastify = Fastify();
  await fastify.register(fp(App), {testing: true, ...opts});

  t.teardown(fastify.close.bind(fastify));

  return fastify;
}
