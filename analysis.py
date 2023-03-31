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

    if "pets" in data:
        for pet in data["pets"]:
            print(pet)

    dog_uri = 'https://dog.ceo/api/breeds/image/random'
    cat_uri = 'https://api.thecatapi.com/v1/images/search'
    duck_uri = 'https://random-d.uk/api/v2/random'

    response = requests.get(duck_uri)
    data = json.loads(response.text)

    # dog
    # image_uri = data['message']
    # cat
    # image_uri = data[0]['url']
    # duck
    # image_uri = data['url']

    # make a separate GET request to the image URI to get the actual image data
    response = requests.get(image_uri)

    filename = os.path.basename(image_uri)
    with open(filename, "wb") as f:
        f.write(response.content)

#
# # In the code you provided, job_scores_total is a dictionary that will contain the total score for each job. The
# # outer for loop iterates over each item in the job_scores dictionary, which contains a mapping of each job to a list
# # of scores representing how important each personality trait is for that job.
# #
# # Inside the outer loop, a new variable total is initialized to 0. The inner for loop then iterates over each item in
# # the responses dictionary, which maps each question number to the user's response (a score from 1 to 5) for that
# # question.
# #
# # For each question, the score for the corresponding personality trait is looked up in the scores list using the
# # question number as an index (scores[qno-1]). This score is then multiplied by the user's response for that question
# # (response), and the result is added to the running total (total += response * scores[qno-1]).
# #
# # Once all questions have been processed for a given job, the total score for that job is stored in the
# # job_scores_total dictionary using the job name as the key (job_scores_total[job] = total).
# #
# # This process is repeated for each job in the job_scores dictionary, resulting in a final dictionary
# # job_scores_total containing the total score for each job. The job with the highest score represents the best match
# # for the user's personality traits, and can be returned as the recommended job.
