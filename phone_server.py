"""
phone_server.py  (OPTIONAL feature)
Shows saved drawings in a web page that a phone on the SAME Wi-Fi can open.
No internet is needed. Works only if Flask and qrcode are installed.
"""
import os
import socket
import threading

import config


def get_local_ip():
    """Find this laptop's Wi-Fi address (nothing is actually sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def start_server(port=5000):
    """Start the web server in a background thread. Returns the URL."""
    from flask import Flask, render_template_string, send_from_directory

    app = Flask(__name__)
    page = """
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Drawings</title></head>
    <body style="font-family:Arial;background:#222;color:white;text-align:center">
    <h2>AI Virtual Drawing Board - Saved Drawings</h2>
    {% if files %}
      {% for f in files %}
        <p>{{ f }}<br><img src="/drawings/{{ f }}" style="max-width:95%;border:2px solid white"></p>
      {% endfor %}
    {% else %}<p>No drawings saved yet.</p>{% endif %}
    </body></html>
    """

    @app.route("/")
    def index():
        os.makedirs(config.DRAWINGS_DIR, exist_ok=True)
        files = sorted((f for f in os.listdir(config.DRAWINGS_DIR)
                        if f.lower().endswith(".png")), reverse=True)
        return render_template_string(page, files=files)

    @app.route("/drawings/<path:name>")
    def drawing(name):
        return send_from_directory(config.DRAWINGS_DIR, name)

    thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False),
        daemon=True)
    thread.start()
    return f"http://{get_local_ip()}:{port}"


def make_qr(url, path):
    """Save a QR code image of the URL."""
    import qrcode
    qrcode.make(url).save(path)
