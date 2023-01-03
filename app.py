
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
import glob
from multiprocessing import Process, Queue
import detect
app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/detect", methods=['POST'])
def detecte():
    if not request.method == "POST":
        return
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    print(video)
    result = subprocess.run(['python3', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename))],capture_output=True, text=True)
    print('------------')
    print('voici les resultats :',str(result.stdout))
    numfer= result.stdout.count('fertilized')
    numunfer = result.stdout.count('unfertilized')
    numfer=numfer-numunfer
    tot = numfer + numunfer
    
    
    print('Les stats:: ', numfer,numunfer,tot)

    # return os.path.join(uploads_dir, secure_filename(video.filename))
    obj = secure_filename(video.filename)
    #gg= max(glob.glob(os.path.join("/runs/detect", '*/')), key=os.path.getmtime)
    directory = 'static'
    gg= max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)
    print(gg)
    gb=os.path.join(gg, obj)
    gb=[gb,numfer,numunfer,tot]
    
    

   # print('NUMBER OF FERTILIZED EGGS: ', A)   

    return gb

@app.route("/opencam", methods=['GET'])
def opencam():
    print("here")
    subprocess.run(['python3', 'detect.py', '--source', '0'])
    return "done"

    

@app.route('/return-files', methods=['GET'])
def return_file():
    obj = request.args.get('obj')
    loc = os.path.join("runs/detect", obj)
    print(loc)
    try:
        return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
        #return send_from_directory(loc, obj)
    except Exception as e:
        return str(e)
    
if __name__ == "__main__":
    app.run()


# @app.route('/display/<filename>')
# def display_video(filename):
# 	#print('display_video filename: ' + filename)
# 	return redirect(url_for('static/video_1.mp4', code=200))