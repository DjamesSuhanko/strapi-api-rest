import requests
import os
import magic
import sys
import json

#zypper install python310-magic (ou python3-blabla-python-magic? verificar)

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

def strapi_upload(file, image_alt):
    local_path = f'./IMGS/{file}'

    with open(local_path, 'r+b') as f:
        files = {
            'files': (
                os.path.basename(file),
                f,
                magic.from_file(local_path, mime=True)
            )
        }

        data = {
            'path': os.path.dirname(file),
            'fileInfo': json.dumps({
                'alternativeText': image_alt,
                'caption': image_alt,
            })
        }

        response = requests.post(f'{strapi_url}/upload', files=files, data=data, headers=headers)

    return response.json()[0]

result = strapi_upload(str(sys.argv[1]),'text to alt')
