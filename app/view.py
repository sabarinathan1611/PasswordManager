from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
view = Blueprint('view', __name__)


@view.route('/',methods=['POST','GET'])
def home():
    return render_template('index.html')