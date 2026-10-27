import http.server
import socketserver
import urllib.request
import threading
import sys
import subprocess

def get_wsl_ip():
    try:
        out = subprocess.check_output(["wsl", "-d", "Ubuntu", "hostname", "-I"], text=True)
        return out.strip().split()[0]
    except Exception:
        return "172.21.167.203"

WSL_IP = get_wsl_ip()
print(f"Targeting WSL IP for NodePorts: {WSL_IP}")

def make_proxy_handler(target_port):
    target_host = WSL_IP
    class ProxyHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.forward_request("GET")

        def do_POST(self):
            self.forward_request("POST")

        def do_DELETE(self):
            self.forward_request("DELETE")

        def forward_request(self, method):
            target_url = f"http://{target_host}:{target_port}{self.path}"
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len) if content_len > 0 else None

            headers = {k: v for k, v in self.headers.items() if k.lower() not in ['host', 'content-length']}

            req = urllib.request.Request(target_url, data=body, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=5) as res:
                    self.send_response(res.status)
                    for k, v in res.getheaders():
                        if k.lower() != 'transfer-encoding':
                            self.send_header(k, v)
                    self.end_headers()
                    self.wfile.write(res.read())
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                for k, v in e.headers.items():
                    if k.lower() != 'transfer-encoding':
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(f"Proxy Error: {e}".encode())

        def log_message(self, format, *args):
            pass # quiet logging

    return ProxyHandler

def start_server(local_port, target_nodeport):
    socketserver.TCPServer.allow_reuse_address = True
    handler = make_proxy_handler(target_nodeport)
    with socketserver.TCPServer(("0.0.0.0", local_port), handler) as httpd:
        print(f"Gateway listening on http://localhost:{local_port} -> NodePort {target_nodeport}")
        httpd.serve_forever()

if __name__ == "__main__":
    t1 = threading.Thread(target=start_server, args=(8081, 30081), daemon=True)
    t2 = threading.Thread(target=start_server, args=(8082, 30082), daemon=True)
    t3 = threading.Thread(target=start_server, args=(8083, 30083), daemon=True)
    t1.start()
    t2.start()
    t3.start()

    print("Kubernetes Localhost Gateway Active: Ports 8081, 8082, 8083")
    while True:
        import time
        time.sleep(1)
