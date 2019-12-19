from flask import Flask,render_template

app = Flask(__name__)

@app.route('/',methods = ['POST'])
def send():
    if request.method == 'POST':
        res = request.files.getlist('log_file')
        save_path = os.path.join(UPLOAD_FOLDER,res.filename)
        res.save(save_path)
        return render_template('index.html',img_path=save_path)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
