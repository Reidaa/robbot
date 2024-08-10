import {FastifyInstance, FastifyRequest} from 'fastify';
import S from 'fluent-json-schema';

import {Mangadex} from '@services/mangadex';

export const autoPrefix = '/manga';

const LANGUAGES = {
  EN: 'en',
  FR: 'fr',
};

interface ISearch {
  title: string;
}

export default async function manga(instance: FastifyInstance) {
  instance.route({
    method: 'GET',
    url: '/search',
    schema: {
      querystring: S.object()
        .prop('title', S.string())
        .required()
        .prop('language', S.string().enum(Object.values(LANGUAGES))),
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
