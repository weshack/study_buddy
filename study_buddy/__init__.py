from flask import Flask
app = Flask(__name__)

print "Running app..."

from study_buddy.views import *