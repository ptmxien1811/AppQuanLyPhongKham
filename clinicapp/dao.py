import hashlib
import json

from clinicapp import app, db
from models import Category, Medicine, User, TreatmentSheet, Services


def load_categories():
    # Doc tu file json
    # with open('data/category.json', encoding='utf-8') as f:
    #     cates = json.load(f)


        return Category.query.all()

def auth_user(username,password):

    password=str(hashlib.md5(password.encode("utf-8")).hexdigest())

    return User.query.filter(User.username.__eq__(username) and User.password.__eq__(password)).first()

def add_user(name,username,password,avatar):
    password=hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    u = User(name=name,username=username.strip(),password=password,avatar=avatar)
    db.session.add(u)
    db.session.commit()

def delete_details(id,name):


    try:
        #  tim ban ghi dua tren ID
        if (name=='Medicine'):
            to_delete = Medicine.query.get(id)
        if (name=='TreatmentSheet'):
            to_delete = TreatmentSheet.query.get(id)

        if to_delete:
            # xoa ban ghi
            db.session.delete(to_delete)
            # commit
            db.session.commit()
            return True
        else:
            return False

    except Exception as e:
        db.session.rollback()
        print(f"DAO ERROR (Delete): {e}")  # Rất quan trọng để debug nếu lỗi
        return False

def add_service_detail(dichvu,dongia,ghichu,ngaylapphieu):
    new_treatment_detail = TreatmentSheet(
        name=dichvu,
        price=dongia,
        note=ghichu,
        created_date=ngaylapphieu
    )

    try:
        db.session.add(new_treatment_detail)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False



def add_medicine_detail(tenthuoc, lieudung, donvi, songay, ngaykedon):
    # tao doi tuong moi
    new_medicine_detail = Medicine(
        name=tenthuoc,
        dosage=lieudung,
        unit=donvi,
        number_of_days=songay,
        created_date=ngaykedon
    )

    try:
        # add doi tuong vao db sau do commit
        db.session.add(new_medicine_detail)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def get_user_by_id(id):
    return User.query.get(id)

def count_medicines():
    return Medicine.query.count()


def load_treatmentsheet(q=None,page=None):

    query = TreatmentSheet.query

    if q:
        query = query.filter(TreatmentSheet.name.contains(q))

    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        query = query.slice(start, start + size)  # ham lay san pham tu diem bat dau cho den diem ket thuc

    return query.all()

def load_services():
    query=Services.query

    return query.all()

def load_medicines(q=None,page=None):
    # with open('data/medicine.json', encoding='utf-8') as f:
    #     meds = json.load(f)
    #
    #     if q:
    #         meds = [m for m in meds if m["medicine_name"].find(q)>=0]
    #
    #     # if cate_id:
    #     #    prods = [p for p in prods if p["cate_id"].__eq__(int(cate_id))]
    #     return meds

    query = Medicine.query

    if q:
        query = query.filter(Medicine.name.contains(q))


    if page:
        size=app.config["PAGE_SIZE"]
        start = (int(page)-1)*size
        query = query.slice(start, start+size) #ham lay san pham tu diem bat dau cho den diem ket thuc


    return query.all()


# def get_product_by_id(id):
#         with open('data/medicine.json', encoding='utf-8') as f:
#             prods = json.load(f)
#
#         for p in prods:
#             if p["id"].__eq__(id):
#                 return p
#         #Luu y phai di chuyen return None ra khoi vong lap (ben ngoai vong lap)!
#         return None



if __name__ == '__main__':
    with app.app_context():
        print(auth_user("user","123"))
