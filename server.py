import socketserver
from routes.auth import add_auth_routes
from routes.chat import add_chat_routes
from routes.static import add_static_routes
from util.request import Request


from util.router import Router


class MyTCPHandler(socketserver.BaseRequestHandler):
    router = Router()
    add_static_routes(router)
    add_chat_routes(router)
    add_auth_routes(router)

    def handle(self):

        received_data = self.request.recv(2048)
        # print(self.client_address)
        # print("--- received data ---")
        # print(received_data)
        # print("--- end of data ---\n\n")
        request = Request(received_data)
        res = self.router.route_request(request)
        self.request.sendall(res)


def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    server.serve_forever()


if __name__ == "__main__":
    main()
