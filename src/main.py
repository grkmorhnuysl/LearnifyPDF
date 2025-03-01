# Gerekli kütüphanelerin yüklenmesi 
!pip install openai PyPDF2 gradio

# Gerekli modüllerin içe aktarılması
from PyPDF2 import PdfReader
import gradio as gr
from openai import OpenAI

# OpenAI API istemcisi
api_key = "your-api-key"
client = OpenAI(api_key=api_key)

# PDF'den metin çıkarma fonksiyonu
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Metni belirli sayıda parçaya bölme fonksiyonu
def split_text_into_parts(text, parts):
    sentences = text.split('. ')
    chunk_size = len(sentences) // parts
    chunks = []

    for i in range(parts):
        start_idx = i * chunk_size
        if i == parts - 1:  # Son parça
            chunks.append('. '.join(sentences[start_idx:]))
        else:
            end_idx = (i + 1) * chunk_size
            chunks.append('. '.join(sentences[start_idx:end_idx]))
    
    return chunks

# Eğitimsel metin oluşturma fonksiyonu
def convert_to_educational_content(text_part, model="gpt-4o-mini"):
    try:
        prompt = f"""
        You are an expert in creating educational content. Transform the following content into a highly detailed and comprehensive educational text.

        Instructions:
        - Avoid using section titles such as "Conclusion".
        - Expand the content with thorough and detailed explanations.
        - Include real-world examples to illustrate key concepts.
        - Perform an in-depth examination of fundamental concepts, explaining their relevance with clarity.

        Content: {text_part}

        Educational Text:
        """
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional educational content creator."},
                {"role": "user", "content": prompt}
            ],
            model=model,
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error processing text part: {e}"

# Ana işlev
def process_pdf(pdf_file, class_length):
    # PDF'den metni çıkar
    raw_text = extract_text_from_pdf(pdf_file)
    
    # Bölüm sayısını belirle (30 dakika için 5, 60 dakika için 15)
    parts = 5 if class_length == "30 Minutes" else 15
    
    # Metni parçalarına ayır
    text_parts = split_text_into_parts(raw_text, parts)
    
    # Eğitimsel metinler oluştur ve birleştir
    educational_texts = []
    for i, part in enumerate(text_parts):
        print(f"Processing part {i + 1} of {parts}...")
        educational_text = convert_to_educational_content(part)
        educational_texts.append(educational_text)
    
    # Eğitimsel metinleri birleştir ve döndür
    final_text = "\n\n".join(educational_texts)
    return final_text

# Gradio uygulaması
with gr.Blocks() as demo:
    gr.Markdown("## Generative Educational Text Transformation")
    gr.Markdown(
        "Upload a PDF file, select the desired class duration (30 or 60 minutes), and the AI will generate a detailed educational text."
    )

    pdf_input = gr.File(label="Upload PDF", type="filepath")
    class_length = gr.Radio(
        ["30 Minutes", "60 Minutes"], label="Select Class Duration", value="30 Minutes"
    )
    output = gr.Textbox(label="Generated Educational Text", lines=30)

    generate_button = gr.Button("Generate Educational Text")
    generate_button.click(
        process_pdf,
        inputs=[pdf_input, class_length],
        outputs=output
    )

demo.launch()
