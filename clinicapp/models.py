import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from clinicapp import db, app
from flask_login import UserMixin
from enum import Enum as RoleEnum


class UserEnum(RoleEnum):
    USER = 1
    ADMIN = 2

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    active = Column(Boolean,default=True)
    created_date= Column(DateTime,default=datetime.now())
    def __str__(self):
        return self.name


class User(Base, UserMixin):
    username=Column(String(150),unique=True,nullable=False)
    password = Column(String(150),nullable=False)
    avatar = Column(String(300),default="https://cdn-icons-png.flaticon.com/512/219/219969.png")
    role = Column(Enum(UserEnum),nullable=False,default=UserEnum.USER)

class TreatmentSheet(Base):
    price= Column(String(150),nullable=False)
    note=Column(String(150),nullable=False)

class Category(Base):
    path= Column(String(150),nullable=False)
    icon = Column(String(150),nullable=False)

    def __str__(self):
        return self.name

class Medicine(Base):
    name = Column(String(150), nullable=False)
    dosage= Column(Integer,default=0)
    unit= Column(String(150),nullable=False)
    number_of_days= Column(Integer, default=0)

    def __str__(self):
        return self.name


# ... (Các Model User, Category, Medicine ở trên) ...




if __name__ == '__main__':
    with app.app_context():



        #Lenh tao bang, comment de ko bi trung`
        # db.create_all()
        # c1 = Category(name="Đặt lịch",path="tab1.html",icon="calendar_month")
        # c2 = Category(name="Lập phiếu",path="tab2.html",icon="medical_information")
        # c3 = Category(name="Quản lý thuốc",path="tab3.html",icon="fluid_balance")
        # c4 = Category(name="Lập hóa đơn thanh toán",path="tab4.html",icon="credit_score")
        # c5 = Category(name="Báo cáo doanh thu",path="tab5.html",icon="chart_data")

        # # them noi dung tu file json > database
        # with open('data/medicine.json', encoding='utf-8') as f:
        #     meds = json.load(f)
        #
        #     for m in meds:
        #         db.session.add(Medicine(**m))

        with open('data/treatment_sheet.json', encoding='utf-8') as f:
            serv = json.load(f)

            for s in serv:
                db.session.add(TreatmentSheet(**s))
        #
        # add c1,c2,.. vao db
        # db.session.add_all([c1, c2, c3, c4, c5])


        # import hashlib
        #
        # u = User(name="User",username="user",password=str(hashlib.md5("123".encode("utf-8")).hexdigest()))
        #
        # db.session.add(u)

        # chay lenh, (phai chay moi cap nhat trong database, tuong tu nhu execute)



        db.session.commit()