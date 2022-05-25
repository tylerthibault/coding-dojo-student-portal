from flask_app import app
from flask_app.config.utils import login_admin_required
from flask import render_template, redirect, session, request

from flask_app.models import model_student, model_user

@app.route('/student/new')          
@login_admin_required
def student_new():
    context = {}
    return render_template('student_new.html', **context)

@app.route('/student/create', methods=['POST'])          
@login_admin_required
def student_create():
    cohort_id = request.form['cohort_id']
    if not model_student.Student.validate(request.form):
        return redirect(f'/cohort/{cohort_id}/edit')

    data = {
        **request.form
    }
    del data['cohort_id']
    user_id = model_user.User.create(**data)

    data = {
        'user_id': user_id,
        'cohort_id': cohort_id,
        'nickname': request.form['name']
    }

    model_student.Student.create(**data)
    return redirect(f'/cohort/{cohort_id}/edit')

@app.route('/student/<int:id>')          
@login_admin_required
def student_show(id):
    context = {}
    return render_template('student_show.html', **context)

@app.route('/student/<int:id>/edit')          
@login_admin_required
def student_edit(id):
    context = {}
    return render_template('student_edit.html', **context)

@app.route('/student/<int:id>/update', methods=['POST'])          
@login_admin_required
def student_update(id):
    return redirect('/')

@app.route('/student/<int:id>/delete')          
@login_admin_required
def student_delete(id):
    return redirect('/')

@app.route('/student/<int:id>/<int:cohort_id>/remove')          
@login_admin_required
def student_remove(id, cohort_id):
    model_student.Student.update_one(cohort_id=None, id=id)
    return redirect(f'/cohort/{cohort_id}/edit')
