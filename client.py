"""Client. Jalankan: python client.py <app_id 1|2> <data>
Contoh: python client.py 2 halo   |   python client.py 1 hitung_pi
Tanpa argumen: mode interaktif."""
import socket, sys
from protocol import *


def kirim(app_id, data):
    with socket.create_connection((HOST, BROKER_PORT)) as s:
        send_line(s, f"REQ {app_id} {data}")
        print(f"[Client] Kirim  : REQ {app_id} {data}")
        print(f"[Client] Balasan: {recv_line(s)}")


if len(sys.argv) >= 3:
    kirim(sys.argv[1], " ".join(sys.argv[2:]))
else:
    while True:
        app = input("Application ID (1=Long, 2=Short, q=keluar): ").strip()
        if app == "q":
            break
        kirim(app, input("Data: "))
