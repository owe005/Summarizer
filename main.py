import io
import requests
import openai
import PyPDF2
import tiktoken
from config import API_KEY

def num_tokens_from_string(string: str, encoding_name: str):
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def calculate_parts(text: str, model_name: str) -> int:
    MAX_TOKENS = 4096
    total_tokens = num_tokens_from_string(text, model_name)
    num_parts = total_tokens // MAX_TOKENS
    if total_tokens % MAX_TOKENS > 0:
        num_parts += 1

    num_parts += 1 # Just incase.. (Better to have too many parts than too few)

    return num_parts

openai.api_key = API_KEY

def read_pdf_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    f = io.BytesIO(response.content)
    pdf_reader = PyPDF2.PdfReader(f)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    
    return text

def divide_text_into_parts(text, n_parts):
    total_length = len(text)
    part_length = total_length // n_parts
    
    return [text[i*part_length: (i+1)*part_length] for i in range(n_parts)]

def get_summary(text_part):
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": "You are now the Summarizer. Your job is to summarize texts. Be specific and try to give concrete examples. Summarize the following text: "},
                                            {"role": "user", "content": text_part}])
    return response["choices"][0]["message"]["content"]

'''def combine_summaries(summaries_list):
    joined_summaries = ' '.join(summaries_list)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": "You are now the Combine Summarizer. Your job is to combine different summaries into one big summary. It is preferable if the summary is specific and not too general."},
                                            {"role": "user", "content": joined_summaries}])
    return response["choices"][0]["message"]["content"]'''

def extract_text_from_pdf(pdf):
    text = ""

    with open(pdf, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
            
    return text
