import Fastify from 'fastify';
import FastifyPlugin from 'fastify-plugin';
import Swagger from '@fastify/swagger';
import SwaggerUI from '@fastify/swagger-ui';

import App from '@src/app.js';
import {env} from '@src/env';

export async function server() {
  const fastify = Fastify({
    logger: {
      transport: {
        target: '@fastify/one-line-logger',
      },
    },
  });

  try {
    await fastify.register(Swagger);
    await fastify.register(SwaggerUI, {
      routePrefix: '/docs',
      uiConfig: {
        docExpansion: 'full',
        deepLinking: false,
      },
      uiHooks: {
        onRequest: function (request, reply, next) {
          next();
        },
        preHandler: function (request, reply, next) {
          next();
        },
      },
      staticCSP: true,
      transformStaticCSP: header => header,
      transformSpecification: (swaggerObject, request, reply) => {
        return swaggerObject;
      },
      transformSpecificationClone: true,
      validatorUrl: 'https://validator.swagger.io/validator',
    });
    await fastify.register(FastifyPlugin(App));
    await fastify.ready();
    fastify.log.info('Successfully registered all plugins');
    fastify.swagger();
    await fastify.listen({port: parseInt(env.PORT)});
  } catch (err) {
    fastify.log.error(err);
    throw new Error(err as string);
  }
}
