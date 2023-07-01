import requests
import os
import magic
import sys
import json

def import_posts():
    for row in get_rows():
        print(row['post_title'])

        filters = {
            'filters[slug][$eq]': row['slug'],
        }

        if strapi_get('articles', filters=filters):
            continue

        tags = row['tags'] or 'Sem Tag'
        article = {
            'title': row['post_title'],
            'body': markdownify(row['post_content'], heading_style='ATX'),
            'metaDescription': row['meta_description'],
            'slug': row['slug'],
            'category': {
                'id': prepare_category(row['categories'].split(',')[0])
            },
            'author': {
              'id': prepare_author('admin', 'admin@luanet.net')
            },
            'tags': [{'id': tag} for tag in map(prepare_tag, tags.split(','))],
        }

        if row['featured_image']:
            article['featuredImage'] = {
                'id': prepare_image(row['featured_image'], row['image_alt'])
            }

        strapi_post('articles', article)