import socket
import sys

def connect_err(msg):
    raise Exception("error connecting - "+ msg)

def request_site(domain, port):
    if len(domain) == 0:
        raise connect_err("empty domain")
    
    cur_sock = socket.socket()
    
    cur_sock.connect((domain, port))
    
    req = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
    print("requesting")
    cur_sock.sendall(req.encode("ISO-8859-1"));
   
    while (resp := cur_sock.recv(4096)):
        print(resp.decode("ISO-8859-1"))
    cur_sock.close()
    

def main():
    port = 80
    if (len(sys.argv) > 2):
        port = int(sys.argv[2])
    elif len(sys.argv) == 1:
        raise ValueError("Website needed!")
    site = sys.argv[1]

    print(port)
    print(site)
    request_site(site, port)


if __name__ == "__main__":
        main()

