import os
import time
import glob
from flask import Flask, redirect, render_template, request, send_file

# Configure Application
app = Flask(__name__)

global filename
global ftype

@app.route("/")
def home():

    # Delete old files
    filelist = glob.glob('uploads/*')
    for f in filelist:
        os.remove(f)
    filelist = glob.glob('downloads/*')
    for f in filelist:
        os.remove(f)
    return render_template("home.html")

app.config["FILE_UPLOADS"] = "/home/mayur/dev/EL/AA/Huffman_Coding/uploads"

@app.route("/compress", methods=["GET", "POST"])
def compress():

    if request.method == "GET":
        return render_template("compress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            # os.system('./c uploads/{}'.format(filename))
            os.system('./Encode uploads/{}'.format(filename))
            # filename = filename[:filename.index(".",1)]
            ftype = ".bin"
            while True:
                if 'uploads/{}.bin'.format(filename) in glob.glob('uploads/*.bin'):
                    os.system('mv uploads/{}.bin downloads/'.format(filename))
                    break
            print(filename, ftype)
            return render_template("compress.html", check=1)

        else:
            print("ERROR")
            return render_template("compress.html", check=-1)

@app.route("/decompress", methods=["GET", "POST"])
def decompress():

    if request.method == "GET":
        return render_template("decompress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            # os.system('./d uploads/{}'.format(filename))
            os.system('./Decode uploads/{}'.format(filename))
            # print("check")
            f = open('uploads/{}'.format(filename), 'rb')
            # ftype = ".txt.bin" + (f.read(int(f.read(1)))).decode("utf-8")
            # filename = filename[:filename.index("-",1)]
            ftype = ".txt"

            while True:
                if 'uploads/{}.txt'.format(filename) in glob.glob('uploads/*.bin.txt'):
                    os.system('mv uploads/{}{} downloads/'.format(filename, ftype))
                    break

            return render_template("decompress.html", check=1)

        else:
            print("ERROR")
            return render_template("decompress.html", check=-1)






@app.route("/download")
def download_file():
    global filename
    global ftype
    path = "downloads/" + filename + ftype
    return send_file(path, as_attachment=True)




# Restart application whenever changes are made
if __name__ == "__main__":
    app.run(port = 5001, debug = True)