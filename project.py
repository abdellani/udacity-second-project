from flask import Flask,request
app = Flask(__name__)


@app.route('/categories',methods=["GET"])
def categoriesIndex():
  return 
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
@app.route('/categories/<int:id>/delete',methods=["POST"])
  return 
def categoriesDestroy():
  return 


@app.route('/categories/<int:id>/items',methods=["GET"])
def itemsIndex():
  return 
@app.route('/categories/<int:id>/items/<int:item_id>',methods=["GET"])
def itemsShow():
  return 
@app.route('/categories/<int:id>/items/<int:item_id>/edit',methods=["GET"])
def itemsEdit():
  return 
@app.route('/categories/<int:id>/items/<int:item_id>/edit',methods=["POST"])
def itemsUpdate():
  return 
@app.route('/categories/<int:id>/items/new',methods=["GET"])
def itemsNew():
  return 
@app.route('/categories/<int:id>/items',methods=["POST"])
def itemsCreate():
@app.route('/categories/<int:id>/items/<int:item_id>/delete',methods=["POST"])
  return 
def itemsDestroy():
  return 

if __name__=="__main__":
  app.run(host="localhost",port=8000)