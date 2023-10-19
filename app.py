import os
from flask import Flask, request, jsonify, render_template
from main import divide_text_into_parts, get_summary, extract_text_from_pdf, num_tokens_from_string, calculate_parts
import uuid

app = Flask(__name__)

# Simple or Adanced mode
global AI_MODE

# Default to simple mode
AI_MODE = "simple"

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
        # Generate a unique filename using UUID
        unique_filename = str(uuid.uuid4()) + "." + file.filename.split('.')[-1]
        filepath = os.path.join("temp/", unique_filename)
        file.save(filepath)

        text = extract_text_from_pdf(filepath)
        n = calculate_parts(text, "gpt-3.5-turbo")
        text_parts = divide_text_into_parts(text, n)
        print(f"Number of parts: {n}, Number of tokens: {num_tokens_from_string(text, 'gpt-3.5-turbo')}")

        summaries = ""

        for part in text_parts:
            summaries += get_summary(part)
            print(f"Summarized! Tokens so far: {num_tokens_from_string(summaries, 'gpt-3.5-turbo')}")

        print(f"Getting ready to combine summaries...")

        # Unsure if I will keep this code, depends if it's needed.
        ''' while num_tokens_from_string(summaries, "gpt-3.5-turbo") > 4096:
            print(f"Summaries too long! Splitting into parts...")
            n = calculate_parts(summaries, "gpt-3.5-turbo")
            summaries_parts = divide_text_into_parts(summaries, n)
            summaries = ""

            for part in summaries_parts:
                summaries += get_summary(part)
                print(f"Summarized! Tokens so far: {num_tokens_from_string(summaries, 'gpt-3.5-turbo')}")

            if num_tokens_from_string(summaries, "gpt-3.5-turbo") > 4096:
                print(f"Summaries still too long! Trying again...")

            else:
                print(f"Summaries combined! Tokens: {num_tokens_from_string(summaries, 'gpt-3.5-turbo')}")
                break'''
        
        os.remove(filepath)  # Clean up the saved file

        if AI_MODE == "simple":
            print(f"Simple mode ON!")
            summary = get_summary(summaries)
            return jsonify({"summary": summary})

        elif AI_MODE == "advanced":
            print(f"Advanced mode ON!")
            return jsonify({"summary": summaries})

@app.route('/set-mode', methods=['POST'])
def set_mode():
    global AI_MODE  # Ensure we're modifying the global variable
    data = request.get_json()
    mode = data.get('mode', 'simple')  # Default to 'simple' if mode isn't provided
    
    if mode in ['simple', 'advanced']:
        AI_MODE = mode
        return jsonify({"message": f"Mode set to {AI_MODE}"})
    else:
        return jsonify({"error": "Invalid mode provided!"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)