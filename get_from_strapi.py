import requests

token = 'TOKEN_AQUI'

strapi_url = 'http://IP_DO_SERVIDOR:1337/api'

headers = {
    'Authorization': f'Bearer {token}'
}

article = {
  'title': 'Meu novo artigo',
  'body': 'Conteúdo do artigo',
  'slug': 'meu-novo-artigo',
  'published_at': '2023-05-02%02:19:18.9512'
}   

def strapi_get(api, filters={}):
    url = f'{strapi_url}/{api}'
    response = requests.get(url, params=filters, headers=headers)

    if response.status_code > 200:
        raise HTTPError(500, 'A busca deu problema', response.status_code, None, None)

    response = response.json()
    if type(response) is list:
        response = {'data': response}

    return response.get('data')

filters = {
        'filters[name][$eq]': 'GEMS.png',
        }

result = strapi_get('upload/files', filters)

print(result)
