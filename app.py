import os
from flask import *
from main import pdfExtractor
UPLOAD_FOLDER = '/home/Akshay/Projects/Python/Summurize/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload():
    return render_template("upload_form.html")

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        (summ,text1) = pdfExtractor(f.filename)
        return render_template("success.html", name=f.filename, sum=summ, tex=text1 )


if __name__ ==  '__main__':
    app.run()

