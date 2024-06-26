import re

class Router:
    def __init__(self):
        self.routes = []
        self.NotFound = b"HTTP/1.1 404 Not Found\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\nContent-Length: 14\r\n\r\nno route exist"
        pass

    def add_route(self, http_method: str, path: str, on_route):
        regex = r"^{}".format(path)
        for item in self.routes:
            if item["pattern"] == regex:
                item[http_method] = on_route
                return
        self.routes.append({"pattern": path, http_method: on_route})

    def route_request(self, request) -> bytes:
        for item in self.routes:
            if (
                re.match(item["pattern"], request.path) != None
                and request.method in item
            ):
                return item[request.method](request)
        return self.NotFound
