import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import requests
from main import read_pdf_from_url, divide_text_into_parts, get_summary, combine_summaries, extract_text_from_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf-file' not in request.files:
        return jsonify({"error": "No file provided!"}), 400
    file = request.files['pdf-file']
    if file.filename == '':
        return jsonify({"error": "No file selected!"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join("", filename)
        file.save(filepath)
        text = extract_text_from_pdf(filepath)
        text_parts = divide_text_into_parts(text, 3)
        summaries = [get_summary(part) for part in text_parts]
        summary = combine_summaries(summaries)
        os.remove(filepath)  # Clean up the saved file
        return jsonify({"summary": summary})

@app.route('/summarize-url', methods=['POST'])
def summarize_url():
    url = request.form.get('pdf-url')
    if not url:
        return jsonify({"error": "No URL provided!"}), 400
    text = read_pdf_from_url(url)
    text_parts = divide_text_into_parts(text, 3)
    summaries = [get_summary(part) for part in text_parts]
    summary = combine_summaries(summaries)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)