from flask import render_template, request
from clinicapp import dao, app
import math

@app.route('/')
def index():
    pages = math.ceil(dao.count_medicines()/app.config["PAGE_SIZE"])

    return render_template("index.html",pages=pages)


@app.route('/cate_id/<int:id>')
def create_form(id):
    q = request.args.get('q')
    print(q)
    page=request.args.get('page')
    meds= dao.load_medicines(q=q,page=page)

    pages = math.ceil(dao.count_medicines() / app.config["PAGE_SIZE"])
    if (id==2):
        return render_template("tab1.html")
    elif (id==1):
        return render_template("tab2.html")
    elif (id==3):
        return render_template("tab3.html",meds=meds,pages=pages)
    elif (id==4):
        return render_template("tab4.html")
    else:
        return render_template("tab5.html")

@app.route('/login')
def login_my_user():
    return render_template("login.html")

@app.context_processor
def common_attribute():
    return {
        "cates":dao.load_categories(),
    }

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)