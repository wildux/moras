import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import MORAS as vc
from werkzeug import secure_filename
from time import strftime
import cv2
app = Flask(__name__)

imgPath = 'static/scene.jpg'
imgRobotPath = 'static/uni.jpg'
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/update")
def update():
    return render_template('upload.html')

@app.route('/send', methods=['POST'])
def send():    
    #print(request.form['x1'],request.form['x2'],request.form['y1'],request.form['y2'])
    x1 = int(request.form['x1'])
    x2 = int(request.form['x2'])
    y1 = int(request.form['y1'])
    y2 = int(request.form['y2'])
    
    height = int(request.form['height'])
    width = int(request.form['width'])

    img = cv2.imread(imgPath)
    h,w,_ = img.shape
    
    scale_h = h/height
    scale_w = w/width

    x1 = int(x1*scale_w)
    x2 = int(x2*scale_w)
    y1 = int(y1*scale_h)
    y2 = int(y2*scale_h)

    img = img[y1:y2, x1:x2]
    imgRobot = cv2.imread(imgRobotPath)

    imgRes, x, y = vc.getResult(img, imgRobot, vc._SIFT)

    resultPath = "static/" + strftime("%Y-%m-%d-%H:%M") + ".png" 
    cv2.imwrite(resultPath, imgRes)

    return render_template('result.html', x=x, y=y, image=resultPath)

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():    
    file = request.files['file']
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        ext = filename.rsplit('.', 1)[1]
        filename = "scene." + ext
        #filename = secure_filename(file.filename)
        # Move the file form the temporal folder to the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file', filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
