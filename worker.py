"""Worker server. Jalankan: python worker.py <server_id>   (1, 2, atau 3)"""
import socket, sys, threading, time
from protocol import *


def handle(conn, server_id):
    with conn:
        msg = recv_line(conn)
        parts = msg.split(" ", 2)
        if len(parts) < 2 or parts[0] != "REQ" or not parts[1].isdigit() or int(parts[1]) not in APPS:
            send_line(conn, "ERR format/application id tidak valid")
            return
        app_id = int(parts[1])
        data = parts[2] if len(parts) > 2 else ""

        print(f"[Worker {server_id}] Terima request app={APPS[app_id]} data='{data}'")
        if app_id == 1:                      # LONG: simulasi perhitungan kompleks
            time.sleep(3)
            result = f"hasil komputasi kompleks untuk '{data}'"
        else:                                # SHORT: echo
            result = f"echo: {data}"
        send_line(conn, f"RES {server_id} {app_id} {result}")
        print(f"[Worker {server_id}] Selesai app={APPS[app_id]}")


def main():
    server_id = int(sys.argv[1])
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, WORKER_PORTS[server_id]))
    srv.listen()
    print(f"[Worker {server_id}] Berjalan di port {WORKER_PORTS[server_id]}")
    while True:
        conn, _ = srv.accept()
        threading.Thread(target=handle, args=(conn, server_id), daemon=True).start()


if __name__ == "__main__":
    main()
