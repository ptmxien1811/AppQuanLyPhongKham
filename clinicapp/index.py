from flask import Flask, render_template, request
from clinicapp import dao

app = Flask(__name__)



@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('cate_id')


    return render_template("index.html")
# @app.route('/product/<int:id>')
# def details(id):
#     prod=dao.get_product_by_id(id)
#     q = request.args.get('q')
#     cate_id = request.args.get('cate_id')
#     cates = dao.load_categories()
#     prods = dao.load_products(q=q, cate_id=cate_id)
#     return render_template("product-details.html",prod=prod,cates=cates,prods=prods)

@app.route('/cate_id/<int:id>')
def create_form(id):
    if (id==2):
        return render_template("tab1.html")
    elif (id==1):
        return render_template("tab2.html")
    elif (id==3):
        return render_template("tab3.html")
    elif (id==4):
        return render_template("tab4.html")
    else:
        return render_template("tab5.html")

@app.context_processor
def common_attribute():
    return {
        "cates":dao.load_categories(),
        "meds":dao.load_medicines()
    }

if __name__ == '__main__':
    app.run(debug=True)