import socket
import sys

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            print(f"Port {port} is FREE")
            return True
        except OSError:
            print(f"Port {port} is BUSY")
            return False

if __name__ == "__main__":
    check_port(8001)
