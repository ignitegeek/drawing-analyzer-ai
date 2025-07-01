from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from datetime import datetime
from utils.analyze_drawing import analyze_drawing

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ANNOTATED_FOLDER'] = 'static/annotated/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ANNOTATED_FOLDER'], exist_ok=True)

IS_PAID_MODE = False

@app.route('/')
def index():
    return render_template('index.html', is_paid=IS_PAID_MODE)

@app.route('/upload', methods=['POST'])
def upload():
    global IS_PAID_MODE
    if 'drawing' not in request.files:
        return "No file uploaded"
    file = request.files['drawing']
    if file.filename == '':
        return "No selected file"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"drawing_{timestamp}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    annotated_path, report_text = analyze_drawing(filepath, app.config['ANNOTATED_FOLDER'])

    return render_template('result.html',
                           original=url_for('static', filename='uploads/' + filename),
                           annotated=url_for('static', filename='annotated/' + os.path.basename(annotated_path)),
                           report=report_text,
                           is_paid=IS_PAID_MODE)

@app.route('/admin/toggle')
def toggle_mode():
    global IS_PAID_MODE
    IS_PAID_MODE = not IS_PAID_MODE
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
