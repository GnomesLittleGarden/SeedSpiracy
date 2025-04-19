from flask import Flask, request, send_from_directory, abort
import csv, re, os
from datetime import datetime
from pathlib import Path

PDF_NAME   = "Seedspiracy_Field_Manual_v0.1.pdf"
FILES_DIR  = Path(__file__).parent / "files"
CSV_PATH   = Path(__file__).parent / "emails.csv"
EMAIL_RX   = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.post("/download")
def capture_and_send():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()

    if not EMAIL_RX.fullmatch(email):
        abort(400, "Invalid e‑mail address")

    # append to CSV (timestamp, email, ip)
    CSV_PATH.touch(exist_ok=True)
    with CSV_PATH.open("a", newline="") as f:
      writer = csv.writer(f)
      writer.writerow([datetime.utcnow().isoformat(), email, request.remote_addr])

    # send the file back as attachment
    return send_from_directory(
        directory=FILES_DIR,
        path=PDF_NAME,
        as_attachment=True,
        download_name=PDF_NAME
    )


# ----  production entry‑point ----
if __name__ == "__main__":
    # dev server: python server.py
    app.run(debug=True, port=8000)
