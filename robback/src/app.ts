import {join, resolve} from 'path';

import {FastifyInstance, FastifyPluginOptions} from 'fastify';
import AutoLoad from '@fastify/autoload';
import Sensible from '@fastify/sensible';

async function app(fastify: FastifyInstance, opts: FastifyPluginOptions) {
  await fastify.register(Sensible);
  await fastify.register(AutoLoad, {
    dir: join(resolve(__dirname), 'routes'),
    dirNameRoutePrefix: false,
    options: Object.assign({}, opts),
  });
}

export default app;
