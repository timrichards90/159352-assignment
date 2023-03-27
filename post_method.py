"""
159.352 demo code sample

A solution to #5 of Exercises 2 - dealing with POST requests

Instructions:

1 - make sure form0.html and form1.html reside in the same directory as this
program file

2 - in both form files, set the "action" attribute of the <form> tag
to "/postie"

3 - start this server program from PyCharm or by command line

4 - in a browser enter the URI localhost:8080/form0.

5 - fill out the form data and press the "Submit" or "Send" button. What do
you see on the server side? Where is the "payload"?

Repeat steps 4-5 with /form1

Note: when running this several times, do not use the reload/refresh button,
rather type the URI into the input field above the toolbar and press return

-- Ian Bond 26/3/2023

"""

import os
import socket
import _thread

hsep = '\r\n'


# Here define some convenience functions

def parse_http(request):
    """Partial solution to Ex. 2. This extracts just the method and URI path
    ignoring everything else"""
    reqline = request.decode().split(hsep).pop(0)
    cmd, path, prot = reqline.split()
    return cmd, path


# Some convenience functions for writing and sending the status line
def http_sts(conn, status):
    """Write and send a status line"""
    conn.send(('HTTP/1.1 ' + status + hsep).encode())


def deliver_200(conn):
    http_sts(conn, '200 OK')


def deliver_404(conn):
    http_sts(conn, '404 Not found')


def http_hdr(conn, hdrline):
    """Send the hdrline input as Python string instance"""
    conn.send((hdrline + hsep).encode())


def http_bdy(conn, payload):
    """Send payload given as byte string"""
    conn.send(hsep.encode())
    conn.send(payload)


def gobble_file(filename, binary=False):
    """General utility to read entire content of file that could be binary"""
    if binary:
        mode = 'rb'
    else:
        mode = 'r'
    with open(filename, mode) as fin:
        content = fin.read()
    return content


def deliver_html(conn, filename):
    """Deliver content of HTML file"""
    content = gobble_file(filename)
    http_hdr(conn, 'Content-Type: text/html; charset=utf-8')
    http_bdy(conn, content.encode())


def deliver_jpeg(conn, filename):
    """Deliver content of JPEG image file"""
    content = gobble_file(filename, binary=True)
    http_hdr(conn, 'Content-Type: image/jpeg')
    http_hdr(conn, 'Accept-Ranges: bytes')
    http_bdy(conn, content)


# request handler
def do_request(connectionSocket):
    # Extract just the HTTP command (method) and path from the request
    request = connectionSocket.recv(1024)
    cmd, path = parse_http(request)
    print(cmd, path)

    # Only allow these method/path combinations
    if cmd == 'GET' and path == '/form':
        deliver_200(connectionSocket)
        deliver_html(connectionSocket, 'form.html')

    elif cmd == 'GET' and path == '/form1':
        deliver_200(connectionSocket)
        deliver_html(connectionSocket, 'form1.html')

    elif cmd == 'POST' and path == '/postie':
        print('Got a POST request. Here are all the lines')
        for line in request.decode().split(hsep):
            print('#', line)
        deliver_200(connectionSocket)

    # ... otherwise deliver "Not found" response
    else:
        deliver_404(connectionSocket)

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
    serverPort = 8000
    main(serverPort)

