import os,json



from settings import app
from flask import request,render_template,send_file


"""   home page   """
@app.route("/")
def home():
    return render_template("upload.html",title="upload",current_url = request.url)


"""  file upload  """
@app.route("/upload_datashak",methods=['POST'])
def file_upload():
    data = {}


    if request.method == "POST":
        """     getting multiple files    """
        file_list = request.files.getlist("datashak")

        if len(file_list) > 0:
            no_file = False
            upload_error = False

            for file in file_list:
                """   if file is empty   """
                if file.filename == '':
                    no_file = True
                    break
                #  otherwise
                else:
                    filename = file.filename

                    try:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    except Exception as e:
                        print str(e)
                        upload_error = True
                        break


            if no_file:
                data = {"status": "error", "message": "No File Selected"}
                return json.dumps(data)
            elif upload_error:
                data = {"status": "error", "message": "No File Selected"}
                return json.dumps(data)
            else:
                data = {"status": "success", "message": "File Successfully Uploaded"}
                return json.dumps(data)


        else:
            data = {"status": "error", "message": "Empty file list"}
            return json.dumps(data)


"""  file list  """
@app.route("/file_list",methods=['GET'])
def file_list():
    data = []
    if request.method == "GET":
        dir = 'datashak'
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
        data = {'status' : 'success','data' : files}
    else:
        data = {'status' : 'error','message' :'Invalid Request'}

    return json.dumps(data)

"""  delete file """
@app.route("/file_delete/<path:filename>",methods=['GET'])
def delete_file(filename):
    data = {}
    dir = "datashak"

    if request.method == "GET":
        file_name = filename

        try:
            if os.path.isfile(os.path.join(dir,file_name)):
                os.remove(os.path.join(dir,file_name))
                data = {"status" : "success","message" : "Successfully Deleted"}
            else:
                data = {"status" : "error","message" : "Invalid Data"}
        except Exception as e:
            print str(e)

    return json.dumps(data)



@app.route('/datashak/<path:path>')
def static_file(path): # SENDING STATIC FILE
    return send_file("./datashak/"+path,attachment_filename=path)


"""   500 handle   """
@app.errorhandler(500)
def Page_not_found():
    return "Hello There :D",5
