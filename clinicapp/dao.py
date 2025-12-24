import hashlib
import json

from clinicapp import app, db
from models import Category, Medicine, User, TreatmentSheet, Services, Patient, MedicineCategory


def load_categories():
    return Category.query.all()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    return User.query.filter(User.username.__eq__(username) and User.password.__eq__(password)).first()


def add_user(name, username, password, avatar):
    password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def delete_details(id, name):
    try:
        # Tim ban ghi dua tren ID va Ten Model
        if (name == 'Medicine'):
            to_delete = Medicine.query.get(id)
        if (name == 'TreatmentSheet'):
            to_delete = TreatmentSheet.query.get(id)
        if (name == 'Patient'):
            to_delete = Patient.query.get(id)

        if to_delete:
            db.session.delete(to_delete)
            db.session.commit()
            return True
        else:
            return False

    except Exception as e:
        db.session.rollback()
        print(f"DAO ERROR (Delete): {e}")
        return False

def get_patient_by_name(name):
    if not name:
        return None
    return Patient.query.filter(Patient.name == name.strip()).first()


def add_service_detail(dichvu, dongia, ghichu, ngaylapphieu, patient_id):
    new_treatment_detail = TreatmentSheet(
        name=dichvu,
        price=dongia,
        note=ghichu,
        created_date=ngaylapphieu,
        patient_id=patient_id
    )

    try:
        db.session.add(new_treatment_detail)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi thêm phiếu: {e}")
        db.session.rollback()
        return False


def add_patient_info(tenbenhnhan, ngaysinh, gioitinh, sodienthoai, cancuoc, email, diachi):
    new_patient_info = Patient(
        name=tenbenhnhan,
        phone_number=sodienthoai,
        email=email,
        address=diachi,
        sex=gioitinh,
        birthday=ngaysinh,
        identity_card=cancuoc
    )

    try:
        db.session.add(new_patient_info)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi thêm bệnh nhân: {e}")
        db.session.rollback()
        return False


def add_medicine_detail(tenthuoc, lieudung, donvi, songay, ngaykedon, patient_id,chiphi):
    new_medicine_detail = Medicine(
        name=tenthuoc,
        dosage=lieudung,
        unit=donvi,
        number_of_days=songay,
        created_date=ngaykedon,
        patient_id=patient_id,
        price=chiphi# Luu ID benh nhan
    )

    try:
        db.session.add(new_medicine_detail)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi thêm thuốc: {e}")
        db.session.rollback()
        return False


def get_user_by_id(id):
    return User.query.get(id)


def count_medicines(q=None, patient_id=None):
    query = Medicine.query
    if patient_id:
        query = query.filter(Medicine.patient_id == patient_id)

    if q:
        query = query.filter(Medicine.name.contains(q))

    return query.count()

def count_patients(q=None, patient_id=None):
    query = Patient.query
    if patient_id:
        query = query.filter(Patient.patient_id == patient_id)

    if q:
        query=query.filter(Patient.name.contains(q))

    return query.count()

def count_treatmentsheets(q=None, patient_id=None):
    query = TreatmentSheet.query

    if patient_id:
        query = query.filter(TreatmentSheet.patient_id == patient_id)

    if q:
        query = query.filter(TreatmentSheet.name.contains(q))

    return query.count()


def load_treatmentsheet(q=None, page=None, patient_id=None):
    query = TreatmentSheet.query

    # Neu co patient_id thi chi lay phieu cua benh nhan do
    if patient_id:
        query = query.filter(TreatmentSheet.patient_id == patient_id)

    if q:
        query = query.filter(TreatmentSheet.name.contains(q))

    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        query = query.slice(start, start + size)

    return query.all()


def load_patient(q=None, page=None):
    query = Patient.query

    if q:
        query = query.filter(Patient.name.contains(q))

    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        query = query.slice(start, start + size)

    return query.all()


def load_services():
    query = Services.query
    return query.all()

def load_medicine_category():
    query = MedicineCategory.query
    return query.all()

def load_medicines(q=None, page=None, patient_id=None):
    query = Medicine.query

    if patient_id:
        query = query.filter(Medicine.patient_id == patient_id)

    if q:
        query = query.filter(Medicine.name.contains(q))

    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        query = query.slice(start, start + size)

    return query.all()
def get_patient_by_name(name):
    if not name:
        return None
    return Patient.query.filter(Patient.name == name.strip()).first()

def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)

from models import Doctor, Invoice

# ================= DOCTOR =================
def load_doctors():
    """Lấy danh sách bác sĩ"""
    return Doctor.query.all()

def get_doctor_by_id(doctor_id):
    """Lấy thông tin bác sĩ theo ID"""
    return Doctor.query.get(doctor_id)

from sqlalchemy import or_
from clinicapp import db
from models import Invoice, Patient, Doctor

from datetime import datetime

from datetime import datetime

def add_invoice(patient_id, doctor_id, total_service, total_medicine, vat, total_payment, created_date=None):
    if not created_date:
        created_date = datetime.now()
    elif isinstance(created_date, str):
        # Chuyển chuỗi thành datetime
        created_date = datetime.strptime(created_date, "%Y-%m-%d")

    invoice_name = f"Hóa đơn ngày {created_date.strftime('%d/%m/%Y')}"

    inv = Invoice(
        name=invoice_name,
        patient_id=patient_id,
        doctor_id=doctor_id,
        total_service=total_service,
        total_medicine=total_medicine,
        vat=vat,
        total_payment=total_payment,
        created_date=created_date
    )
    try:
        db.session.add(inv)
        db.session.commit()
        return inv
    except Exception as e:
        db.session.rollback()
        print("Lỗi lưu hóa đơn:", e)
        return None

def load_invoices(keyword=None):
    query = Invoice.query.join(Patient).join(Doctor)

    if keyword:
        keyword = f"%{keyword}%"
        query = query.filter(
            or_(
                Patient.name.ilike(keyword),
                Doctor.name.ilike(keyword)
            )
        )

    return query.order_by(Invoice.created_date.desc()).all()

def load_unpaid_treatments(patient_id):
    return TreatmentSheet.query.filter(
        TreatmentSheet.patient_id == patient_id,
        TreatmentSheet.invoice_id == None
    ).all()

def load_unpaid_medicines(patient_id):
    return Medicine.query.filter(
        Medicine.patient_id == patient_id,
        Medicine.invoice_id == None
    ).all()



def get_invoice_by_id(invoice_id):
    """Lấy hóa đơn theo ID"""
    return Invoice.query.get(invoice_id)


def update_invoice(invoice_id, doctor_id=None, total_service=None, total_medicine=None, vat=None, total_payment=None):
    """Cập nhật hóa đơn"""
    inv = Invoice.query.get(invoice_id)
    if not inv:
        return None

    if doctor_id:
        inv.doctor_id = doctor_id
    if total_service is not None:
        inv.total_service = total_service
    if total_medicine is not None:
        inv.total_medicine = total_medicine
    if vat is not None:
        inv.vat = vat
    if total_payment is not None:
        inv.total_payment = total_payment

    try:
        db.session.commit()
        return inv
    except Exception as e:
        print(f"Lỗi cập nhật hóa đơn: {e}")
        db.session.rollback()
        return None


def delete_invoice(invoice_id):
    """Xóa hóa đơn"""
    inv = Invoice.query.get(invoice_id)
    if not inv:
        return False

    try:
        db.session.delete(inv)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi xóa hóa đơn: {e}")
        db.session.rollback()
        return False

from models import Doctor

def add_doctor(name, specialty=None, phone_number=None, email=None):
    new_doctor = Doctor(
        name=name,
        specialty=specialty,
        phone_number=phone_number,
        email=email
    )
    try:
        db.session.add(new_doctor)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi thêm bác sĩ: {e}")
        db.session.rollback()
        return False

def load_doctors(q=None, page=None):
    query = Doctor.query
    if q:
        query = query.filter(Doctor.name.contains(q))
    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        query = query.slice(start, start + size)
    return query.all()

def count_doctors(q=None):
    query = Doctor.query
    if q:
        query = query.filter(Doctor.name.contains(q))
    return query.count()

def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor:
        try:
            db.session.delete(doctor)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Lỗi xóa bác sĩ: {e}")
            db.session.rollback()
            return False
    return False

from sqlalchemy import func
from models import Invoice, Doctor

# ================= DOANH THU =================

def revenue_by_date(from_date=None, to_date=None):
    query = db.session.query(
        Invoice.created_date,
        func.sum(Invoice.total_payment)
    )

    if from_date:
        query = query.filter(Invoice.created_date >= from_date)
    if to_date:
        query = query.filter(Invoice.created_date <= to_date)

    query = query.group_by(Invoice.created_date).order_by(Invoice.created_date)

    return query.all()


def revenue_by_doctor(doctor_id, from_date=None, to_date=None):
    query = db.session.query(
        Doctor.name,
        func.sum(Invoice.total_payment)
    ).join(Invoice)

    query = query.filter(Invoice.doctor_id == doctor_id)

    if from_date:
        query = query.filter(Invoice.created_date >= from_date)
    if to_date:
        query = query.filter(Invoice.created_date <= to_date)

    query = query.group_by(Doctor.name)

    return query.first()


if __name__ == '__main__':
    with app.app_context():
        print(auth_user("user", "123"))