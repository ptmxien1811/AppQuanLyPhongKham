from datetime import date

from flask import render_template, request, redirect, url_for, flash
from clinicapp import dao, app, login, admin,db
import math
from flask_login import login_user, current_user, logout_user
from clinicapp.dao import add_medicine_detail, delete_details, add_service_detail, add_patient_info
import cloudinary.uploader

@app.route('/')
def index():
    pages = math.ceil(dao.count_medicines()/app.config["PAGE_SIZE"])

    return render_template("index.html",pages=pages)


@app.route('/delete-detail/<int:id>/<string:name>', methods=['POST'])
def delete_detail(id,name):
    if request.form.get('action') == 'delete_details':
        if delete_details(id,name):
            print('Xoa thong tin thuoc thanh cong')
        else:
            print('Khong tim thay muc thuoc hoac bi loi khi xoa.')

    #chuyen huong ve trng truoc do
    return redirect(request.referrer)

@app.route('/patient_management',methods=['GET', 'POST'])
def patient_management():
    q=request.args.get('q')
    page=request.args.get('page', 1, type=int)
    pages = math.ceil(dao.count_medicines() / app.config["PAGE_SIZE"])

    tenbenhnhan=request.form.get('tenbenhnhan')
    ngaysinh=request.form.get('ngaysinh')
    gioitinh=request.form.get('gioitinh')
    sodienthoai=request.form.get('sodienthoai')
    cancuoc=request.form.get('cancuoc')
    email=request.form.get('email')
    diachi=request.form.get('diachi')

    if add_patient_info(tenbenhnhan=tenbenhnhan,
                        ngaysinh=ngaysinh,
                        gioitinh=gioitinh,
                        sodienthoai=sodienthoai,
                        cancuoc=cancuoc,
                        email=email,
                        diachi=diachi):

        print('Them thanh cong!')
    else:
        print('Loi khi dua du lieu vao CSDL!')

    patient=dao.load_patient(q=q,page=page)
    return render_template('pages/patient_management.html',pages=pages,page=page,patient=patient)

@app.route('/cate_id/<int:id>', methods=['GET', 'POST'])
def create_form(id):
    q = request.args.get('q')
    page=request.args.get('page')
    pages = math.ceil(dao.count_medicines() / app.config["PAGE_SIZE"])
    page = request.args.get('page', 1, type=int)

    if (id==2):
        dichvu = request.form.get('dichvu')
        dongia = request.form.get('dongia')
        ghichu = request.form.get('ghichu')
        ngaylapphieu = request.form.get('ngaylapphieu')

        if add_service_detail(dichvu=dichvu,
                               dongia=dongia,
                               ghichu=ghichu,
                               ngaylapphieu=ngaylapphieu):

            print('Them thanh cong!')
        else:
            print('Loi khi dua du lieu vao CSDL!')

        treatm=dao.load_treatmentsheet(q=q,page=page)
        serv=dao.load_services()
        return render_template("pages/tab1.html",treatm=treatm,q=q,pages=pages,serv=serv)
    elif (id==1):
        return render_template("pages/tab2.html")
    elif (id==3):

        today=date.today()
        today_formatted=today.strftime('%Y-%m-%d')


        tenthuoc = request.form.get('tenthuoc')
        lieudung = request.form.get('lieudung')
        donvi = request.form.get('donvi')
        songay = request.form.get('songay')
        ngaykedon = request.form.get('ngaykedon')

        if add_medicine_detail(tenthuoc=tenthuoc,
                               lieudung=lieudung,
                               donvi=donvi,
                               songay=songay,
                               ngaykedon=ngaykedon):

            print('Them thanh cong!')
        else:
            print('Loi khi dua du lieu vao CSDL!')

        patient=dao.load_patient(q=q,page=page)
        meds = dao.load_medicines(q=q, page=page)


        return render_template("pages/tab3.html",meds=meds,pages=pages,today=today_formatted,patient=patient)
    elif (id==4):
        return render_template("pages/tab4.html")
    else:
        return render_template("pages/tab5.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    err_msg = None
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password == confirm:
            name = request.form.get('name')
            username = request.form.get('username')
            avatar = request.files.get('avatar')

            path_file = None
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                path_file = res['secure_url']

            try:
                dao.add_user(name,username,password,avatar=path_file)
                return redirect('/login')
            except:
                db.session.rollback()
                err_msg="He thong dang co loi!"
        else:
            err_msg="Mat khau khong khop!"
    return render_template("register.html",err_msg=err_msg)
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