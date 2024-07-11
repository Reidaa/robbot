import axios, {isCancel, AxiosError, Method, AxiosRequestConfig} from 'axios';

export class Mangadex {
  private base_url: string;

  constructor() {
    this.base_url = 'https://api.mangadex.org';
  }

  public async getManyMangas(title: string) {
    const response = await this._call('GET', '/manga', {
      title: title,
      'availableTranslatedLanguage[]': 'en',
    });

    return response;
  }

  public async getOneManga(manga_id: string) {
    const response = await this._call('GET', `/manga/${manga_id}`);

    return response;
  }

  public async getOneMangaFeed(manga_id: string) {
    const response = await this._call('GET', `/manga/${manga_id}/feed`);

    return response;
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
