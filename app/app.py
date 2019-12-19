from flask import Flask,request, render_template
 
UPLOAD_DIR = "/Users/louis/product/data"
 
app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def index() :
  if request.method == 'POST' :
    f = request.files['file1']
    f.save(UPLOAD_DIR + f.filename)
    return render_template('index.html', message='Uploaded ' + UPLOAD_DIR + f.filename)
  else :
    return render_template('index.html', message="")

if __name__ == '__main__':
    app.run(port=8000, debug=True)