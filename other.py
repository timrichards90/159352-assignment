# if cmd == 'GET':
#     sign_in_status = authenticate(connectionSocket, request)
#
#     if sign_in_status:
#         # If file exists, try and deliver
#         if os.path.exists(filename):
#             deliver_200(connectionSocket)
#
#             # Deliver according to filename extension type. So far only HTML and
#             # JPEG are supported
#             if ftype == 'html':
#                 deliver_html(connectionSocket, filename)
#             elif ftype == 'jpeg':
#                 deliver_jpeg(connectionSocket, filename)
#             else:
#                 deliver_404(connectionSocket)
#
#         # ... otherwise deliver "Not found" response
#         else:
#             deliver_404(connectionSocket)
#     else:
#         # if not authenticated do not serve the file
#         pass
import json

if __name__ == '__main__':
    q = 'question%5B1%5D'
    print(q.split("%5B")[1].split("%5D")[0])