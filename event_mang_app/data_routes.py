import os
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort
from event_mang_app.forms import DataForm, SearchForm
from event_mang_app.models import User, Data, ProjectData, SystemData, LoopData, TypeData
from event_mang_app import app, db
from flask_login import current_user, login_required


@app.route("/data/new", methods=['GET', 'POST'])
@login_required
def new_data():
    try:
        form = DataForm()

        dataa = Data.query.order_by(Data.id.desc()).first()  # to fill the form by previous data
        if request.method == 'GET':
            form.project_name.data = dataa.project_name
            form.system_name.data = dataa.system_name
            form.loop_num.data = dataa.loop_num
            form.type_file.data = dataa.type_file
    except:
        pass
    if form.validate_on_submit():
        data1 = Data(project_name=form.project_name.data.upper(), system_name=form.system_name.data.upper(),
                     loop_num=form.loop_num.data,
                     type_file=form.type_file.data.upper(), content=form.content.data, author=current_user,
                     sender=form.sender.data, file_path=form.file_path.data)
        db.session.add(data1)
        db.session.commit()
        project_data = len(ProjectData.query.all())  # for project data
        if project_data == 0:
            projects = ProjectData(project=form.project_name.data.upper(), data_id=data1.id)
            systems = SystemData(project=form.system_name.data.upper(), data_id=data1.id)
            loops = LoopData(project=form.loop_num.data, data_id=data1.id)
            types = TypeData(project=form.type_file.data.upper(), data_id=data1.id)
            db.session.add(projects)
            db.session.add(systems)
            db.session.add(loops)
            db.session.add(types)
            db.session.commit()
            print(ProjectData.query.all(), SystemData.query.all(), LoopData.query.all(), TypeData.query.all(), '....start')
        try:
            '''p_name = ProjectData.query.all()
            s_name = SystemData.query.all()
            l_num = LoopData.query.all()
            t_file = TypeData.query.all()'''
            p_name = [ProjectData.query.all(), SystemData.query.all(), LoopData.query.all(), TypeData.query.all()]
            f_data = [form.project_name.data.upper(), form.system_name.data.upper(), form.loop_num.data, form.type_file.data.upper()]
            global count
            count = 0
            for k in p_name[0]:
                print(k.project, f_data[0])
                if k.project == f_data[0]:
                    count = count + 1
                else:
                    pass
            print(count, '1')
            if count == len(p_name[0]):
                pass
            else:
                if count == 1:
                    pass
                else:
                    add = ProjectData(project=form.project_name.data.upper(), data_id=data1.id)
                    db.session.add(add)
                    db.session.commit()
            count = 0

            for k in p_name[1]:
                print(k.project, f_data[1])
                if k.project == f_data[1]:
                    count = count + 1
                else:
                    pass
            print(count, '222222222')
            if count == len(p_name[1]):
                pass
            else:
                if count == 1:
                    pass
                else:
                    add = SystemData(project=form.system_name.data.upper(), data_id=data1.id)
                    db.session.add(add)
                    db.session.commit()
            count = 0

            for k in p_name[2]:
                print(k.project, f_data[2])
                if k.project == f_data[2]:
                    count = count + 1
                else:
                    pass
            print(count, '3333333')
            if count == len(p_name[2]):
                pass
            else:
                if count == 1:
                    pass
                else:
                    add = LoopData(project=form.loop_num.data, data_id=data1.id)
                    db.session.add(add)
                    db.session.commit()
            count = 0

            for k in p_name[3]:
                print(k.project, f_data[3])
                if k.project == f_data[3]:
                    count = count + 1
                else:
                    pass
            print(count, '1')
            if count == len(p_name[3]):
                pass
            else:
                if count == 1:
                    pass
                else:
                    add = TypeData(project=form.type_file.data.upper(), data_id=data1.id)
                    db.session.add(add)
                    db.session.commit()
            count = 0


        except:
            pass
        flash(f'Your data has been added successfully', 'success')
        return redirect(url_for('home'))

    '''date = Data.query.all()
    for file in date:  # MODIFYING TIME
        file_loc = file.file_path
        try:
            modified_file1 = os.stat(file_loc).st_mtime
            modified_time1 = datetime.fromtimestamp(modified_file1)
            file.last_date_modified = modified_time1
        except:
            file.last_date_modified = file.last_date_modified
        db.session.commit()'''
    return render_template('add_data.html', title='New data', form=form, legend="New Data",
                           pro_details1=ProjectData.query.all(),
                           pro_details2=SystemData.query.all(), pro_details3=LoopData.query.all(),
                           pro_details4=TypeData.query.all())


@app.route("/data/<int:data_id>")
def data(data_id):
    data = Data.query.get_or_404(data_id)
    return render_template('data.html', title=data.project_name, data=data)


@app.route("/data/<int:data_id>/update", methods=['GET', 'POST'])
@login_required
def update_data(data_id):
    data = Data.query.get_or_404(data_id)
    if data.author != current_user:
        abort(403)
    form = DataForm()
    if form.validate_on_submit():
        data.file_path = form.file_path.data
        data.project_name = form.project_name.data
        data.system_name = form.system_name.data
        data.loop_num = form.loop_num.data
        data.type_file = form.type_file.data
        data.sender = form.sender.data
        data.content = form.content.data
        db.session.commit()
        '''p_name = [ProjectData.query.all(), SystemData.query.all(), LoopData.query.all(), TypeData.query.all()]
        f_data = [form.project_name.data, form.system_name.data, form.loop_num.data, form.type_file.data]
        for i in p_name:
            count = 0
            for j in i:
                if(f_data[i] == j.project):
                    pass
                else:
                    count = count+1'''
        flash(f'Your data has been updated!', 'success')
        return redirect(url_for('data', data_id=data.id))
    elif request.method == 'GET':
        form.project_name.data = data.project_name
        form.system_name.data = data.system_name
        form.loop_num.data = data.loop_num
        form.type_file.data = data.type_file
        form.sender.data = data.sender
        form.file_path.data = data.file_path
        form.content.data = data.content
    return render_template('add_data.html', title="Update data", form=form, legend="Update Data")


@app.route("/data/<int:data_id>/delete", methods=['POST'])
@login_required
def delete_data(data_id):
    data = Data.query.get_or_404(data_id)
    if data.author != current_user:
        abort(403)
    db.session.delete(data)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_data(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    data = Data.query.filter_by(author=user).order_by(Data.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_data.html', data=data, user=user, pro_details1=ProjectData.query.all(),
                           pro_details2=SystemData.query.all(), pro_details3=LoopData.query.all(),
                           pro_details4=TypeData.query.all())


@app.route("/data/<string:sender>")
def customer_data(sender):
    page = request.args.get('page', 1, type=int)
    user = Data.query.filter_by(sender=sender).first_or_404()
    data = Data.query.filter_by(sender=sender).order_by(Data.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('customer_data.html', sender=user, data=data, pro_details1=ProjectData.query.all(),
                           pro_details2=SystemData.query.all(), pro_details3=LoopData.query.all(),
                           pro_details4=TypeData.query.all())


@app.route("/results", methods=['GET', 'POST'])
def search_data():
    form = SearchForm()
    try:
        page = request.args.get('page', 1, type=int)
        data = Data.query.filter_by(project_name=form.project_name.data.upper(),
                                    system_name=form.system_name.data.upper(),
                                    loop_num=form.loop_num.data, type_file=form.type_file.data.upper()).order_by(
            Data.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template('results.html', data=data, form=form, pro_details1=ProjectData.query.all(),
                               pro_details2=SystemData.query.all(), pro_details3=LoopData.query.all(),
                               pro_details4=TypeData.query.all())
    except:
        pass


'''try:
    pro = Data.query.all()
    for file in pro:  # MODIFYING TIME
        file_loc = file.file_path
        try:
            modified_file1 = os.stat(file_loc).st_mtime
            modified_time1 = datetime.fromtimestamp(modified_file1)
            file.last_date_modified = modified_time1
        except:
            file.last_date_modified = file.last_date_modified
        db.session.commit()
except:
    pass'''
