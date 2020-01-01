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
    usernam = str(request.form['username'])
    passwor = str(request.form['password'])
    cursor = db.cursor() 
    cursor.execute("SELECT password FROM admin_table WHERE username ='"+usernam+"'")
    user = cursor.fetchone()
    print(user)
    def convertTuple(tup): 
        str1 =  ''.join(tup) 
        return str1
  
# Driver code
    if user is not None:
        tuple = user 
        str1 = convertTuple(tuple) 
        print(str1)
        if str1 == passwor:
            return render_template("admin.html")
        else:
            return render_template("login.html") 
    else:
        return render_template("login.html") 


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
        filename = 'C:\\chatbot\\rasa\\intents.json'
        jsn =[]
        a = True
        with open(filename, 'r',encoding="utf8") as f:
            data = json.load(f)
            for i in range(len(data['intents'])):
                #print(data['intents']);
                val= data['intents'][i]
                if val['tag'] == tag:
                    a =False
                    me = patterns
                    he = responses
                    val["responses"].append(he)
                    val["patterns"].append(me)
                jsn.append(val)
            

            if i==len(data['intents'])-1 and a == True:
                jsval={
                    "tag" : tag,
                    "patterns" :[patterns],
                    "responses" : [responses]
                }
                jsn.append(jsval)
                #print(jsn)
            data['intents']=jsn
            with open(filename, 'w',encoding="utf8") as f1:
                json.dump(data,f1,indent=3)       
    return render_template("add.html")

    
if __name__ == "__main__":    
    app.run(debug=True)