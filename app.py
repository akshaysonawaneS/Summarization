import os
from werkzeug.utils import secure_filename
from flask import *
from main import starter,main
from Regional import marathi

UPLOAD_FOLDER = os.path.abspath('uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "akshay"
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
radio_button = ""

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload():
    return render_template("upload_form.html")

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        radio_button = request.form["language"]
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        (summ,text1) = starter(f.filename, radio_button)
        return render_template("success.html", name=f.filename, sum=summ, tex=text1)

@app.route('/successText', methods = ['POST'])
def success1():
    if request.method == 'POST':
        text = request.form["texta"]
        radio_button = request.form["language"]
        if text == "":
            return "<h1>Enter the Text<h1>"

        if radio_button == "marathi":
            sum1 = marathi(text)
        elif radio_button == "english":
            sum1 = main(text)

        return render_template("successA.html", sum=sum1, tex=text)

@app.route('/text')
def text():
    return render_template("text.html")


@app.route('/apiFileUpload', methods=['POST'])
def apiUpload():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['file']

    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 402
        return resp

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        (summ, text1) = starter(file.filename)
        resp = jsonify({'Text' : text1, 'summuary': summ})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are pdf'})
        resp.status_code = 403
        return resp

if __name__ == '__main__':
    app.run(debug=True)

