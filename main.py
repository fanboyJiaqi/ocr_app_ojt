from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

from config import get_logger

logger = get_logger()

app = Flask(__name__)

# Thư mục lưu file được mount volume
# UPLOAD_FOLDER = '/app/uploads'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tải mô hình OCR từ Hugging Face
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

# Đảm bảo thư mục tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('files')
    ocr_results = []  # Danh sách để lưu kết quả OCR
    
    for file in files:
        if file.filename == '':
            return 'No selected file'
        
        if file:
            # Lưu file vào thư mục static/uploads
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Mở file ảnh và thực hiện OCR
            image = Image.open(file_path).convert('RGB')
            pixel_values = processor(images=image, return_tensors="pt").pixel_values
            generated_ids = model.generate(pixel_values)
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # Lưu tên file và text vào danh sách ocr_results
            ocr_results.append({
                'filename': file.filename,
                'text': generated_text
            })
    
    # Render template với kết quả OCR
    return render_template('result.html', ocr_results=ocr_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
