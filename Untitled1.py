from flask import Flask,render_template,request,redirect,url_for,jsonify
import mysql.connector
import json

app = Flask(__name__)
db = mysql.connector.connect(user='root',password='',host='127.0.0.1',database='chatbot')
cur = db.cursor()


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    username = str(request.form['username'])
    password = str(request.form['password'])
    cursor = db.cursor()   
    cursor.execute("SELECT password FROM admin_table WHERE username ='"+username+"'")
    user = cursor.fetchone()
    if len(user) is 1:
        return render_template("admin.html") #redirect(url_for("admin"))
    else:
        return ("FAIL")
    
    
@app.route("/admin", methods=['GET', 'POST'])
def home():
    return render_template("admin.html")

@app.route("/admin/view", methods=['GET', 'POST'])
def look():
    cursor = db.cursor()
    cursor.execute("SELECT question FROM question_table")
    data = cursor.fetchall()
    return render_template("view.html", data=data)

@app.route("/admin/answer", methods=['GET', 'POST'])
def ans():    
    with open('intents.json', encoding= "utf8") as data:
        data = json.load(data) 
    return render_template("answer.html", data=data)

@app.route("/admin/answer/add",methods=["GET","POST"])
def add():
    if request.method == "POST":        
        tag = request.form['tag']
        patterns = request.form['patterns']
        responses = request.form['responses']
        filename = 'C:/Users/navya/Desktop/rasa/intents.json'
        jsn =[]
        with open(filename, 'r',encoding="utf8") as f:
            data = json.load(f)
            for i in range(len(data['intents'])):
                #print(data['intents']);
                val= data['intents'][i]
                if val['tag'] == tag:
                    val["tag"] = tag
                    val["patterns"] = patterns
                    val["responses"] = responses
                jsn.append(val)
            if i==len(data['intents'])-1:
                jsval={
                    "tag" : tag,
                    "patterns" :patterns,
                    "responses" : responses
                }
                jsn.append(jsval)
                #print(jsn)
            data['intents']=jsn
            with open(filename, 'w',encoding="utf8") as f1:
                json.dump(data,f1,indent=3)       
    return render_template("add.html")

    
if __name__ == "__main__":    
    app.run(debug=True)