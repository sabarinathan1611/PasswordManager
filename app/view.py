from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from . import db
from .models import User
from flask_login import login_required,current_user
from .sysinfo import *
view = Blueprint('view', __name__)


@view.route('/',methods=['POST','GET'])
@login_required
def home():
    return render_template('index.html')



    
@view.route('/admin',methods=['POST','GET'])
@login_required
def admin():
    
    if current_user.role == 'admin':
        system_info_printer = SystemInfoPrinter()
        storage_info= system_info_printer.print_storage_info()
        system_info =system_info_printer.print_system_info()

    else: 
        flash("You Don't have a Access")
        return redirect(url_for('view.home'))


    return render_template ('admin.html',storage_info=storage_info,system_info=system_info)