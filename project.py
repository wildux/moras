from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    print("I got it!")
    print(request.form['x1'],request.form['x2'],request.form['y1'],request.form['y2'])
    return render_template('result.html', x1=request.form['x1'])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
