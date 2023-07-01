import os
import requests

strapi_url = "http://your-domain.com"
api_token = "your-auth-token"
upload_directory = "path/to/public/uploads"
headers = {"Authorization": f"Bearer {api_token}"}

def strapi_upload_image(image_path, alt_text):
    with open(image_path, "rb") as img_file:
        upload_files = {
            "files": (os.path.basename(image_path), img_file, "image/jpeg")
        }

        response = requests.post(
            f"{strapi_url}/upload",
            files=upload_files,
            data={"altText": alt_text},
            headers=headers
        )

        if response.status_code == 200:
            uploaded_image = response.json()[0]
            return uploaded_image["id"]
        else:
            print(f"Erro ao fazer upload da imagem: {image_path}")
            return None

for image_filename in os.listdir(upload_directory):
    image_filepath = os.path.join(upload_directory, image_filename)
    image_alt_text = f"Descrição da imagem {image_filename}"

    # Fazer o upload da imagem usando a API do Strapi
    strapi_upload_image(image_filepath, image_alt_text)

print("Imagens importadas com sucesso.")