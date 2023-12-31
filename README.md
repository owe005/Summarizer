# PDF Summarizer

## Description

This project provides a service that allows users to upload a PDF document, and receive a concise summary generated by ChatGPT3.5 Turbo.

## Directory Structure

```
.
|-- main.py
|-- app.py
|-- /templates
|   |-- index.html
|-- /static
|   |-- /css
|   |   |-- style.css
|   |-- /js
|   |   |-- script.js
|-- /temp (Used for temporarily storing uploaded files)
```
> Note: The `config.py` file, which contains the API key, is not included, duh..

## Setup and Installation

1. Clone the repository.

2. Install the required packages.

3. Create a `config.py` file in the root directory and add your openAI API key:

6. Start the application.

   ```bash
   python app.py
   ```

## Usage

1. Navigate to the provided link (typically `http://127.0.0.1:5000/`).
2. Upload a PDF document using the file input or provide a PDF URL.
3. Click on "Summarize" and wait for the process to complete.
4. Once done, you will receive a concise summary of your document.

Keep in mind that currently, the maximum token limit for this is 4096 tokens, but since this splits the pdf into three equal parts, the size limit should be 4096*3 = 12288 tokens. It is possible to work with larger pdfs but the code in `app.py` specifically: 

```text_parts = divide_text_into_parts(text, 3)```

You then change the "3" to a larger number, but it will increase the time it takes to get a summary.

Edit: With the newly added "Advanced mode" the token limit is now limitless, it'll just take a very long time.
