from flask import Flask,request,render_template

app = Flask(__name__)

@app.route('/')
@app.route('/categories',methods=["GET"])
def categoriesIndex():
  return render_template("categories/index.html")
@app.route('/categories/<int:id>',methods=["GET"])
def categoriesShow():
  return
@app.route('/categories/<int:id>/edit',methods=["GET"])
def categoriesEdit():
  return 
@app.route('/categories/<int:id>/edit',methods=["POST"])
def categoriesUpdate():
  return 
@app.route('/categories/new',methods=["GET"])
def categoriesNew():
  return 
@app.route('/categories',methods=["POST"])
def categoriesCreate():
  return
@app.route('/categories/<int:id>/delete',methods=["POST"])
def categoriesDestroy():
  return 

@app.route("/test")
@app.route('/categories/<int:id>/items',methods=["GET"])
def itemsIndex():
  return render_template("items/index.html")
@app.route('/categories/<int:id>/items/<int:item_id>',methods=["GET"])
def itemsShow():
  return 
@app.route('/categories/<int:id>/items/<int:item_id>/edit',methods=["GET"])
def itemsEdit():
  return 
@app.route('/categories/<int:id>/items/<int:item_id>/edit',methods=["POST"])
def itemsUpdate():
  return
@app.route("/test1")
@app.route('/categories/<int:id>/items/new',methods=["GET"])
def itemsNew():
  return render_template("items/new.html",title="Add new item")

@app.route('/categories/<int:id>/items',methods=["POST"])
def itemsCreate():
  return
@app.route('/categories/<int:id>/items/<int:item_id>/delete',methods=["POST"])
def itemsDestroy():
  return 

if __name__=="__main__":
  app.run(host="localhost",port=8000,debug= True)