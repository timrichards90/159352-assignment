# import json
# import os
#
# import requests
#
# if __name__ == '__main__':
#
#     with open('input.json') as f:
#         data = json.load(f)
#
#     responses = {}
#     profile = {}
#     job_scores_total = {}
#
#     for k, v in data.items():
#         if isinstance(v, int):
#             responses[k] = v
#
#     job_scores = {
#         "ceo": [4, 5, 5, 2, 2, 5, 2, 2, 5, 2, 3, 1, 3, 2, 5, 3, 5, 5, 2, 2],
#         "astronaut": [1, 5, 4, 3, 1, 4, 4, 3, 1, 5, 1, 2, 5, 5, 2, 5, 2, 2, 5, 3],
#         "doctor": [3, 4, 4, 5, 1, 5, 3, 5, 3, 4, 2, 2, 4, 4, 2, 3, 2, 2, 4, 4],
#         "model": [3, 2, 3, 2, 5, 2, 4, 3, 2, 1, 4, 3, 3, 3, 5, 1, 5, 4, 1, 1],
#         "rockstar": [5, 3, 5, 2, 5, 2, 5, 5, 4, 4, 2, 4, 1, 1, 5, 1, 5, 4, 1, 4],
#         "garbage": [1, 1, 1, 3, 5, 1, 1, 5, 2, 1, 5, 5, 5, 5, 1, 5, 2, 1, 3, 3],
#     }
#
#     apis = {
#         "dog": "https://dog.ceo/api/breeds/image/random",
#         "cat": "https://api.thecatapi.com/v1/images/search",
#         "duck": "https://random-d.uk/api/v2/random",
#         "ceo": "https://www.omdbapi.com/?apikey=39aeb1f7&t=the+wolf+of+wall+street",
#         "astronaut": "https://www.omdbapi.com/?apikey=39aeb1f7&t=alien",
#         "doctor": "https://www.omdbapi.com/?apikey=39aeb1f7&t=doctor+who",
#         "model": "https://www.omdbapi.com/?apikey=39aeb1f7&t=zoolander",
#         "rockstar": "https://www.omdbapi.com/?apikey=39aeb1f7&t=school+of+rock",
#         "garbage": "https://www.omdbapi.com/?apikey=39aeb1f7&t=clean"
#     }
#
#     suitability = 5
#     for job, scores in job_scores.items():
#         total = 0
#         for qno, response in responses.items():
#             total += response * scores[int(qno) - 1]
#         job_scores_total[job] = total
#
#     best_job = max(job_scores_total, key=job_scores_total.get)
#
#     # print("Your suitability for each job is:")
#
#     desired_job = data['job']
#     suitability = 6
#
#     for job, total in job_scores_total.items():
#         if job_scores_total[job] > job_scores_total[desired_job]:
#             suitability -= 1
#
#     # print(suitability)
#     #
#     # for job, total in job_scores_total.items():
#     #     print(f"{job}: {total}")
#     #
#     # print(f"Based on your responses, you are best suited for the job of {best_job}.")
#
#     movie_uri = apis[desired_job]
#     response = requests.get(movie_uri)
#     movie_data = json.loads(response.text)
#
#     profile['desired_job'] = desired_job
#     profile['best_suited_job'] = best_job
#     profile['suitability_for_chosen_job'] = suitability
#     profile['movie'] = movie_data
#
#     if "pets" in data:
#         for pet in data["pets"]:
#             if pet == 'dog':
#                 uri = 'https://dog.ceo/api/breeds/image/random'
#                 response = requests.get(uri)
#                 data = json.loads(response.text)
#                 image_uri = data['message']
#                 response = requests.get(image_uri)
#                 filename = os.path.basename(image_uri)
#                 if os.path.exists(filename):
#                     os.remove(filename)
#                 with open(filename, "wb") as f:
#                     f.write(response.content)
#                 profile[pet] = filename
#
#             if pet == 'cat':
#                 uri = 'https://api.thecatapi.com/v1/images/search'
#                 response = requests.get(uri)
#                 data = json.loads(response.text)
#                 image_uri = data[0]['url']
#                 response = requests.get(image_uri)
#                 filename = os.path.basename(image_uri)
#                 with open(filename, "wb") as f:
#                     f.write(response.content)
#                 profile[pet] = filename
#
#             if pet == 'duck':
#                 uri = 'https://random-d.uk/api/v2/random'
#                 response = requests.get(uri)
#                 data = json.loads(response.text)
#                 image_uri = data['url']
#                 response = requests.get(image_uri)
#                 filename = os.path.basename(image_uri)
#                 with open(filename, "wb") as f:
#                     f.write(response.content)
#                 profile[pet] = filename
#
#     print(json.dumps(profile))
#
#     with open("profile.json", "w") as file:
#         json.dump(profile, file)