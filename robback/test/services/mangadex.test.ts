import t from 'tap';
import {Mangadex} from '@services/mangadex';

t.test("GET Chainsaw Man's manga informations", async t => {
  const mangadex = new Mangadex();
  const manga_id = 'a77742b1-befd-49a4-bff5-1ad4e6b0ef7b';

  const response = await mangadex.getOneManga(manga_id);

  t.equal(response.status, 200);
  t.equal(response.data['result'], 'ok');
  t.equal(response.data['response'], 'entity');
});

t.test("GET Chainsaw Man's chapters", async t => {
  const mangadex = new Mangadex();
  const manga_id = 'a77742b1-befd-49a4-bff5-1ad4e6b0ef7b';

  const response = await mangadex.getOneMangaFeed(manga_id);

  // console.log(response.data);
  t.equal(response.status, 200);
  t.equal(response.data['result'], 'ok');
  t.equal(response.data['response'], 'collection');
});

t.test('Searching for a manga', async t => {
  const mangadex = new Mangadex();
  const title = 'chainsaw man';

  const response = await mangadex.getManyMangas(title);

  console.log(response.data);
  t.equal(response.status, 200);
  t.equal(response.data['result'], 'ok');
  t.equal(response.data['response'], 'collection');
});
