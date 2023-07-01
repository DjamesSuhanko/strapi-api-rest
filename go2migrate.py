import mysql.connector
import json
import magic
import os
import requests
from functools import lru_cache
from markdownify import markdownify
from urllib.error import HTTPError
# esse script migra os artigos do wordpress para o strapi. Ajuste os campos e query conforme necessario
# as configuracoes do banco estao no arquivo wp-config.php
# o strapi foi criado com um template para nao precisar criar os colletion types:
#  npx create-strapi-app NOME_PARA_SEU_STRAPI  --template @elegantstack/strapi-template-blog-backend

#CONNECTION TO STRAPI
auth_token = 'TOKEN_AQUI'
strapi_url = 'http://IP_DO_SERVIDOR:1337/api'

headers = {'Authorization': f'Bearer {auth_token}'}

# CONNECTION TO DATABASE
config = {
    'user': 'usuario_do_db_wp',
    'password': 'senha_do_db_wp',
    'host': 'localhost',
    'database': 'database_do_wp'
}

query = """
SELECT 
    p.ID as post_id, 
    p.post_title, 
    p.post_content, 
    p.post_name as slug, 
    p.post_date as published_at,
    wp2.meta_value as featured_image_path,
    wp3.meta_value as yoast_excerpt,
    GROUP_CONCAT(t.name SEPARATOR ', ') as tags
FROM wp_posts p
LEFT JOIN wp_postmeta wp1 ON (p.ID = wp1.post_id AND wp1.meta_key = '_thumbnail_id')
LEFT JOIN wp_posts p2 ON p2.ID = wp1.meta_value
LEFT JOIN wp_postmeta wp2 ON (p2.ID = wp2.post_id AND wp2.meta_key = '_wp_attached_file')
LEFT JOIN wp_postmeta wp3 ON (p.ID = wp3.post_id AND wp3.meta_key = '_yoast_wpseo_metadesc')
LEFT JOIN wp_term_relationships tr ON p.ID = tr.object_id
LEFT JOIN wp_term_taxonomy tt ON (tr.term_taxonomy_id = tt.term_taxonomy_id AND tt.taxonomy = 'post_tag')
LEFT JOIN wp_terms t ON t.term_id = tt.term_id
WHERE p.post_type = 'post' AND wp1.meta_value IS NOT NULL
GROUP BY p.ID;
"""

def strapi_post(api, payload):
    payload = {'data': payload}
    response = requests.post(f'{strapi_url}/{api}', json=payload, headers=headers)

    if response.status_code > 200:
        print("=== === ERROR === ===")
        print("Verify the last title above")
        print("=== === ===== === ===")
        

    return response.json().get('data')


def strapi_get(api, filters={}):
    url = f'{strapi_url}/{api}'
    response = requests.get(url, params=filters, headers=headers)

    if response.status_code > 200:
        raise HTTPError(500, 'FAIL ON STRAPI_GET', response.status_code, None, None)

    response = response.json()
    if type(response) is list:
        response = {'data': response}

    return response.get('data')


def strapi_post(api, payload):
    payload = {'data': payload}
    response = requests.post(f'{strapi_url}/{api}', json=payload, headers=headers)

    if response.status_code > 200:
        print(response.json())
        raise HTTPError(500, 'FAIL ON STRAPI_POST', response.status_code, None, None)

    return response.json().get('data')

def strapi_upload_img(file, image_alt):
    local_path = f'{file}'

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

@lru_cache
def prepare_image(path, image_alt):
    #pega a imagem no path; faz upload; devolve o id. Essa funcao eh usada diretamente na composicao em main()
    name = os.path.basename(path)

    filters = {
        'filters[name][$eq]': name,
        'filters[caption][$eq]': image_alt,
    }

    data = next(iter(strapi_get('upload/files', filters)), None)

    if not data:
        data = strapi_upload_img(path, image_alt)

    
    img_id = data.get('id')
    print("IMAGE ID {img_id}")
    return img_id   

def main():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute(query)

    counter = 0
    for row in cursor.fetchall():
        counter += 1

        post_id, title, content, slug, published_at, featured_image_path, yoast_excerpt, tags = row

        print(counter)
        print(f"{title}")


        filters = {
            'filters[slug][$eq]': f'{slug}',
        }

        if strapi_get('articles', filters=filters):
            continue
        
        #tags e author removidos
        article = {
            'title':         f"{title}",
            'body':          markdownify(f"{content}", heading_style='ATX'),
            'slug':          f"{slug}",
            'author':        f'3',
            'featured':      'true',
            'private':       'false',
            'thumbnailText': 'dobitaobyte.com.br',
            'date':          f"{published_at}",
            'image':         { 'id': prepare_image(f"uploads/{featured_image_path}","dobitaobyte.com.br") },
            'excerpt':       f"{yoast_excerpt}",
        }

        strapi_post('articles', article)


        #print(f"Post ID: {post_id}")
        #print(f"Title: {title}")
        #print(f"Content: {content}")
        #print(f"Slug: {slug}")
        #print(f"Featured Image Path: {featured_image_path}")
        #print(f"Yoast Excerpt: {yoast_excerpt}")
        #print(f"Tags: {tags}")
        #print()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()

