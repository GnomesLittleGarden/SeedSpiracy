from flask import Flask, request, redirect, send_file, abort
import datetime, os, csv

# Paths
CSV  = 'emails.csv'
PDF  = 'Seedspiracy_Field_Manual_v0.1.pdf'
HTML = 'index.html'

app = Flask(__name__)

def append_csv(email):
    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # Open in append mode, write a new row
    with open(CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([email, ts])

@app.route('/', methods=['GET'])
def form():
    if not os.path.exists(HTML):
        abort(404, description="Form HTML missing")
    return send_file(HTML)

@app.route('/collect', methods=['POST'])
def collect():
    email = request.form.get('email', '').strip()
    # basic sanity check
    if '@' not in email or len(email) < 5:
        return "Invalid email address.", 400

    append_csv(email)
    return redirect('/download')

@app.route('/download', methods=['GET'])
def download():
    if not os.path.exists(PDF):
        abort(404, description="PDF missing")
    return send_file(
      PDF,
      as_attachment=True,
      download_name='Field_Manual.pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
