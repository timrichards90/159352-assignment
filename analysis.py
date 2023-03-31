import json
import os

import requests

if __name__ == '__main__':

    f = open('file.json')

    data = json.load(f)

    print(data)

    responses = {}

    for k, v in data.items():
        if isinstance(v, int):
            responses[k] = v

    print(responses)

    job_scores = {
        "ceo": [4, 5, 5, 2, 2, 5, 2, 2, 5, 2, 3, 1, 3, 2, 5, 3, 5, 5, 2, 2],
        "astronaut": [1, 5, 4, 3, 1, 4, 4, 3, 1, 5, 1, 2, 5, 5, 2, 5, 2, 2, 5, 3],
        "doctor": [3, 4, 4, 5, 1, 5, 3, 5, 3, 4, 2, 2, 4, 4, 2, 3, 2, 2, 4, 4],
        "model": [3, 2, 3, 2, 5, 2, 4, 3, 2, 1, 4, 3, 3, 3, 5, 1, 5, 4, 1, 1],
        "rockstar": [5, 3, 5, 2, 5, 2, 5, 5, 4, 4, 2, 4, 1, 1, 5, 1, 5, 4, 1, 4],
        "garbage": [1, 1, 1, 3, 5, 1, 1, 5, 2, 1, 5, 5, 5, 5, 1, 5, 2, 1, 3, 3],
    }

    job_scores_total = {}

    for job, scores in job_scores.items():
        total = 0
        for qno, response in responses.items():
            # print(qno, " ", response)
            total += response * scores[int(qno) - 1]
        job_scores_total[job] = total

    best_job = max(job_scores_total, key=job_scores_total.get)

    print(best_job)

    apis = {
        "dog": "https://dog.ceo/api/breeds/image/random",
        "cat": "https://api.thecatapi.com/v1/images/search",
        "duck": "https://random-d.uk/api/v2/random"
    }

    if "pets" in data:
        for pet in data["pets"]:
            if pet == 'dog':
                uri = 'https://dog.ceo/api/breeds/image/random'
                response = requests.get(uri)
                data = json.loads(response.text)
                image_uri = data['message']
                response = requests.get(image_uri)
                filename = os.path.basename(image_uri)
                if os.path.exists(filename):
                    os.remove(filename)
                with open(filename, "wb") as f:
                    f.write(response.content)

            if pet == 'cat':
                uri = 'https://api.thecatapi.com/v1/images/search'
                response = requests.get(uri)
                data = json.loads(response.text)
                image_uri = data[0]['url']
                response = requests.get(image_uri)
                filename = os.path.basename(image_uri)
                with open(filename, "wb") as f:
                    f.write(response.content)

            if pet == 'duck':
                uri = 'https://random-d.uk/api/v2/random'
                response = requests.get(uri)
                data = json.loads(response.text)
                image_uri = data['url']
                response = requests.get(image_uri)
                filename = os.path.basename(image_uri)
                with open(filename, "wb") as f:
                    f.write(response.content)
