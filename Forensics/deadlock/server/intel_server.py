import socket
import threading

# Connection settings
HOST = "0.0.0.0"
PORT = 31337

FLAG1 = "ransomware"
FLAG2 = "deadlock"
FLAG3 = "2025-06-27 15:45:06 UTC"
FLAG4 = "52.111.243.30"
FLAG5 = "Netherlands"
CONNECTION_TIMEOUT = 30

BANNER = """
╔══════════════════════════════════════════════════════════════════════╗
║           ██████╗ ███████╗ █████╗ ██████╗ ██╗                       ║
║          ██╔═══██╗██╔════╝██╔══██╗██╔══██╗██║                       ║
║          ██║   ██║█████╗  ███████║██████╔╝██║                       ║
║          ██║   ██║██╔══╝  ██╔══██║██╔══██╗██║                       ║
║          ╚██████╔╝███████╗██║  ██║██║  ██║███████╗                  ║
║           ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝                  ║
║                                                                      ║
║        ▓▓▓▓▓▓  OPERATION  D E A D L O C K  ▓▓▓▓▓▓                    ║
║                                                                      ║
║   THREAT INTELLIGENCE TERMINAL — CLASSIFIED ACCESS                  ║
║                                                                      ║
║  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   ║
║  ⚠️  LKS IS NOT JUST A COMPETITION — IT IS A MINDSET ⚠️             ║
║  LOGIC • DISCIPLINE • INTEGRITY • CYBER RESILIENCE                 ║
║  YOU ARE NOT PLAYING — YOU ARE BEING TESTED                         ║
║  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   ║
╚══════════════════════════════════════════════════════════════════════╝

Jawab semua pertanyaan berurutan.
"""

QUESTIONS = [
    ("Q1. Jenis malware ini?\n> ", FLAG1, True),
    ("Benar.\nQ2. Termasuk family ransomware apa?\n> ", FLAG2, True),
    ("Benar.\nQ3. Kapan ransomware ini dibuat? (UTC)\n> ", FLAG3, False),
    ("Benar.\nQ4. Alamat IP C2 penyerang?\n> ", FLAG4, False),
    ("Benar.\nQ5. Threat actor berasal dari negara?\n> ", FLAG5, False),
]


def recv_line(conn):
    """
    Receive a line as str, return None on disconnect, timeout, or invalid bytes.
    """
    data = bytearray()
    while True:
        try:
            chunk = conn.recv(1)
        except socket.timeout:
            return None
        if not chunk:
            return None
        if chunk == b"\n":
            break
        data.extend(chunk)
    try:
        return data.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return None


def ask_questions(conn):
    for prompt, expected_answer, lower in QUESTIONS:
        conn.sendall(prompt.encode("utf-8"))
        answer = recv_line(conn)
        if answer is None:
            return False
        answer = answer.strip()
        if lower:
            answer = answer.lower()
        if answer != expected_answer:
            return False
    return True


def handler(conn, addr):
    try:
        conn.settimeout(CONNECTION_TIMEOUT)
        conn.sendall(BANNER.encode("utf-8"))

        if ask_questions(conn):
            conn.sendall(b"\nSEMUA BENAR!\nFLAG{DEADLOCK_INTEL_COMPLETE}\n")
        else:
            conn.sendall(b"Salah. Koneksi ditutup.\n")
    finally:
        conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        while True:
            try:
                conn, addr = server.accept()
            except OSError:
                # Keep server alive on transient errors.
                continue
            threading.Thread(target=handler, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
