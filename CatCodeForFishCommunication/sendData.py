import socket
import tqdm
import os
import time


def sendD():
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096

    host = "192.168.0.11"

    port = 5003

    filename = "dataFromCat.txt"

    filesize = os.path.getsize(filename)

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"[+] Connecting to {host}:{port}")
    try:
        s.connect((host, port))
    except:
        return
    
    print("[+] Connected.")
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            
            try:
                s.sendall(bytes_read)
            except:
                break
            
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()


#while 1:
#    send()
#    time.sleep(1)

