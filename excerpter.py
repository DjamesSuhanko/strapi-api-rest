from bs4 import BeautifulSoup
import requests
import json
from itertools import islice

token = 'TOKEN_HERE'

headers = {'Authorization': f'Bearer {token}'}

START = 5

END   = 1008

url = "http://ADDR_HERE:1337/api/articles/"

failed_articles = []

for i in range(START,END):
    response = requests.get(url + str(i), params={}, headers=headers)
    article = response.json()

    body_html = article['data']['attributes']['body']

    paragraphs = [line for line in body_html.split('\n') if line.strip() != '']
    non_empty_paragraphs = [paragraph for paragraph in paragraphs if paragraph and paragraph.strip()]

    first_two_paragraphs = list(islice(non_empty_paragraphs, 2))

    joined_paragraphs = '\n'.join(first_two_paragraphs)
    
    data = {
            "data": {
                    "excerpt": joined_paragraphs
                    }
            }

    response = requests.put(url + str(i),headers=headers, json=data)
    if response.status_code == 200:
        print(f"Artigo {i} atualizado com sucesso!")
    else:
        print(f"Falha ao atualizar o artigo {i}, status code: {response.status_code}")
        failed_articles.append(str(i))
    #

print(failed_articles)
