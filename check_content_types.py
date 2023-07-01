import requests
import json

url = "http://IP_DO_SERVIDOR:1337"  # Mude para o endereço do seu servidor Strapi

# Substitua 'YOUR_API_TOKEN' por sua chave de API ou JWT
headers = {
    "Authorization": "YOUR_API_TOKEN",
    "Content-Type": "application/json",
}

print("Starting...")
# Recuperando os detalhes dos Content Types
#response = requests.get(f"{url}/content-manager/content-types", headers=headers)
response = requests.get(f"{url}/content-manager/content-types", headers=headers)

if response.status_code == 200:
    content_types = response.json()
    for content_type in content_types['data']:
        print(f"Nome do Content Type: {content_type['info']['name']}")

        # Imprimir campos do Content Type
        print("Campos:")
        for field_name, field_info in content_type['schema']['attributes'].items():
            print(f"  - {field_name}: {field_info['type']}")
            
        print("\n-------\n")

else:
    print(f"Erro ao recuperar Content Types. Código de status: {response.status_code}")

print("Done!")
