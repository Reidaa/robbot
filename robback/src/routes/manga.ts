import {FastifyInstance, FastifyRequest} from 'fastify';
import S from 'fluent-json-schema';

import {Mangadex} from '@services/mangadex';

export const autoPrefix = '/manga';

interface ISearch {
  title: string;
}

interface ITrack {
  manga_id: string;
}

export default async function manga(instance: FastifyInstance) {
  instance.route({
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
  // instance.route({
  //   method: "POST",
  //   url: "/track",
  //   schema: {
  //     querystring: S.object().prop("manga_id", S.string().format("uuid")).required(["manga_id"])
  //   },
  //   handler: async (req: FastifyRequest<{Querystring: ITrack}>) => {
  //     try {
  //       const {manga_id} = req.query;

  //       const mangadex = new Mangadex();
  //       const info = await mangadex.getOneManga(manga_id);
  //       return {};
  //     } catch (err) {
  //       return {};
  //     }
  //   },
  // });
}
