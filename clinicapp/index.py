
from clinicapp import dao, app, login, admin, db
import math
from flask_login import login_user, current_user, logout_user
from clinicapp.dao import add_medicine_detail, delete_details, add_service_detail, add_patient_info
import cloudinary.uploader
from flask import Flask
from clinicapp import dao


from models import UserEnum


@app.route('/')
def index():
    pages = math.ceil(dao.count_medicines() / app.config["PAGE_SIZE"])
    return render_template("index.html", pages=pages)


@app.route('/delete-detail/<int:id>/<string:name>', methods=['POST'])
def delete_detail(id, name):
    if request.form.get('action') == 'delete_details':
        if delete_details(id, name):
            print('Xoa thong tin thanh cong')
        else:
            print('Loi khi xoa thong tin')
    return redirect(request.referrer)


@app.route('/patient_management', methods=['GET', 'POST'])
def patient_management():
    if not current_user.is_authenticated or current_user.role != UserEnum.ADMIN:
        flash("Bạn không có quyền truy cập trang này!", "danger")
        return redirect('/')

    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)


    pages = math.ceil(dao.count_patients() / app.config["PAGE_SIZE"])

    if request.method == 'POST':
        tenbenhnhan = request.form.get('tenbenhnhan')
        ngaysinh = request.form.get('ngaysinh')
        gioitinh = request.form.get('gioitinh')
        sodienthoai = request.form.get('sodienthoai')
        cancuoc = request.form.get('cancuoc')
        email = request.form.get('email')
        diachi = request.form.get('diachi')

        if add_patient_info(tenbenhnhan=tenbenhnhan,
                            ngaysinh=ngaysinh,
                            gioitinh=gioitinh,
                            sodienthoai=sodienthoai,
                            cancuoc=cancuoc,
                            email=email,
                            diachi=diachi):
            print('Them benh nhan thanh cong!')
        else:
            print('Loi khi them benh nhan!')

    patient = dao.load_patient(q=q, page=page)
    return render_template('pages/patient_management.html', pages=pages, page=page, patient=patient)


@app.route('/cate_id/<int:id>', methods=['GET', 'POST'])
def create_form(id):
    if not current_user.is_authenticated:
        return redirect('/login')

    allowed_for_user = [1, 4]

    if current_user.role == UserEnum.USER and id not in allowed_for_user:
        flash("Bạn không có quyền truy cập chức năng này!", "danger")
        return redirect('/')

    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)


    selected_patient_name = request.values.get('benhnhan')
    selected_patient = None

    if selected_patient_name:
        selected_patient = dao.get_patient_by_name(selected_patient_name)

    if (id == 2):
        if request.method == 'POST' and 'dichvu' in request.form:
            dichvu = request.form.get('dichvu')
            dongia = request.form.get('dongia')
            ghichu = request.form.get('ghichu')
            ngaylapphieu = request.form.get('ngaylapphieu')

            patient_id_hidden = request.form.get('patient_id_hidden')

            if patient_id_hidden:
                if add_service_detail(dichvu=dichvu,
                                      dongia=dongia,
                                      ghichu=ghichu,
                                      ngaylapphieu=ngaylapphieu,
                                      patient_id=patient_id_hidden):
                    print('Them phieu thanh cong!')
                else:
                    print('Loi khi them phieu!')
            else:
                print('Chua chon benh nhan!')

        today = date.today()
        today_formatted = today.strftime('%Y-%m-%d')

        p_id = selected_patient.id if selected_patient else None

        all_patients = dao.load_patient(page=None)
        treatm = dao.load_treatmentsheet(q=q, page=page, patient_id=p_id)
        serv = dao.load_services()
        total_sheets = dao.count_treatmentsheets(q=q, patient_id=p_id)
        pages = math.ceil(total_sheets / app.config["PAGE_SIZE"])

        return render_template("pages/tab1.html", treatm=treatm, q=q, pages=pages,
                               serv=serv, patient=all_patients, selected_patient=selected_patient,today=today_formatted)



    elif (id == 1):

        patients = dao.load_patient(page=None)

        doctors = Doctor.query.all()

        appointments = Appointment.query.order_by(

            Appointment.appointment_date.desc(),

            Appointment.appointment_time.desc()

        ).all()

        if request.method == 'POST':

            patient_data = {

                'name': request.form.get('patient_name'),

                'sex': request.form.get('sex'),

                'birthday': request.form.get('birthday'),

                'phone_number': request.form.get('phone_number'),

                'email': request.form.get('email'),

                'address': request.form.get('address'),

                'identity_card': request.form.get('identity_card')

            }

            doctor_id = int(request.form.get('doctor_id'))

            appointment_date = request.form.get('appointment_date')

            appointment_time = request.form.get('appointment_time')

            note = request.form.get('note')

            # 🔍 Kiểm tra trùng giờ

            existing = Appointment.query.filter_by(

                doctor_id=doctor_id,

                appointment_date=appointment_date,

                appointment_time=appointment_time

            ).first()

            # 🔍 Kiểm tra số lượng lịch trong ngày

            count_same_day = Appointment.query.filter_by(

                doctor_id=doctor_id,

                appointment_date=appointment_date

            ).count()

            if existing:

                flash("❌ Giờ này đã được đặt!", "danger")

            elif count_same_day >= 5:

                flash("❌ Bác sĩ đã đủ 5 lịch trong ngày!", "danger")

            else:

                schedule_appointment(

                    patient_data,

                    doctor_id,

                    appointment_date,

                    appointment_time,

                    note

                )

                flash("✅ Đặt lịch thành công!", "success")

            return redirect(url_for('create_form', id=1))

        return render_template(

            'pages/tab2.html',

            doctors=doctors,

            appointments=appointments,

            patients=patients

        )

    elif (id == 3):
        if request.method == 'POST' and 'tenthuoc' in request.form:
            tenthuoc = request.form.get('tenthuoc')
            lieudung = request.form.get('lieudung')
            donvi = request.form.get('donvi')
            songay = request.form.get('songay')
            ngaykedon = request.form.get('ngaykedon')
            chiphi = request.form.get('chiphi')

            # Lay ID benh nhan tu input an
            patient_id_hidden = request.form.get('patient_id_hidden')

            if patient_id_hidden:
                if add_medicine_detail(tenthuoc=tenthuoc,
                                       lieudung=lieudung,
                                       donvi=donvi,
                                       songay=songay,
                                       ngaykedon=ngaykedon,
                                       patient_id=patient_id_hidden,
                                       chiphi=chiphi):
                    print('Them thuoc thanh cong!')
                else:
                    print('Loi khi them thuoc!')
            else:
                print('Chua chon benh nhan!')

        today = date.today()
        today_formatted = today.strftime('%Y-%m-%d')

        p_id = selected_patient.id if selected_patient else None

        all_patients = dao.load_patient(page=None)
        meds_cate=dao.load_medicine_category()
        meds = dao.load_medicines(q=q, page=page, patient_id=p_id)
        total_meds = dao.count_medicines(q=q, patient_id=p_id)
        pages = math.ceil(total_meds / app.config["PAGE_SIZE"])

        return render_template("pages/tab3.html", meds=meds, pages=pages,
                               today=today_formatted, patient=all_patients, selected_patient=selected_patient,meds_cate=meds_cate)

    elif (id == 4):
        patients = dao.load_patient(page=None)
        doctors = dao.load_doctors()

        patient_id = request.args.get('patient_id')
        selected_patient = dao.get_patient_by_id(patient_id) if patient_id else None
        doctor_id = request.form.get('doctor_id')
        created_date = request.form.get('created_date') or date.today()

        # Tính tổng dịch vụ và thuốc
        services = dao.load_unpaid_treatments(patient_id) if patient_id else []
        medicines = dao.load_unpaid_medicines(patient_id) if patient_id else []

        total_service = sum(to_float(s.price) for s in services)
        total_medicine = sum(to_float(m.price) for m in medicines)
        vat = int((total_service + total_medicine) * 0.1)
        total_payment = total_service + total_medicine + vat

        # POST: Lưu hóa đơn
        if request.method == 'POST' and patient_id and doctor_id:
            inv = dao.add_invoice(
                patient_id=int(patient_id),
                doctor_id=int(doctor_id),
                total_service=total_service,
                total_medicine=total_medicine,
                vat=vat,
                total_payment=total_payment,
                created_date=created_date
            )
            if inv:
                flash("✅ Lưu hóa đơn thành công!", "success")
                return redirect(url_for('view_invoice', invoice_id=inv.id))
            else:
                flash("❌ Lỗi khi lưu hóa đơn!", "danger")

        # GET: hiển thị thông tin tạm tính trước khi lưu
        invoice = None
        if selected_patient:
            invoice = SimpleNamespace(
                patient=selected_patient,
                services=services,
                medicines=medicines,
                total_service=total_service,
                total_medicine=total_medicine,
                vat=vat,
                total_payment=total_payment,
                created_date=date.today()
            )

        return render_template(
            "pages/tab4.html",
            patients=patients,
            doctors=doctors,
            invoice=invoice,
            today=date.today()
        )


    else:

        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        doctor_id = request.args.get('doctor_id')

        doctors = dao.load_doctors()

        labels = []
        values = []
        doctor_revenue = None

        # ✅ CHỈ CẢNH BÁO KHI USER ĐÃ BẤM XEM
        if (doctor_id or request.args) and (not from_date or not to_date):
            flash("⚠️ Hãy chọn thời gian bạn muốn xem doanh thu!", "warning")

        elif from_date and to_date:
            from datetime import datetime

            try:
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()

                # Doanh thu toàn phòng khám
                revenue_data = dao.revenue_by_date(from_date_obj, to_date_obj)
                labels = [r[0].strftime('%d/%m/%Y') for r in revenue_data]
                values = [r[1] for r in revenue_data]

                # Doanh thu theo bác sĩ
                if doctor_id:
                    doctor_revenue = dao.revenue_by_doctor(
                        doctor_id=int(doctor_id),
                        from_date=from_date_obj,
                        to_date=to_date_obj
                    )

            except ValueError:
                flash("⚠️ Dữ liệu thời gian không hợp lệ!", "danger")

        return render_template(
            "pages/tab5.html",
            labels=labels,
            values=values,
            doctors=doctors,
            doctor_revenue=doctor_revenue,
            from_date=from_date,
            to_date=to_date,
            doctor_id=doctor_id
        )


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
                dao.add_user(name, username, password, avatar=path_file)
                return redirect('/login')
            except:
                db.session.rollback()
                err_msg = "He thong dang co loi!"
        else:
            err_msg = "Mat khau khong khop!"
    return render_template("register.html", err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect('/')

    err_msg = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "Tài khoản hoặc mật khẩu không chính xác!"

    return render_template("login.html", err_msg=err_msg)


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories(),
    }


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


def to_float(v):
    if v is None:
        return 0
    v = str(v).strip()

    v = v.replace('.', '')

    v = v.replace(',', '.')
    try:
        return float(v)
    except ValueError:
        return 0

from types import SimpleNamespace
from datetime import date




# ----------------- Xem hóa đơn -----------------
@app.route('/invoice/view/<int:invoice_id>')
def view_invoice(invoice_id):
    invoice = dao.get_invoice_by_id(invoice_id)
    if not invoice:
        flash("Không tìm thấy hóa đơn!", "warning")
        return redirect(url_for('invoice_pagecate/'))

    return render_template("pages/view_invoice.html", invoice=invoice)



@app.route('/invoices')
def invoice_list():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)

    total = dao.count_invoices(keyword)
    pages = math.ceil(total / app.config["PAGE_SIZE"])

    invoices = dao.load_invoices(keyword, page)

    return render_template("pages/invoice_list.html",
                           invoices=invoices,
                           pages=pages,
                           current_page=page)
@app.route('/invoice/edit/<int:invoice_id>', methods=['GET', 'POST'])
def edit_invoice(invoice_id):
    invoice = dao.get_invoice_by_id(invoice_id)
    doctors = dao.load_doctors()
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id') or request.args.get('doctor_id')
        dao.update_invoice(invoice_id, doctor_id=doctor_id)
        flash("Hóa đơn đã được cập nhật!", "info")
        return redirect(url_for('invoice_list'))
    return render_template("pages/edit_invoice.html", invoice=invoice, doctors=doctors)
@app.route('/invoice/delete/<int:invoice_id>', methods=['POST'])
def delete_invoice(invoice_id):
    if dao.delete_invoice(invoice_id):
        flash("Đã xóa hóa đơn!", "danger")
    else:
        flash("Lỗi khi xóa hóa đơn!", "warning")
    return redirect(url_for('invoice_list'))


@app.route('/doctor_management', methods=['GET', 'POST'])
def doctor_management():
    if not current_user.is_authenticated or current_user.role != UserEnum.ADMIN:
        flash("Bạn không có quyền truy cập trang này!", "danger")
        return redirect('/')

    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    pages = math.ceil(dao.count_doctors(q=q) / app.config["PAGE_SIZE"])

    if request.method == 'POST':
        name = request.form.get('name')
        specialty = request.form.get('specialty')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')

        if dao.add_doctor(name=name, specialty=specialty, phone_number=phone_number, email=email):
            flash("Thêm bác sĩ thành công!", "success")
        else:
            flash("Lỗi khi thêm bác sĩ!", "danger")

    doctors = dao.load_doctors(q=q, page=page)
    return render_template('pages/doctor_management.html', pages=pages, page=page, doctors=doctors)



app = Flask(__name__)
app.secret_key = "secret_key"


from clinicapp import app, db
from flask import render_template, request, redirect, url_for, flash
from clinicapp import app
from models import Doctor, Appointment
from clinicapp.dao import schedule_appointment



if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)