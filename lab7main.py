from flask import Flask, session ,render_template, request, redirect, g, url_for
import os
import getconfig
import ospfconfig
import configparser
import test
app = Flask(__name__)
app.secret_key=os.urandom(24)
@app.route("/")
def index():
    html= "<html><title> LAB 7 automation </title><body> Choose an option </body><br><a href=/getconfig> Get configuration </a><br><a href=/conf_ospf> Login and configure ospf </a></html>"

    return html

@app.route("/getconfig")
def getcon():
    a=getconfig.getconf()
    return(a)

@app.route("/conf_ospf")
def conf_ospf():
    try:
        session.pop('user', None)
    except:
        pass
    return render_template("conf_index.html")

@app.route("/ospf_ping")
def ospf_ping():
    config=configparser.ConfigParser()
    config.read("test.conf")
    status=ospfconfig.ospf_ping(config["R1"]["username"],config["R1"]["password"],config["R1"]["ip"],config["R2"]["username"],config["R2"]["password"],config["R2"]["ip"])
    if(status==1):
        return "<html><body> Successful pings between r1 and R3 </body></html>"
    else:
        return "<html><body> PIngs not successful </html></body>"



@app.route("/ospf_r1", methods=['GET','POST'])
def ospf_r1():
    print("The request method is:"+str(request.method))
    print("The request type is:"+str(type(request.method)))
    print("The request is :"+str(request))
    if(request.method=="GET"):
        #session.pop('user', None)
        print("Get request")
        return render_template("login_r1.html")
    if request.method == 'POST':
        print("Post request")
        session.pop('user', None)
        config=configparser.ConfigParser()
        config.read("test.conf")
        username=config["R1"]["username"]
        password=config["R1"]["password"]

        if request.form['r1_user']==username and request.form['r1_pass']==password:
            session['user']=request.form['r1_user']
            return render_template("conf_r1.html")
        else:
            return redirect(url_for('ospf_r1'))
    else:
        return str(request.method)

@app.route("/ospf_r2",methods=['GET','POST'])
def ospf_r2():
    #return "Configuring OSPF on R2"
    print("The request method is:"+str(request.method))
    print("The request type is:"+str(type(request.method)))
    print("The request is :"+str(request))
    if(request.method=="GET"):
        #session.pop('user', None)
        print("Get request")
        return render_template("login_r2.html")
    if request.method == 'POST':
        print("Post request")
        session.pop('user', None)
        config=configparser.ConfigParser()
        config.read("test.conf")
        username=config["R2"]["username"]
        password=config["R2"]["password"]

        if request.form['r2_pass']==password and request.form['r2_user']==username:
            session['user']=request.form['r2_user']
            return render_template("conf_r2.html")
        else:
            return redirect(url_for('ospf_r2'))
    else:
        return str(request.method)


@app.route("/ospf_r3",methods=['GET','POST'])
def ospf_r3():
    #return "Configuring OSPF on R3"
    print("The request method is:"+str(request.method))
    print("The request type is:"+str(type(request.method)))
    print("The request is :"+str(request))
    if(request.method=="GET"):
        #session.pop('user', None)
        print("Get request")
        return render_template("login_r3.html")
    if request.method == 'POST':
        print("Post request")
        session.pop('user', None)
        config=configparser.ConfigParser()
        config.read("test.conf")
        username=config["R3"]["username"]
        password=config["R3"]["password"]

        if request.form['r3_pass']==password and request.form['r3_user']==username:
            session['user']=request.form['r3_user']
            return render_template("conf_r3.html")

        else:
            return redirect(url_for('ospf_r3'))
    else:
        return str(request.method)





@app.route("/ospf_r4",methods=['GET','POST'])
def ospf_r4():
    print("The request method is:"+str(request.method))
    print("The request type is:"+str(type(request.method)))
    print("The request is :"+str(request))
    if(request.method=="GET"):
        #session.pop('user', None)
        print("Get request")
        return render_template("login_r4.html")
    if request.method == 'POST':
        print("Post request")
        session.pop('user', None)
        config=configparser.ConfigParser()
        config.read("test.conf")
        username=config["R4"]["username"]
        password=config["R4"]["password"]

        if request.form['r4_pass']==password and request.form['r4_user']==username:
            session['user']=request.form['r4_user']
            return render_template("conf_r4.html")
        else:
            return redirect(url_for('ospf_r4'))
    else:
        return str(request.method)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']



@app.route("/done_conf_r1",methods=['GET','POST'])
def conf_r1():
    print("The request is ------>"+request.method)
    if g.user:
        if(request.method=="POST"):
            print("YOLO")
            config=configparser.ConfigParser()
            config.read('test.conf')
            print("Here now")
            physical_ip=config["R1"]["ip"]
            print("ascfefwfwrgrvfs wgrgverg rg wgfr grgrg")
            test.test()
            print("physicalip:"+physical_ip)
            print("loopback:"+request.form['r1_lo'])
            print("process id:"+request.form['r1_pid'])
            print("router id:"+request.form['r1_id'])
            print("area id:"+request.form['r1_aid'])
            print("username:"+request.form['r1_user'])
            print("password:"+request.form['r1_pass'])
            config=configparser.ConfigParser()
            config.read("test.conf")
            username=config["R1"]["username"]
            password=config["R1"]["password"]
            ospfconfig.conf_ospf(physical_ip,request.form['r1_lo'],request.form['r1_pid'],request.form['r1_id'],request.form['r1_aid'],username,password,1)
            print("Function executed")
            return redirect(url_for('conf_ospf'))

            #return ("OSPF configured on r1 with rid:"+str(request.form['r1_pid']))
        
    return render_template("conf_index.html")

@app.route("/done_conf_r2",methods=['GET','POST'])
def conf_r2():
    if g.user:
        if(request.method=="POST"):
            config=configparser.ConfigParser()
            config.read("test.conf")
            physical_ip=config["R2"]["ip"]
            config=configparser.ConfigParser()
            config.read("test.conf")
            username=config["R2"]["username"]
            password=config["R2"]["password"]
            ospfconfig.conf_ospf(physical_ip,request.form['r2_lo'],request.form['r2_pid'],request.form['r2_id'],request.form['r2_aid'],username,password,2)
            return redirect(url_for('conf_ospf'))
            #return ("Configured r2 with rid:"+str(request.form['r2_pid']))

    return render_template("conf_index.html")

@app.route("/done_conf_r3",methods=['GET','POST'])
def conf_r3():
    if g.user:
        if(request.method=="POST"):
            config=configparser.ConfigParser()
            config.read("test.conf")
            physical_ip=config["R3"]["ip"]
            config=configparser.ConfigParser()
            config.read("test.conf")
            username=config["R3"]["username"]
            password=config["R3"]["password"]

            ospfconfig.conf_ospf(physical_ip,request.form['r3_lo'],request.form['r3_pid'],request.form['r3_id'],request.form['r3_aid'],username,password,3)        
            return redirect(url_for('conf_ospf'))
            #return ("Configured r3 with rid:"+str(request.form['r3_pid']))

    return render_template("conf_index.html")


@app.route("/done_conf_r4",methods=['GET','POST'])
def conf_r4():
    if g.user:
        if(request.method=="POST"):
            config=configparser.ConfigParser()
            config.read("test.conf")
            physical_ip=config["R4"]["ip"]
            config=configparser.ConfigParser()
            config.read("test.conf")
            username=config["R4"]["username"]
            password=config["R4"]["password"]
            ospfconfig.conf_ospf(physical_ip,request.form['r4_lo'],request.form['r4_pid'],request.form['r4_id'],request.form['r4_aid'],username,password,4)
            return redirect(url_for('conf_ospf'))
            #return ("Configured r4 with rid:"+str(request.form['r4_pid']))        
    return render_template("conf_index.html")


@app.route('/logout')
def dropsession():
    session.pop('user', None)
    return "Logged Out"

@app.route("/ospf_neighbor")
def ospf_neighbor():
    config=configparser.ConfigParser()
    config.read("test.conf") 
    R4_ip=config["R4"]["ip"]
    R4_user=config["R4"]["username"]
    R4_pass=config["R4"]["password"]
    R2_ip=config["R2"]["ip"]
    R2_user=config["R2"]["username"]
    R2_pass=config["R2"]["password"]
    ospfconfig.ospf_neighbhor(R4_ip,R4_user,R4_pass,4)
    ospfconfig.ospf_neighbhor(R2_ip,R2_user,R2_pass,2)
    
    #a="<html><body> R2 <br>"+str(r2_neighbors)+"<br> R4 <br>"+str(r4_neighbors)+"</body></html>"
    filenames=["nbr_router4.txt","nbr_router2.txt" ]
    with open('templates/nbr.html', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())
    return render_template("nbr.html")



if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)





