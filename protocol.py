"""
PROTOKOL (text, 1 baris per pesan, diakhiri '\n')

Client -> Broker  :  REQ <app_id> <data>
Broker -> Worker  :  REQ <app_id> <data>
Worker -> Broker  :  RES <server_id> <app_id> <hasil>
Broker -> Client  :  RES <server_id> <app_id> <hasil>
Error             :  ERR <pesan>

Application ID:
  1 = LONG  (perhitungan kompleks, disimulasikan)
  2 = SHORT (echo / perhitungan sederhana)
"""

HOST = "127.0.0.1"
BROKER_PORT = 5000
WORKER_PORTS = {1: 6001, 2: 6002, 3: 6003}   # server_id -> port
APPS = {1: "LONG", 2: "SHORT"}


def recv_line(conn):
    """Baca satu baris (sampai '\\n') dari socket."""
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()


def send_line(conn, text):
    conn.sendall((text + "\n").encode())
