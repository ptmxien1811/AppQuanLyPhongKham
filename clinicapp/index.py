from datetime import date
from flask import render_template, request, redirect, url_for, flash
from clinicapp import dao, app, login, admin, db
import math
from flask_login import login_user, current_user, logout_user
from clinicapp.dao import add_medicine_detail, delete_details, add_service_detail, add_patient_info
import cloudinary.uploader
from types import SimpleNamespace
from clinicapp.models import LichHen

from models import UserEnum


@app.route('/')
def index():
    pages = math.ceil(dao.count_medicines() / app.config["PAGE_SIZE"])
    return render_template("index.html", pages=pages)

@app.route("/", methods=["GET", "POST"])
def indexx():
    if request.method == "POST":
        ten_benh_nhan = request.form["ten_benh_nhan"]
        ngay = request.form["ngay"]
        gio = request.form["gio"]
        noi_dung = request.form["noi_dung"]

        trung = LichHen.query.filter_by(ngay=ngay, gio=gio).first()
        if trung:
            flash("❌ Giờ này đã có lịch rồi!","error")
            return redirect("/")

        lich = LichHen(
            ten_benh_nhan=request.form["ten_benh_nhan"],
            ngay=ngay,
            gio=gio,
            noi_dung=request.form["noi_dung"]
        )
        db.session.add(lich)
        db.session.commit()

        flash("✅ Đặt lịch thành công!")
        return redirect("/")

    lichhen = LichHen.query.all()
    return render_template("tab2.html", lich=lichhen)

@app.route("/delete/<int:id>")
def delete(id):
        lich = LichHen.query.get(id)
        if lich:
            db.session.delete(lich)
            db.session.commit()
        return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    lich = LichHen.query.get(id)

    if request.method == "POST":
        lich.ten_benh_nhan = request.form["ten_benh_nhan"]
        lich.ngay = request.form["ngay"]
        lich.gio = request.form["gio"]
        lich.noi_dung = request.form["noi_dung"]
        db.session.commit()
        return redirect(url_for("main.indexx"))

    return render_template("edit.html", lich=lich)
if __name__ == '__main__':
    app.run(debug=True)

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
        return render_template("pages/tab2.html")

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



    elif id == 4:
        all_patients = dao.load_patient(page=None)
        doctors = dao.load_doctors()  # thêm dòng này

        p_id = selected_patient.id if selected_patient else None
        services = dao.load_treatmentsheet(patient_id=p_id) if p_id else []
        medicines = dao.load_medicines(patient_id=p_id) if p_id else []

        total_service = sum(float(s.price) for s in services)
        total_medicine = sum(float(m.price) for m in medicines)
        sub_total = total_service + total_medicine
        vat = sub_total * 0.1
        total_payment = sub_total + vat

        return render_template(
            "pages/tab4.html",
            patient=all_patients,
            doctors=doctors,  # truyền vào template
            selected_patient=selected_patient,
            services=services,
            medicines=medicines,
            total_service=total_service,
            total_medicine=total_medicine,
            vat=vat,
            total_payment=total_payment
        )

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

# Hàm chuyển đổi chuỗi tiền tệ sang float an toàn
def to_float(v):
    if v is None:
        return 0
    v = str(v).strip()
    # bỏ dấu chấm ngăn cách hàng nghìn
    v = v.replace('.', '')
    # nếu có dấu phẩy thì đổi thành dấu chấm (trường hợp số thập phân)
    v = v.replace(',', '.')
    try:
        return float(v)
    except ValueError:
        return 0

@app.route('/cate_id/4', methods=['GET', 'POST'])
def invoice_page():
    # Danh sách bệnh nhân và bác sĩ
    patients = dao.load_patient(page=None)
    doctors = dao.load_doctors()

    # Lấy dữ liệu từ form/URL
    patient_id = request.args.get('patient_id')
    doctor_id = request.form.get('doctor_id')
    created_date = request.form.get('created_date') or date.today()

    # Lấy thông tin bệnh nhân, dịch vụ, thuốc
    selected_patient = dao.get_patient_by_id(patient_id) if patient_id else None
    services = dao.load_treatmentsheet(patient_id=patient_id) if patient_id else []
    medicines = dao.load_medicines(patient_id=patient_id) if patient_id else []

    # Tính toán tổng tiền (dùng to_float để tránh lỗi)
    total_service = sum(to_float(s.price) for s in services)
    total_medicine = sum(to_float(m.price) for m in medicines)
    vat = (total_service + total_medicine) * 0.1
    total_payment = total_service + total_medicine + vat

    # Nếu POST thì lưu hóa đơn
    if request.method == 'POST' and patient_id and doctor_id:
        dao.add_invoice(patient_id, doctor_id,
                        total_service, total_medicine,
                        vat, total_payment, created_date)
        flash("Hóa đơn đã được lưu thành công!", "success")
        return redirect(url_for('invoice_list'))

    # Tạo đối tượng invoice để template dễ dùng
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
            created_date=created_date
        )

    return render_template("pages/tab4.html",
                           patients=patients,
                           doctors=doctors,
                           invoice=invoice,
                           selected_doctor=dao.get_doctor_by_id(doctor_id) if doctor_id else None,
                           today=date.today())


@app.route('/invoices')
def invoice_list():
    keyword = request.args.get('keyword')
    invoices = dao.load_invoices(keyword)
    return render_template("pages/invoice_list.html", invoices=invoices)
@app.route('/invoice/edit/<int:invoice_id>', methods=['GET', 'POST'])
def edit_invoice(invoice_id):
    invoice = dao.get_invoice_by_id(invoice_id)
    doctors = dao.load_doctors()
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
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


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)