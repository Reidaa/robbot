import axios, {Method} from 'axios';

export class Mangadex {
  private readonly base_url: string;

  constructor() {
    this.base_url = 'https://api.mangadex.org';
  }

  public async getManyMangas(title: string, translated_language: string = "en") {
    return await this._call('GET', '/manga', {
      title: title,
      'availableTranslatedLanguage[]': translated_language,
    });
  }

  public async getOneManga(manga_id: string) {
    return await this._call('GET', `/manga/${manga_id}`);
  }

  public async getOneMangaFeed(manga_id: string) {
    return await this._call('GET', `/manga/${manga_id}/feed`);
  }

  private async _call(
    method: Method,
    endpoint: string,
    params?: Record<string, unknown>,
    body?: Record<string, unknown>
  ) {
    return axios({
      method: method,
      url: `${this.base_url}${endpoint}`,
      params: params,
      data: body,
    });
  }
}
