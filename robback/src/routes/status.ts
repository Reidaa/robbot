import {
  FastifyInstance,
  FastifyPluginOptions,
  FastifyReply,
  FastifyRequest,
} from 'fastify';
import S from 'fluent-json-schema';

export const autoPrefix = '/_app';

export default async function status(
  fstf: FastifyInstance,
  opts: FastifyPluginOptions
) {
  fstf.route({
    method: 'GET',
    url: '/status',
    handler: onStatus,
    schema: {
      description: 'Returns status and version of the application',
      response: {
        200: S.object().prop('status', S.string()),
      },
    },
  });

  async function onStatus(request: FastifyRequest, reply: FastifyReply) {
    return {
      status: 'ok',
    };
  }
}
