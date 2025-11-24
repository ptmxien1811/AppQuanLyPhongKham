import hashlib
import json

from clinicapp import app
from models import Category, Medicine, User


def load_categories():
    # Doc tu file json
    # with open('data/category.json', encoding='utf-8') as f:
    #     cates = json.load(f)


        return Category.query.all()

def auth_user(username,password):

    password=str(hashlib.md5(password.encode("utf-8")).hexdigest())

    return User.query.filter(User.username.__eq__(username) and User.password.__eq__(password)).first()


def get_user_by_id(id):
    return User.query.get(id)

def count_medicines():
    return Medicine.query.count()

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
