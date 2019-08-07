from flask import Flask, render_template, request,Response,make_response,send_from_directory
from werkzeug.utils import secure_filename

import choice
import asyncio
import os
import re
import IPy
from logging.config import dictConfig

basepath = os.path.dirname(__file__)
resultfile = os.path.join(basepath, 'result_file')


#日志配置
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

#上传文件页面
@app.route('/upload')
def show_upload_file():
    return render_template('upload.html')


#上传文件到指定文件夹
@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(basepath, 'upload_file', secure_filename(f.filename))
        upload_path = os.path.abspath(upload_path) # 将路径转换为绝对路径
        f.save(upload_path)
        #app.logger.info
        #return redirect(url_for('upload'))
        #return render_template('upload.html')
        return 'file uploaded successfully'


#文本框页面
@app.route('/ip')
def show_IP_file():
    return render_template('ip.html')

#单IP查询
@app.route('/ip=<IP>',methods=['get'])
def singleip(IP):
    single_ip=choice.choice
    return single_ip.Sing_RequestQQGJ(IP)


#文件批量查询
@app.route('/file=<file>',methods=['get'])
def filechaxun(file):
        file_chaxun = choice.choice
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(file_chaxun.OpenFile(file))
        loop.run_until_complete(future)
        return 'ok'
        loop.close()


#下载结果文件
@app.route('/<file>', methods=['GET'])
def return_file(file):
    filename = file
    directory = resultfile
    response = make_response(send_from_directory(directory, file, as_attachment=True))
    return response
'''
#打印结果目录的文件
@app.route('/')
def get_filename():
    for root, dirs, files in os.walk(resultfile):
        for file in files:
            print(file)
        return file
'''



if __name__ == '__main__':
    app.run(debug=False, threaded=True)