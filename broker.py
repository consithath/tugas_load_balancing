"""
Broker (server utama).
Jalankan: python broker.py <mode>
  mode "least" -> pemerataan jumlah request yang sudah dilayani tiap worker
  mode "rr"    -> berurutan sesuai server-id berdasarkan counter broker
"""
import socket, sys, threading
from protocol import *

mode = "rr"
lock = threading.Lock()
rr_counter = 0                                  # counter milik broker (mode rr)
served = {sid: 0 for sid in WORKER_PORTS}       # jumlah request per worker (mode least)


def pilih_worker():
    global rr_counter
    with lock:
        if mode == "rr":
            sid = (rr_counter % len(WORKER_PORTS)) + 1
            rr_counter += 1
        else:
            sid = min(served, key=lambda s: (served[s], s))   # paling sedikit dilayani
        served[sid] += 1
        return sid


def handle(conn, addr):
    with conn:
        msg = recv_line(conn)
        print(f"[Broker] Dari client {addr[1]}: '{msg}'")
        parts = msg.split(" ", 2)
        if len(parts) < 2 or parts[0] != "REQ" or not parts[1].isdigit() or int(parts[1]) not in APPS:
            send_line(conn, "ERR format harus: REQ <app_id 1|2> <data>")
            return

        sid = pilih_worker()
        print(f"[Broker] Diteruskan ke Worker {sid} (mode={mode}) | total: {dict(served)}")
        try:
            with socket.create_connection((HOST, WORKER_PORTS[sid])) as w:
                send_line(w, msg)
                reply = recv_line(w)
        except OSError:
            reply = f"ERR worker {sid} tidak bisa dihubungi"
        send_line(conn, reply)
        print(f"[Broker] Balasan Worker {sid} diteruskan ke client {addr[1]}")


def main():
    global mode
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, BROKER_PORT))
    srv.listen()
    print(f"[Broker] Berjalan di port {BROKER_PORT}, mode={mode}")
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
