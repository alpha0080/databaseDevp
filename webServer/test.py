# -*- coding: utf8 -*-


    

import os
import json
import sys


import datetime
import time
#import PIL
#from PIL import Image
from time import gmtime,strftime
#import psycopg2
#import collections
from shutil import copyfile

from flask import Flask, render_template, request

#from flask_dropzone import Dropzone
from flask import jsonify
#import moviepy.editor as mp

app = Flask(__name__)


#initial start
@app.route('/timeline')
def timeline():
   # return 'Hello World!'
    return render_template("timeline.html")

if __name__ == '__main__':
    app.run(debug=True,port=80)