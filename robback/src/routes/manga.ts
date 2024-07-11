import {FastifyInstance, FastifyRequest} from 'fastify';
import S from 'fluent-json-schema';

import {Mangadex} from '@services/mangadex';

export const autoPrefix = '/manga';

interface ISearch {
  title: string;
}

export default async function manga(fstf: FastifyInstance) {
  fstf.route({
    method: 'GET',
    url: '/search',
    schema: {
      querystring: S.object().prop('title', S.string()).required(['title']),
    },
    handler: async (req: FastifyRequest<{Querystring: ISearch}>) => {
      try {
        const {title} = req.query;
        console.log(title);

        const mangadex = new Mangadex();
        const response = await mangadex.getManyMangas(title);

        for (const entry in response.data) {
          console.log(entry);
        }

        return response.data['data'];
      } catch (error) {
        return {};
      }
    },
  });
}
