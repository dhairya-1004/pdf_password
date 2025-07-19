from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfReader, PdfWriter
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Loads your frontend page

@app.route('/protect_pdf', methods=['POST'])
def protect_pdf():
    file = request.files.get('file')
    password = request.form.get('password')
    file_name = request.form.get('filename')

    if not all([file, password, file_name]):
        return {'error': 'Please provide all inputs!'}, 400

    # Ensure filename ends with .pdf
    if not file_name.endswith('.pdf'):
        file_name += '.pdf'

    # Save uploaded file temporarily
    input_path = 'temp_input.pdf'
    file.save(input_path)

    # Protect PDF
    writer = PdfWriter()
    reader = PdfReader(input_path)

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    # Output protected file
    output_path = 'protected_file.pdf'
    with open(output_path, 'wb') as f:
        writer.write(f)

    # Clean up temp file
    os.remove(input_path)

    # Send file for download
    return send_file(output_path, download_name=file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
