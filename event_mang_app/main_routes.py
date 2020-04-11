from flask import render_template, request

from event_mang_app.forms import SearchForm
from event_mang_app.models import Data, ProjectData, SystemData, LoopData, TypeData
from event_mang_app import app


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    data = Data.query.order_by(Data.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', data=data, pro_details1=ProjectData.query.all(),
                           pro_details2=SystemData.query.all(), pro_details3=LoopData.query.all(),
                           pro_details4=TypeData.query.all())


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    try:
        page = request.args.get('page', 1, type=int)
        if form.validate_on_submit():
            data = Data.query.filter_by(project_name=form.project_name.data.upper(),
                                        system_name=form.system_name.data.upper(),
                                        loop_num=form.loop_num.data, type_file=form.type_file.data.upper()).order_by(
                Data.date_posted.desc()).paginate(page=page, per_page=5)
            return render_template('results.html', data=data, form=form, pro_details1=ProjectData.query.all(),
                                   pro_details2=SystemData.query.all(), pro_details3=LoopData.query.all(),
                                   pro_details4=TypeData.query.all(), title='Search Results', legend='hello')
    except:
        pass
    return render_template('search.html', title='Search', form=form, pro_details1=ProjectData.query.all(),
                           pro_details2=SystemData.query.all(), pro_details3=LoopData.query.all(),
                           pro_details4=TypeData.query.all())


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
