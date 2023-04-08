import json
import os
import socket
import _thread
import requests

hsep = '\r\n'


# Here define some convenience functions
def parse_http(request):
    """Partial solution to Ex. 2. This extracts just the method and URI path
    ignoring everything else"""
    # print(request)
    reqline = request.decode().split(hsep).pop(0)
    try:
        cmd, path, prot = reqline.split()
    except ValueError:
        cmd = ''
        path = ''
    return cmd, path


def parse_authentication(request):
    key = request.decode().split().pop()
    return key


# Some convenience functions for writing and sending the status line
def http_status(connection, status):
    """Write and send a status line"""
    connection.send(('HTTP/1.1 ' + status + hsep).encode())


def deliver_200(connection):
    http_status(connection, '200 OK')


def deliver_404(connection):
    http_status(connection, '404 Not found')


def http_header(connection, headerline):
    """Send the header line input as Python string instance"""
    connection.send((headerline + hsep).encode())


def http_body(connection, payload):
    """Send payload given as byte string"""
    connection.send(hsep.encode())
    connection.send(payload)


def gobble_file(filename, binary=False):
    """General utility to read entire content of file that could be binary"""
    if binary:
        mode = 'rb'
    else:
        mode = 'r'
    with open(filename, mode) as fin:
        content = fin.read()
    return content


def deliver_html(connection, filename):
    """Deliver content of HTML file"""
    deliver_200(connection)
    content = gobble_file(filename)
    http_header(connection, 'Content-Type: text/html')
    http_body(connection, content.encode())


def deliver_jpg(connection, filename):
    """Deliver content of JPEG image file"""
    deliver_200(connection)
    content = gobble_file(filename, binary=True)
    http_header(connection, 'Content-Type: image/jpg')
    http_header(connection, 'Accept-Ranges: bytes')
    http_body(connection, content)


def deliver_json_string(connection, jsonstr):
    deliver_200(connection)
    http_header(connection, 'Content-Type: application/json')
    http_body(connection, jsonstr.encode())


def deliver_json(connection, filename):
    """Deliver JSON stored in a server-side file"""
    content = gobble_file(filename)
    deliver_json_string(connection, content)


def parse_form_data(request):
    # Extract the method and URI path
    method, path = parse_http(request)

    # Split the request into headers and body
    headers, body = request.decode().split(hsep + hsep, 1)

    # print(body)

    # Parse the form data
    parsed_form_data = {}
    form_data_pairs = body.split('&')
    # print(form_data_pairs)
    for pair in form_data_pairs:
        question, answer = pair.split('=')
        if question.startswith("question"):
            # Extract the question number and value from the question parameter
            question_number = (question.split("%5B")[1].split("%5D")[0])
            parsed_form_data[question_number] = int(answer)
        elif question.startswith("message") or question.startswith("residence") or question.startswith(
                "birthplace") or question.startswith("name"):
            parsed_form_data[question] = answer.replace('+', ' ')
        elif question.startswith("pets"):
            # Append the pet value to the pets array in parsed_form_data
            if "pets" not in parsed_form_data:
                parsed_form_data["pets"] = []
            parsed_form_data["pets"].append(answer)
        else:
            parsed_form_data[question] = answer

    # print(json.dumps(parsed_form_data))

    with open("input.json", "w") as file:
        json.dump(parsed_form_data, file)


def analyze():
    with open('input.json') as f:
        data = json.load(f)

    responses = {}
    profile = {}
    job_scores_total = {}

    for k, v in data.items():
        if isinstance(v, int):
            responses[k] = v

    job_scores = {
        "ceo": [4, 5, 5, 2, 2, 5, 2, 2, 5, 2, 3, 1, 3, 2, 5, 3, 5, 5, 2, 2],
        "astronaut": [1, 5, 4, 3, 1, 4, 4, 3, 1, 5, 1, 2, 5, 5, 2, 5, 2, 2, 5, 3],
        "doctor": [3, 4, 4, 5, 1, 5, 3, 5, 3, 4, 2, 2, 4, 4, 2, 3, 2, 2, 4, 4],
        "model": [3, 2, 3, 2, 5, 2, 4, 3, 2, 1, 4, 3, 3, 3, 5, 1, 5, 4, 1, 1],
        "rockstar": [5, 3, 5, 2, 5, 2, 5, 5, 4, 4, 2, 4, 1, 1, 5, 1, 5, 4, 1, 4],
        "garbage": [1, 1, 1, 3, 5, 1, 1, 5, 2, 1, 5, 5, 5, 5, 1, 5, 2, 1, 3, 3],
    }

    apis = {
        "dog": "https://dog.ceo/api/breeds/image/random",
        "cat": "https://api.thecatapi.com/v1/images/search",
        "duck": "https://random-d.uk/api/v2/random",
        "ceo": "https://www.omdbapi.com/?apikey=39aeb1f7&t=the+wolf+of+wall+street",
        "astronaut": "https://www.omdbapi.com/?apikey=39aeb1f7&t=alien",
        "doctor": "https://www.omdbapi.com/?apikey=39aeb1f7&t=doctor+who",
        "model": "https://www.omdbapi.com/?apikey=39aeb1f7&t=zoolander",
        "rockstar": "https://www.omdbapi.com/?apikey=39aeb1f7&t=school+of+rock",
        "garbage": "https://www.omdbapi.com/?apikey=39aeb1f7&t=clean"
    }

    suitability = 5
    for job, scores in job_scores.items():
        total = 0
        for qno, response in responses.items():
            total += response * scores[int(qno) - 1]
        job_scores_total[job] = total

    best_job = max(job_scores_total, key=job_scores_total.get)

    desired_job = data['job']

    suitability = 6

    for job, total in job_scores_total.items():
        if job_scores_total[job] > job_scores_total[desired_job]:
            suitability -= 1

    movie_uri = apis[desired_job]
    response = requests.get(movie_uri)
    movie_data = json.loads(response.text)

    if desired_job == 'ceo':
        desired_job = 'CEO of large mega-corporation'
    elif desired_job == 'astronaut':
        desired_job = 'Astronaut'
    elif desired_job == 'doctor':
        desired_job = 'Medical doctor'
    elif desired_job == 'model':
        desired_job = 'Fashion model'
    elif desired_job == 'rockstar':
        desired_job = 'Rock star'
    else:
        desired_job = 'Refuse collection operative'

    if best_job == 'ceo':
        best_job = 'CEO of large mega-corporation'
    elif best_job == 'astronaut':
        best_job = 'Astronaut'
    elif best_job == 'doctor':
        best_job = 'Medical doctor'
    elif best_job == 'model':
        best_job = 'Fashion model'
    elif best_job == 'rockstar':
        best_job = 'Rock star'
    else:
        best_job = 'Refuse collection operative'

    profile['desired_job'] = desired_job
    profile['best_suited_job'] = best_job
    profile['suitability_for_chosen_job'] = suitability
    profile['movie'] = movie_data

    if "pets" in data:
        profile["pets"] = []
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
                profile["pets"].append({"name": pet, "image": filename})

            if pet == 'cat':
                uri = 'https://api.thecatapi.com/v1/images/search'
                response = requests.get(uri)
                data = json.loads(response.text)
                image_uri = data[0]['url']
                response = requests.get(image_uri)
                filename = os.path.basename(image_uri)
                with open(filename, "wb") as f:
                    f.write(response.content)
                profile["pets"].append({"name": pet, "image": filename})

            if pet == 'duck':
                uri = 'https://random-d.uk/api/v2/random'
                response = requests.get(uri)
                data = json.loads(response.text)
                image_uri = data['url']
                response = requests.get(image_uri)
                filename = os.path.basename(image_uri)
                with open(filename, "wb") as f:
                    f.write(response.content)
                profile["pets"].append({"name": pet, "image": filename})

    with open("pets.json", "w") as file:
        json.dump(profile["pets"], file)

    with open("profile.json", "w") as file:
        json.dump(profile, file)


# def authenticate(connection, request):
#     key = parse_authentication(request)
#     correct_key = 'MTkwMzIzMTU6MTkwMzIzMTU='
#     if key == correct_key:
#         return True
#     else:
#         connection.send(b'HTTP/1.1 401 Unauthorized\r\n')
#         # Request to authenticate
#         connection.send(b'WWW-Authenticate: Basic realm="Web 159352"')
#         connection.send(b'\r\n')
#         return False


# request handler
def do_request(connectionSocket):
    # Extract just the HTTP command (method) and path from the request
    request = connectionSocket.recv(20240)
    cmd, path = parse_http(request)
    print(cmd)
    print(path)

    if cmd == 'GET' and path == '/':
        deliver_html(connectionSocket, 'index.html')
    elif cmd == 'GET' and path == '/form':
        deliver_html(connectionSocket, 'psycho.html')
    elif cmd == 'GET' and path == '/view/input':
        deliver_json(connectionSocket, 'input.json')
    elif cmd == 'GET' and path == '/view/profile':
        deliver_json(connectionSocket, 'profile.json')
    elif cmd == 'GET' and path == '/input.json':
        deliver_json(connectionSocket, path.strip('/'))
    elif cmd == 'GET' and path == '/profile.json':
        deliver_json(connectionSocket, path.strip('/'))
    elif cmd == 'GET' and path.endswith('.jpg'):
        deliver_jpg(connectionSocket, path.strip('/'))
    elif cmd == 'POST' and path == '/analysis':
        parse_form_data(request)
        analyze()
        deliver_200(connectionSocket)
    else:
        deliver_404(connectionSocket)

    # Implement our URI path mapping scheme - here remove leading and
    # trailing '/' and use what's left as a local file name
    filename = path.strip('/')
    ftype = filename.split('.').pop()  # the file extension

    # sign_in_status = authenticate(connectionSocket, request)

    # If file exists, try and deliver
    # if os.path.exists(filename) and sign_in_status:
    # if os.path.exists(filename):
    #
    #
    #     deliver_200(connectionSocket)
    #     # Deliver according to filename extension type. So far only HTML and
    #     # JPEG are supported
    #     if ftype == 'html':
    #         deliver_html(connectionSocket, filename)
    #     elif ftype == 'jpeg':
    #         deliver_jpeg(connectionSocket, filename)
    #     else:
    #         deliver_404(connectionSocket)
    #
    # # ... otherwise deliver "Not found" response
    # else:
    #     deliver_404(connectionSocket)

    # Close the connection
    connectionSocket.close()


def main(serverPort):
    # Create the server socket object
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the server socket to the port
    mySocket.bind(('', serverPort))

    # Start listening for new connections
    mySocket.listen()
    # print('The server is ready to receive messages on port:', serverPort)

    while True:
        # Accept a connection from a client
        connectionSocket, addr = mySocket.accept()

        # Handle each connection in a separate thread
        _thread.start_new_thread(do_request, (connectionSocket,))


if __name__ == '__main__':
    serverPort = 8080
    main(serverPort)
