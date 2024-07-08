import {FastifyInstance, FastifyPluginOptions} from 'fastify';
import AutoLoad from '@fastify/autoload';
import {join, resolve} from 'path';

export default async function (
  fastify: FastifyInstance,
  opts: FastifyPluginOptions
) {
  await fastify.register(AutoLoad, {
    dir: join(resolve(__dirname), 'routes'),
    dirNameRoutePrefix: false,
    options: Object.assign({}, opts),
  });
}
