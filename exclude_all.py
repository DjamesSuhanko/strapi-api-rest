
import requests

auth_token = 'TOKEN_AQUI'
strapi_url = 'http://IP_DO_SERVIDOR:1337/api'

headers = {'Authorization': f'Bearer {auth_token}'}

def get_all_articles():
    response = requests.get(f"{strapi_url}/articles", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao recuperar artigos. Código de status: {response.status_code}")
        return []

# Função para excluir um artigo pelo ID
def delete_article(article_id):
    response = requests.delete(f"{strapi_url}/articles/{article_id}", headers=headers)
    if response.status_code == 200:
        print(f"Artigo com ID {article_id} excluído com sucesso!")
    else:
        print(f"Erro ao excluir o artigo. Código de status: {response.status_code}")

# Recupera todos os artigos e os exclui um por um
articles = get_all_articles()
for article in articles:
    delete_article(article["id"])
