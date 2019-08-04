#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define SOCK_RAW 3
#define SOCK_RDM 4
#define SOCK_SEQPACKET 5
#coding:utf-8

import socket
import threading
import errno

EOL1 = b"\n\n"
EOL2 = b"\n\r\n"
body = "Hello world"
response_params = [
    "HTTP/1.0 200 OK",
    "Date:Sun ,27 may 2018 01:01:01 GMT",
    "Content-Type:text/plain;charset=utf-8",
    "Content-Length:{}\r\n".format(len(body.encode())),
    body,
]

response = "\r\n".join(response_params)


def handle_connection(conn, addr):
    print("oh,new conn",conn,addr)
    import time
    time.sleep(10)
    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
    print(request)
    conn.send(response.encode())
    conn.close()

def main():
    serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,0)
    serversocket.bind(("127.0.0.1",8000))
    serversocket.listen(5)
    print("http://127.0.0.1:8000")
    try:
        i=0
        while True:
            try:
                conn,address=serversocket.accept()
                handle_connection(conn,address)
            except socket.error as e:
                if e.args[0] != errno.EAGAIN:
                    raise
                continue
            i+=1
            print(i)
            t=threading.Thread(target=handle_connection,args=(conn,address),name="thread-%s"%i)
            t.start()
    finally:
        serversocket.close()

if __name__ == '__main__':
    main()






