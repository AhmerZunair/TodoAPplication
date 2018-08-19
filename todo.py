from flask import Flask, jsonify,json,request,render_template
from flask_pymongo import PyMongo
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from wtforms import Form, StringField, SubmitField, DecimalField


app = Flask(__name__)

app.config['MONGO_DBNAME']='ahmer'
app.config['MONGO_URI']='mongodb://zunair:pass123@ds217138.mlab.com:17138/ahmer'
mongo = PyMongo(app)


class InsertForm(Form):
    id = DecimalField(
        'id', validators=[Required(), Length(1, 100)]
    )
    title = StringField(
        'title', validators=[Required(), Length(1, 100)]
    )
    description = StringField(
        'description', validators=[Required(), Length(1, 100)]
    )

    submit = SubmitField('submit')
class searchForm(Form):
    title=StringField('title',validators=[Required()])
    submit = SubmitField('submit')


@app.route("/todo/api/v1.0/home",methods=['GET'])
def home():
    return render_template('home.html')



@app.route("/todo/api/v1.0/",methods=['GET'])
def index():
    todo = mongo.db.todo
    data = todo.find({}).count()
    if (data == 0):
        return "data not found"
    else:
        d = {}
        data=mongo.db.todo.find({})
        for i in data:

            d[i['id']] = {"id": i["id"],"title": i["title"],"description":i["description"],"done": bool(i["done"])}
        
        return jsonify(d)


@app.route("/todo/api/v1.0/Insert",methods=['GET','POST'])
def Insert():
    form=InsertForm(request.form)
    if request.method=='POST':
       id = request.form['id']
       title=request.form['title']
       description=request.form['description']
       done = bool(request.form["submit"])
       count=mongo.db.todo.find({}).count()
       
       mongo.db.todo.insert({'id':id,'title':title,'description':description,'done':done })
       return "Successfully add"
                  
       
    return render_template('Insert.html',form=form)

@app.route("/todo/api/v1.0/Search",methods=['GET','POST'])
def search():
    form=searchForm(request.form)
    if request.method=='POST':
      
       if mongo.db.todo.find({'id':request.form['id']}):
           record=mongo.db.todo.find({'id':request.form['id']})
           d=[]
           for i in record:
              d.append({'id':i['id'],'title':i['title'],'description':i['description'],'done':i['done'] })
           return jsonify({'record':d})
       else:
           return "ID does not exist"

    return render_template('Search.html')

@app.route("/todo/api/v1.0/Update", methods=['GET','POST','PUT'])

def update():
    if request.method=='POST':
        id1=request.form['id1']
        id2=request.form['id2']
        title = request.form['title']
        description=request.form['description']
        done = bool(request.form["submit"])
        if mongo.db.todo.find({'id':id1}):
            update_query = mongo.db.todo.update_one({'id':id1},{'$set':{"id": id2,"title": title,"description": description,"done": done}})
            return ("successfully updated.")
        else: 
           return 'title does not exist' 
    

    return render_template('Update.html')
    
    



@app.route("/todo/api/v1.0/delete", methods=['GET','POST','DELETE'])
def delete():
    if request.method == 'POST':
        id = request.form['id']
        mongo.db.todo.delete_one({'id': id})
        return "deleted"
        


    return render_template('Delete.html')

if __name__=='__main__':
    app.run(debug=True)
