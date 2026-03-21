import socket

MAX_REQUEST_LINE = 2048  # request line length limit

def safe_handle_client(conn):
    try:
        data = conn.recv(4096)

        # length check
        if len(data) > MAX_REQUEST_LINE:
            conn.sendall(b"HTTP/1.1 414 Request-URI Too Long\r\n\r\n")
            return

        # parse request line
        try:
            request_line = data.split(b"\r\n")[0]
            method, path, version = request_line.split(b" ")
        except ValueError:
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            return

        # method validation
        if method not in [b"GET", b"POST"]:
            conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            return

        # path length limit (key protection)
        if len(path) > 1024:
            conn.sendall(b"HTTP/1.1 414 Request-URI Too Long\r\n\r\n")
            return

        # filter null bytes
        if b"\x00" in path:
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            return

        # valid request
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\nHello")

    finally:
        conn.close()


def start_server(host="0.0.0.0", port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(5)

        print(f"Listening on {host}:{port}")

        while True:
            conn, _ = server.accept()
            safe_handle_client(conn)


if __name__ == "__main__":
    start_server()
