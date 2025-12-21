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


if __name__ == '__main__':
    with app.app_context():
        print(auth_user("user", "123"))