from flask import Flask, render_template, request, session, jsonify
import pymongo
from datetime import datetime
import json




with open("confi.json", "r") as c:
    data=json.load(c)
params=data["parameter"]

app = Flask(__name__)
app.secret_key = "super-secret-key"

myclient = pymongo.MongoClient("mongodb+srv://gautammauryamail:R44GrJoMauAjN2yS@cluster0.hk9okct.mongodb.net/")
db = myclient["mydatabase"]

contact_db = db.contacts
post_db = db.posts

# def insert_contacts():
#     contact_db.insert()






@app.route("/")
@app.route("/home")
def home_html():
    start=datetime.now()
    posts=post_db.find()[:params["no_of_post"]]
    print("time different:-",datetime.now()-start)
    print("time start:-",start)
    print("time later:-",datetime.now())
    print("server url:-", request.url)
    
    return render_template("home.html", params=params,posts=posts)


@app.route("/post/<string:post_slug>", methods=["GET"])
def post_detail(post_slug):
    # slug=post_slug
    post=post_db.find_one({"slug":post_slug})
    return render_template("postdetail.html",params=params,post=post)




@app.route("/login", methods=["GET","POST"])
def login():
    if("user" in session and session["user"]==params["admin_uname"]):
        posts=post_db.find()
        return render_template("dasboard.html",params=params,posts=posts)
        
    elif request.method == "POST":
        uname= request.form.get("uname")
        password=request.form.get("p_word")
        if uname==params["admin_uname"] and password==params["admin_password"]:
            session["user"]=uname
            params["session_user"]=True
            
            posts=post_db.find()
            return render_template("dasboard.html",params=params,posts=posts)
        elif uname!=params["admin_uname"] or password!=params["admin_password"]:
            error_mess="username or password is not correct!"
            return render_template("login.html",mess=error_mess, params=params)
        else:
            return render_template("login.html", params=params)
    
        # return render_template("login.html", params=params)

    else:
        return render_template("login.html", params=params)


@app.route("/about")
def about():
    return render_template("about.html",params=params)



@app.route("/post")
def post_route():
    posts=post_db.find()[:params["no_of_post"]]
    return render_template("post.html", params=params,posts=posts)
    


@app.route("/contact", methods=['GET', 'POST'])
def contact():

    if request.method == "POST":
        #  entry message to database
        '''first (name) is to store data ,second ("name") is comes from web page'''
        clint_data={
            "name": request.form.get("name"),
            "phone" : request.form.get("phone"),
            "email" : request.form.get("email"),
            "message" : request.form.get("message"),
            "time" : datetime.now()
            }
        contact_db.insert_one(clint_data)

    return render_template("contact.html", params=params)






@app.route("/dasboard")
def dasboard():
    posts=post_db.find()
    return render_template("dasboard.html",params=params,posts=posts)




@app.route("/logout")
def logout():
    # Remove the "user" key from the session
    session.pop("user", None)
    params["session_user"]=False
    # return render_template("home.html",params=params)
    return home_html()


@app.route("/api", methods=["GET"])
def api():
    filter={"_id":0, "s_no":1,"title":1,"name":1,"slug":1,"content":1,"date":1, "tagline":1}
    posts = post_db.find({},filter)
    
    post_data = [post for post in posts]
    print("post data...", len(post_data))
    print("post data...", type(post_data))
    return jsonify(post_data)



@app.route("/add_post", methods=["POST"])
def add_post():
    if request.method == "POST":
        #  entry message to database
        '''first (name) is to store data ,second ("name") is comes from web page'''
        post_data={
            "name": request.form.get("name"),
            "phone" : request.form.get("phone"),
            "email" : request.form.get("email"),
            "message" : request.form.get("message"),
            "time" : datetime.now()
            }
        response = post_db.insert_one(post_data)
        return "response"
       
    
    
    
    


if __name__ == "__main__":
    app.run(debug=True)
    