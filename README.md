# PDF to Educational Text Converter

This project converts PDF documents into structured educational content using OpenAI's GPT model. 

## Features
- Extracts text from PDFs
- Converts text into detailed educational content
- Supports 30-minute and 60-minute class durations
- Provides real-world examples and deep insights

## Installation
```
pip install openai PyPDF2 gradio
```

## Usage
Run the main script:
```
python src/main.py
```

## Project Structure
```
📂 pdf-to-educational-text
│-- 📂 src                # Code files
│   ├── main.py          # Main Python script
│-- 📂 docs               # Documentation
│   ├── explanation.md   # Explanation of the project
│-- 📂 results            # Example output files
│   ├── 30_minutes_output.txt
│   ├── 60_minutes_output.txt
│-- 📂 assets             # Visuals and external links
│   ├── screenshot.png   # Interface screenshot
│   ├── hosted_link.txt  # Hosted link for the app
│-- README.md            # Project description
```

## License
This project is licensed under the MIT License.
