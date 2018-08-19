from flask import Flask, jsonify,json,request,render_template
from flask_pymongo import PyMongo
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from wtforms import Form, StringField, SubmitField


app = Flask(__name__)

app.config['MONGO_DBNAME']='ahmer'
app.config['MONGO_URI']='mongodb://zunair:pass123@ds217138.mlab.com:17138/ahmer'
mongo = PyMongo(app)


class InsertForm(Form):
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
 
    data = mongo.db.todo.find({}).count()
    if (data == 0):
        return "data not found"
    else:
        d = {}
        data=mongo.db.todo.find({})
        for i in data:

            d[i['id']] = {"id": i["id"],"title": i["title"],"description":i["description"],    "done": bool(i["done"])}
        
        return jsonify(d)


@app.route("/todo/api/v1.0/Insert",methods=['GET','POST'])
def Insert():
    form=InsertForm(request.form)
    if request.method=='POST':
       title=request.form['title']
       description=request.form['description']
       done = bool(request.form["submit"])
       count=mongo.db.todo.find({}).count()
       
       mongo.db.todo.insert({'id':count+1,'title':title,'description':description,'done':done })
       return "Successfully add"
                  
       
    return render_template('Insert.html',form=form)

@app.route("/todo/api/v1.0/Search",methods=['GET','POST'])
def search():
    form=searchForm(request.form)
    if request.method=='POST':
      
       if mongo.db.todo.find({'title':request.form['title']}):
           record=mongo.db.todo.find({'title':request.form['title']}) 
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
        title1=request.form['title1']
        title2=request.form['title2']
        description=request.form['description']
        done = bool(request.form["submit"])
        if mongo.db.todo.find({'title':title1}):    
            update_query = mongo.db.todo.update_one({'title':title1},{'$set':{"title": title2,"description": description,"done": done}})
            return ("successfully updated.")
        else: 
           return 'title does not exist' 
    

    return render_template('Update.html')
    
    



@app.route("/todo/api/v1.0/delete", methods=['GET','POST','DELETE'])
def delete():
    if request.method == 'POST':
        title = request.form['title']
        mongo.db.todo.delete_one({'title': title})
        return "deleted"
        


    return render_template('Delete.html')

if __name__=='__main__':
    app.run(debug=True)
