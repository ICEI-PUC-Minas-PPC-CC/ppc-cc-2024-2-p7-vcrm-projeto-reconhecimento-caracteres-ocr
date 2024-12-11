import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFileDialog, QComboBox, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document
from pdf2image import convert_from_path

URL_API = "http://127.0.0.1:5000/ocr"

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Aplicativo OCR')
        self.setGeometry(100, 100, 700, 500)
        self.input_mode = None

        self.set_palette()

        self.layout = QVBoxLayout()

        self.init_ui()

        self.setLayout(self.layout)

    def set_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#11091a"))
        palette.setColor(QPalette.WindowText, QColor("#e8d18e"))
        palette.setColor(QPalette.Button, QColor("#626970"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.Base, QColor("#626970"))
        palette.setColor(QPalette.Highlight, QColor("#e8d18e"))
        self.setPalette(palette)

    def init_ui(self):
        title_label = QLabel('Selecione a entrada para conversão OCR')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #e8d18e;')
        self.layout.addWidget(title_label)

        input_layout = QHBoxLayout()
        self.input_path = QLineEdit(self)
        self.input_path.setReadOnly(True)
        select_input_btn = QPushButton('Selecionar Entrada', self)
        select_input_btn.clicked.connect(self.select_input)
        select_input_btn.setStyleSheet("background-color: #626970; color: white; padding: 10px 20px; border-radius: 8px;")
        input_layout.addWidget(QLabel('Entrada:'))
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(select_input_btn)
        self.layout.addLayout(input_layout)

        output_layout = QHBoxLayout()
        self.output_folder = QLineEdit(self)
        self.output_folder.setReadOnly(True)
        select_output_btn = QPushButton('Selecionar Pasta de Saída', self)
        select_output_btn.clicked.connect(self.select_output_folder)
        select_output_btn.setStyleSheet("background-color: #626970; color: white; padding: 10px 20px; border-radius: 8px;")
        output_layout.addWidget(QLabel('Pasta de Saída:'))
        output_layout.addWidget(self.output_folder)
        output_layout.addWidget(select_output_btn)
        self.layout.addLayout(output_layout)

        output_format_layout = QHBoxLayout()
        self.output_format_combobox = QComboBox(self)
        self.output_format_combobox.addItems(['txt', 'pdf', 'docx', 'html'])
        output_format_layout.addWidget(QLabel('Formato de Saída:'))
        output_format_layout.addWidget(self.output_format_combobox)
        self.layout.addLayout(output_format_layout)

        run_btn = QPushButton('Executar OCR', self)
        run_btn.setFont(QFont("Arial", 18))
        run_btn.setStyleSheet("background-color: #626970; color: white; padding: 10px 20px; border-radius: 8px;")
        run_btn.clicked.connect(self.perform_ocr)
        self.layout.addWidget(run_btn)

    def select_input(self):
        input_type, ok = QInputDialog.getItem(
            self, 
            "Selecionar Entrada", 
            "Deseja selecionar um arquivo ou uma pasta?",
            ["Arquivo", "Pasta"], 
            0, False
        )

        if ok:
            if input_type == "Arquivo":
                file_path, _ = QFileDialog.getOpenFileName(self, 'Selecionar Arquivo', '', 'Todos os Arquivos (*)')
                if file_path:
                    self.input_path.setText(file_path)
                    self.input_mode = "file"
            elif input_type == "Pasta":
                folder_path = QFileDialog.getExistingDirectory(self, 'Selecionar Pasta de Imagens')
                if folder_path:
                    self.input_path.setText(folder_path)
                    self.input_mode = "folder"

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Selecionar Pasta de Saída')
        if folder_path:
            self.output_folder.setText(folder_path)

    def perform_ocr(self):
        input_path = self.input_path.text()
        output_dir = self.output_folder.text()
        output_format = self.output_format_combobox.currentText()

        if not input_path or not output_dir or not self.input_mode:
            QMessageBox.critical(self, "Erro", "Selecione a entrada e a pasta de saída.")
            return

        try:
            results = []

            if self.input_mode == "file":
                if input_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                    results.append(self.process_image(input_path))
                elif input_path.lower().endswith('.pdf'):
                    results.extend(self.process_pdf(input_path))

            elif self.input_mode == "folder":
                for root, _, files in os.walk(input_path):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                            results.append(self.process_image(file_path))

            self.save_output(results, output_dir, output_format)
            QMessageBox.information(self, "Sucesso", f"Saída gerada em {output_dir}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def process_image(self, image_path):
        with open(image_path, "rb") as img_file:
            response = requests.post(URL_API, files={"image": img_file})
        response.raise_for_status()
        result = response.json()
        return self.extract_text(result)

    def process_pdf(self, pdf_path):
        images = convert_from_path(pdf_path)
        results = []
        for i, image in enumerate(images):
            temp_path = f"temp_page_{i}.jpg"
            image.save(temp_path, "JPEG")
            results.append(self.process_image(temp_path))
            os.remove(temp_path)
        return results

    def extract_text(self, result):
        text = ""
        for line in result.get("recognized_text", []):
            if isinstance(line, dict) and 'text' in line:
                text += line['text'] + "\n"
        return text.strip()

    def save_pdf(self, text, output_file):
        c = canvas.Canvas(output_file, pagesize=letter)
        width, height = letter
        margin = 40
        c.setFont("Helvetica", 10)
        y_position = height - margin
        line_height = 12
        max_line_width = width - 2 * margin

        lines = text.split("\n")

        for line in lines:
            words = line.split()
            current_line = ""

            while words:
                if y_position <= margin:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y_position = height - margin

                while words and c.stringWidth(current_line + words[0] + " ", "Helvetica", 10) < max_line_width:
                    current_line += words.pop(0) + " "

                c.drawString(margin, y_position, current_line.strip())
                y_position -= line_height
                current_line = ""

                if not words:
                    y_position -= line_height

        c.save()

    def save_output(self, results, output_dir, output_format):
        combined_text = "\n\n".join([result for result in results if result.strip()])
        output_file = os.path.join(output_dir, f"output.{output_format}")

        if output_format == "txt":
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(combined_text)
        elif output_format == "pdf":
            self.save_pdf(combined_text, output_file)
        elif output_format == "docx":
            doc = Document()
            doc.add_paragraph(combined_text)
            doc.save(output_file)
        elif output_format == "html":
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"<pre>{combined_text}</pre>")
        else:
            raise ValueError("Formato de saída não suportado.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec_())
