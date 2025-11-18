import json


def load_categories():
    with open('data/category.json', encoding='utf-8') as f:
        cates = json.load(f)
        return cates


def load_medicines():
    with open('data/medicine.json', encoding='utf-8') as f:
        meds = json.load(f)

        # if q:
        #     prods = [p for p in prods if p["name"].find(q)>=0]
        # if cate_id:
        #    prods = [p for p in prods if p["cate_id"].__eq__(int(cate_id))]
        return meds

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
    print(get_product_by_id(id))
