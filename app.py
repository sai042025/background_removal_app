from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from rembg import remove
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    upload_history = os.listdir(UPLOAD_FOLDER)
    upload_history.sort(reverse=True)
    return render_template('index.html', uploaded_file=None, processed_file=None, history=upload_history)

@app.route('/upload', methods=['POST'])
def upload_file(): 
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(PROCESSED_FOLDER, file.filename)
    print(f"📥 Saving uploaded file to: {input_path}")
    file.save(input_path)
    try:
         with open(input_path, 'rb') as i:
            input_image = i.read()
         output_image = remove(input_image)

         with open(output_path, 'wb') as o:
            o.write(output_image)
         print(f"✅ Processed image saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return f"Processing failed: {e}", 500

    upload_history = os.listdir(UPLOAD_FOLDER)
    upload_history.sort(reverse=True)

    return render_template(
        'index.html',
        uploaded_file=file.filename,
        processed_file=file.filename,
        history=upload_history
    )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render provides a PORT env variable
    app.run(host="0.0.0.0", port=port, debug=True)
