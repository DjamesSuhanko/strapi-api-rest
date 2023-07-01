import requests

token = 'TOKEN_AQUI'

strapi_url = 'http://IP_DO_SERVIDOR:1337/api'

headers = {
    'Authorization': f'Bearer {token}'
}

#exemplo de criação de artigo
article = {
  'title': 'Meu novo artigo',
  'body': 'Conteúdo do artigo',
  'slug': 'meu-novo-artigo',
  'published_at': '2023-05-02%02:19:18.9512'
}   

def strapi_post(api, payload):
	print("api: " + api)
	print("payload: " + str(payload))
	payload = {'data': payload}
	response = requests.post(f'{strapi_url}/{api}', json=payload, headers=headers)
	print(response)


strapi_post('articles',article)
