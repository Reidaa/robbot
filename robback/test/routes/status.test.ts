import t from 'tap';
import {build} from '@test/helper';

t.test('Status route', async t => {
  const fastify = await build(t);
  const response = await fastify.inject({
    method: 'GET',
    path: '/_app/status',
  });

  t.equal(response.statusCode, 200);
  t.same(response.json(), {status: 'ok'});
});
