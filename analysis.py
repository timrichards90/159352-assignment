import json
import cgi
import analysis
import socket
import _thread

hsep = '\r\n'

# Here define some convenience functions
# ...

# This is the main function to handle incoming requests
def handle_request(connection, address):
    # Receive and parse the HTTP request
    request = connection.recv(4096)
    method, path = parse_http(request)

    # Handle POST requests to /analysis
    if method == 'POST' and path == '/analysis':
        # Parse the form data using cgi.FieldStorage
        form = cgi.FieldStorage(
            fp=request,
            headers=request.decode().split(hsep)[1:-2],
            environ={'REQUEST_METHOD': 'POST'}
        )

        # Construct a dictionary from the form data
        data = {
            'name': form.getvalue('name'),
            'gender': form.getvalue('gender'),
            'birthyear': form.getvalue('birthyear'),
            'birthplace': form.getvalue('birthplace'),
            'residence': form.getvalue('residence'),
            'job': form.getvalue('job'),
            'pets': form.getlist('pets'),
            'message': form.getvalue('message'),
            'question': [int(form.getvalue('question['+str(i)+']')) for i in range(1,21)]
        }

        # Call your analysis function with the data
        result = analysis.analyze(data)

        # Send the JSON-encoded result back to the client
        http_status(connection, '200 OK')
        connection.send(('Content-Type: application/json' + hsep).encode())
        connection.send(('Access-Control-Allow-Origin: *' + hsep).encode())
        connection.send(hsep.encode())
        connection.send(json.dumps(result).encode())

    # Handle all other requests with a 404 error
    else:
        http_status(connection, '404 Not Found')
        connection.send(('Content-Type: text/html' + hsep).encode())
        connection.send(hsep.encode())
        connection.send(('Page not found' + hsep).encode())

    # Close the connection
    connection.close()

def handle_method(client_socket):
    # Read the request from the client
    request = client_socket.recv(1024).decode()

    # Extract the method, path, and headers from the request
    method, path, headers = parse_request(request)

    # Send a response back to the client
    if method == "GET" and path == "/":
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, world!"
    else:
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot Found"

    client_socket.send(response.encode())
    client_socket.close()


def parse_request(request):
    lines = request.split("\r\n")
    method, path, version = lines[0].split()
    headers = {}
    for line in lines[1:]:
        if line:
            key, value = line.split(": ")
            headers[key] = value
    return method, path, headers

def parse_form_data(request):
    # Extract the method and URI path
    method, path = parse_http(request)

    # Check if the method is POST
    if method != 'POST':
        return None

    # Split the request into headers and body
    headers, body = request.decode().split(hsep+hsep, 1)

    # Parse the form data
    data = {}
    for field in body.split(hsep):
        if '=' in field:
            key, value = field.split('=', 1)
            data[key] = value

    # Convert the form data to JSON format
    json_data = {
        'name': data.get('name'),
        'gender': data.get('gender'),
        'birthyear': data.get('birthyear'),
        'birthplace': data.get('birthplace'),
        'residence': data.get('residence'),
        'job': data.get('job'),
        'pets': data.getlist('pets[]'),
        'message': data.get('message'),
        'question': {k: int(v) for k, v in data.items() if k.startswith('question[')}
    }

    return json_data