# import json
# import os.path
#
# import requests
#
# if __name__ == '__main__':
#     dog_uri = 'https://dog.ceo/api/breeds/image/random'
#     cat_uri = 'https://api.thecatapi.com/v1/images/search'
#     duck_uri = 'https://random-d.uk/api/v2/random'
#
#     response = requests.get(duck_uri)
#     data = json.loads(response.text)
#
#     # dog
#     # image_uri = data['message']
#     # cat
#     # image_uri = data[0]['url']
#     # duck
#     # image_uri = data['url']
#
#     # make a separate GET request to the image URI to get the actual image data
#     response = requests.get(image_uri)
#
#     filename = os.path.basename(image_uri)
#     with open(filename, "wb") as f:
#         f.write(response.content)