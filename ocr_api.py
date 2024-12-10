from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import os

ocr = PaddleOCR(use_angle_cls=True, lang='en')

app = Flask(__name__)

UPLOAD = 'uploads'
os.makedirs(UPLOAD, exist_ok=True)
app.config['UPLOAD'] = UPLOAD

@app.route('/ocr', methods=['POST'])
def ocr_api():
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem foi enviada."}), 400
    
    image = request.files.get('image')

    if image.filename == '':
        return jsonify({"error": "Nenhuma arquivo selecionado."}), 400

    image_path = os.path.join(app.config['UPLOAD'], image.filename)
    image.save(image_path)

    try:
        result = ocr.ocr(image_path, cls=True)
        
        os.remove(image_path)

        extracted_text = []
        for line in result[0]:
            text = line[1][0]
            confidence = line[1][1]
            extracted_text.append({"text": text, "confidence": confidence})

        return jsonify({"recognized_text": extracted_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API OCR está rodando"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)