import json
import os
import socket
import _thread
import analysis

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


def deliver_jpeg(connection, filename):
    """Deliver content of JPEG image file"""
    deliver_200(connection)
    content = gobble_file(filename, binary=True)
    http_header(connection, 'Content-Type: image/jpeg')
    http_header(connection, 'Accept-Ranges: bytes')
    http_body(connection, content)


# def deliver_gif(connection, filename):
#     """Deliver content of GIF image file"""
#     content = gobble_file(filename, binary=True)
#     deliver_200(connection)
#     http_header(connection, 'Content-Type: image/gif')
#     http_header(connection, 'Accept-Ranges: bytes')
#     http_body(connection, content)

def deliver_js(connection, filename):
    """Deliver Javascript"""
    content = gobble_file(filename)
    deliver_200(connection)
    http_header(connection, 'Content-Type: text/javascript')
    http_body(connection, content.encode())


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

    print(body)

    # Parse the form data
    parsed_form_data = {}
    form_data_pairs = body.split('&')
    print(form_data_pairs)
    for pair in form_data_pairs:
        question, answer = pair.split('=')
        if question.startswith("question"):
            # Extract the question number and value from the question parameter
            question_number = (question.split("%5B")[1].split("%5D")[0])
            parsed_form_data[question_number] = int(answer)
        # elif question == "pets[]":
        elif question.startswith("pets"):
            # Append the pet value to the pets array in parsed_form_data
            if "pets" not in parsed_form_data:
                parsed_form_data["pets"] = []
            parsed_form_data["pets"].append(answer)
        else:
            parsed_form_data[question] = answer

    print(json.dumps(parsed_form_data))

    with open("file.json", "w") as file:
        json.dump(parsed_form_data, file)

    # Convert the parsed form data to JSON and return it
    return json.dumps(parsed_form_data)


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
    #     deliver_gif(connectionSocket, path.strip('/'))
    elif cmd == 'POST' and path == '/analysis':
        parse_form_data(request)
        deliver_200(connectionSocket)
    else:
        deliver_404(connectionSocket)

    # elif cmd == 'GET' and path == '/datefunc.js':
    #     deliver_js(connectionSocket, 'datefunc.js')
    # elif path == '/dachshund.jpeg':
    #     deliver_jpeg(connectionSocket, path.strip('/'))
    # elif path in ['/pic_bulboff.gif', '/pic_bulbon.gif', '/sun.gif']:

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
    print('The server is ready to receive messages on port:', serverPort)

    while True:
        # Accept a connection from a client
        connectionSocket, addr = mySocket.accept()

        # Handle each connection in a separate thread
        _thread.start_new_thread(do_request, (connectionSocket,))


if __name__ == '__main__':
    serverPort = 8080
    main(serverPort)
