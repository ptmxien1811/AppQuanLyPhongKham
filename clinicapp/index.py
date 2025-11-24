from flask import render_template, request, redirect, url_for
from clinicapp import dao, app, login, admin
import math
from flask_login import login_user, current_user, logout_user

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

@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect('/')

    err_msg= None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username,password)

        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "Tài khoản hoặc mật khẩu không chính xác!"

    return render_template("login.html",err_msg=err_msg)

@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.context_processor
def common_attribute():
    return {
        "cates":dao.load_categories(),
    }

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)