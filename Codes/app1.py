from flask import Flask, session, redirect, url_for, escape, request, render_template
import MySQLdb
import os
from werkzeug import generate_password_hash,check_password_hash

app = Flask(__name__)

db = MySQLdb.connect(host="localhost", user="root", passwd="dl9CP@7088", db="siddharth")
cur = db.cursor()
done=0
cur.execute("SET FOREIGN_KEY_CHECKS=0")
def dexecute (str):		
	try:
		cur.execute(str)
		db.commit()
	except:
		db.rollback()

@app.route('/')
def home():
	return render_template('Home.html')

@app.route('/home/doctorlogin/doctorhome')
def doctorindex():
	if 'username' in session:
		username_session=escape(session['username'].capitalize())
		cur.execute("select First_Name from Doctor where Doctor_ID=%d" %int(username_session))
		First_name=cur.fetchone()[0]
		cur.execute("""select Last_Name from Doctor where Doctor_ID=%d""" %int(username_session))
		last_name=cur.fetchone()[0]
		cur.execute("""select Sex from Doctor where Doctor_ID=%d""" %int(username_session))
		sex=cur.fetchone()[0]
		cur.execute("""select Age from Doctor where Doctor_ID=%d""" %int(username_session))
		age=cur.fetchone()[0]
		cur.execute("""select E_mail from Doctor where Doctor_ID=%d""" %int(username_session))
		Email=cur.fetchone()[0]
		cur.execute("""select Phone_Number from Doctor where Doctor_ID=%d""" %int(username_session))
		phoneno=cur.fetchone()[0]
		cur.execute("""select Department from Doctor where Doctor_ID=%d""" %int(username_session))
		Department=cur.fetchone()[0]
		cur.execute("""select Shift from Doctor where Doctor_ID=%d""" %int(username_session))
		shift=cur.fetchone()[0]
		cur.execute("""select patient.Patient_ID,patient.First_Name from patient join Consult on patient.Patient_ID=Consult.Patient_ID where Consult.Doctor_ID=%d"""%int(username_session))
		data=cur.fetchall()
		return render_template('doctorhome.html',username=username_session,firstname=First_name,lastname=last_name,sex=sex,age=age,Email=Email,phno=phoneno,department=Department,shift=shift,data=data)

@app.route('/home/doctorlogin',methods=['GET', 'POST'])
def doclogin():
	error=None
	if 'username' in session:
		return redirect(url_for('doctorindex'))
	if request.method=='POST':
		usernameDOC=request.form['username']
		passwordDOC=request.form['password']
		cur.execute("SELECT COUNT(1) From Doctor where Doctor_ID = %d" %int(usernameDOC))
		if cur.fetchone()[0]:
			cur.execute("SELECT password FROM docPass where Doctor_ID= %d" %int(usernameDOC))
			data=cur.fetchone()[0]
			if (check_password_hash(data,passwordDOC)):
				session['username']=usernameDOC
				return redirect(url_for('doctorindex'))
			else:
				error="Invalid password"
		else:
			error="Invalid username"
	return render_template('doctor.html',error=error)

@app.route('/home/patientlogin/patienthome')
def patindex():
	if 'username' in session:
		username_session=escape(session['username'].capitalize())
		cur.execute("select First_Name from patient where Patient_ID=%d" %int(username_session))
		First_name=cur.fetchone()[0]
		cur.execute("""select Last_Name from patient where Patient_ID=%d""" %int(username_session))
		last_name=cur.fetchone()[0]
		cur.execute("""select Sex from patient where Patient_ID=%d""" %int(username_session))
		sex=cur.fetchone()[0]
		cur.execute("""select Age from patient where Patient_ID=%d""" %int(username_session))
		age=cur.fetchone()[0]
		cur.execute("""select E_mail from patient where Patient_ID=%d""" %int(username_session))
		Email=cur.fetchone()[0]
		cur.execute("""select Phone_Number from patient where Patient_ID=%d""" %int(username_session))
		phoneno=cur.fetchone()[0]
		cur.execute("""select Disease from patient where Patient_ID=%d""" %int(username_session))
		disease=cur.fetchone()[0]
		cur.execute("""select Room_Number from allocation where Patient_ID=%d""" %int(username_session))
		room_no=cur.fetchone()[0]
		cur.execute("""select Doctor.Doctor_ID,Doctor.First_Name from Doctor join Consult on Doctor.Doctor_ID=Consult.Doctor_ID where Consult.Patient_ID=%d"""%int(username_session))
		data=cur.fetchall()
		return render_template('patienthome.html',username=username_session,firstname=First_name,lastname=last_name,sex=sex,age=age,Email=Email,phno=phoneno,disease=disease,roomno=room_no,data=data)

@app.route('/home/patientlogin',methods=['GET','POST'])
def patlogin():
	error=None
	if 'username' in session:
		return redirect(url_for('patindex'))
	if request.method=='POST':
		usernamepat=request.form['username']
		passwordpat=request.form['password']
		cur.execute("SELECT COUNT(1) From patient where Patient_ID = %d" %int(usernamepat))
		if cur.fetchone()[0]:
			cur.execute("SELECT password FROM patPass where Patient_ID= %d" %int(usernamepat))
			data=cur.fetchone()[0]
			if (check_password_hash(data,passwordpat)):
				session['username']=usernamepat
				return redirect(url_for('patindex'))
			else:
				error="Invalid password"
		else:
			error="Invalid username"
	return render_template('patient.html',error=error)

@app.route('/signed')
def signed():
	done=0
	return render_template('done.html',done=done)
	
@app.route('/home/signup/successful',methods=['GET','POST'])
def psigned():
	error=None
	if request.method=='POST':
		pid=request.form['pid']
		first_name=request.form['pFirstname']
		last_name=request.form['pLastname']
		sex=request.form['sex']
		age=request.form['age']
		email=request.form['email']
		ph_no=request.form['number']
		disease=request.form['disease']
		room_no=request.form['room_number']
		date_add=request.form['date_add']
		consult_doc=request.form['docCons']
		bill=request.form['billnum']
		consC=request.form['Consultation_Charge']
		medC=request.form['Medication_Charge']
		roomC=request.form['Room_Charge']
		bdate=request.form['billdate']
		cur.execute("SELECT COUNT(1) From patient where Patient_ID = %d" %int(pid))
		if cur.fetchone()[0]:
			error="ID already exists"
		else:
			cur.execute("select count(1) from room where Room_Number = %d" %int(room_no))
			if cur.fetchone()[0]:
				cur.execute("""select count(1) from room where Room_Number=%d and Room_Status="Not Available" """ %int(room_no))
				if cur.fetchone()[0]:
					error="Room is already full"
				else:
					cur.execute("select count(1) from Doctor where Doctor_ID=%d " %int(consult_doc))
					if cur.fetchone()[0]:
						cur.execute("""insert into patient values(%d,"%s","%s","%s",%d,"%s",%d,"%s")""" %(int(pid),first_name,last_name,sex,int(age),email,int(ph_no),disease))
						cur.execute("""insert into In_patient values(%d,"%s",%d)""" %(int(pid),date_add,int(room_no)))
						cur.execute("""insert into allocation values(%d,%d)"""%(int(pid),int(room_no)))
						cur.execute("""insert into Consult values(%d,%d)"""%(int(pid),int(consult_doc)))
						cur.execute("""insert into bill values(%d,%d,"%s",%d,%d,%d,%d)"""%(int(bill),int(pid),bdate,int(consC),int(roomC),int(medC),int(consC)+int(roomC)+int(medC)))
						done=0
						return redirect(url_for('signed'))
					else:
						error="Doctor does not exist"
			else:
				error="Room doesnot exist"						
	return render_template('psignin.html',error=error)


@app.route('/home/patient/update',methods=['GET','POST'])
def patientUp():
	error=None
	if request.method=='POST':
		pid=request.form['pid']
		pwd=request.form['passwd']
		cur.execute("""select count(1) from In_patient where Patient_ID=%d"""%int(pid))
		if cur.fetchone()[0]:
			cur.execute("SELECT password FROM patPass where Patient_ID= %d" %int(pid))
			data=cur.fetchone()[0]
			if (check_password_hash(data,pwd)):
				val=request.form['attr']
				if val=='Fname':
					session['k']=0
				elif val=='Lname':
					session['k']=1
				elif val=='sex':
					session['k']=2
				elif val=='age':
					session['k']=3
				elif val=='Email':
					session['k']=4
				elif val=='Phone number':
					session['k']=5
				elif val=='Disease':
					session['k']=6
				elif val=='Room_no':
					session['k']=7
				elif val=='consdoc':
					session['k']=8
				elif val=='passw':
					session['k']=9
				session['user']=pid
				return redirect(url_for('values'))
			else:
				error="incorrect password"
		else:
			error="invalid username"
	return render_template('update.html',error=error)

@app.route('/home/patient/update/values',methods=['GET','POST'])
def values():
	error=None
	if request.method=='POST':
		if session['k']==0:
			val=request.form['Fname']
			cur.execute("""update patient set First_Name="%s" where Patient_ID=%d""" %(val,int(session['user'])))
			session['user']=None
			db.commit()
			done=1
			return render_template('done.html',done=done)
		elif session['k']==1:
			val=request.form['Lname']
			cur.execute("""update patient set Last_Name="%s" where Patient_ID=%d""" %(val,int(session['user'])))
			session['user']=None
			db.commit()
			done=1
			return render_template('done.html',done=done)
		elif session['k']==2:
			val=request.form['sex']
			cur.execute("""update patient set Sex="%s" where Patient_ID=%d""" %(val,int(session['user'])))
			session['user']=None
			db.commit()
			done=1
			return render_template('done.html',done=done)
		elif session['k']==3:
			val=request.form['age']
			cur.execute("""update patient set age=%d where Patient_ID=%d""" %(int(val),int(session['user'])))
			session['user']=None
			db.commit()
			done=1
			return render_template('done.html',done=done)
		elif session['k']==4:
			done=1
			val=request.form['Email']
			cur.execute("""update patient set E_mail="%s" where Patient_ID=%d""" %(val,int(session['user'])))
			session['user']=None
			db.commit()
			return render_template('done.html',done=done)
		elif session['k']==5:
			val=request.form['Phone number']
			done=1
			cur.execute("""update patient set Phone_number=%d where Patient_ID=%d""" %(int(val),int(session['user'])))
			db.commit()
			session['user']=None
			return render_template('done.html',done=done)
		elif session['k']==6:
			val=request.form['Disease']
			done=1
			cur.execute("""update patient set Disease="%s" where Patient_ID=%d""" %(val,int(session['user'])))
			session['user']=None
			db.commit()
			return render_template('done.html',done=done)
		elif session['k']==7:
			val=request.form['Room_no']
			cur.execute("select count(1) from room where Room_Number = %d" %int(val))
			if cur.fetchone()[0]:
				cur.execute("""select count(1) from room where Room_Number=%d and Room_Status="Not Available" """ %int(val))
				if cur.fetchone()[0]:
					error="Room is already full"
				else:
					done=1
					cur.execute("""update allocate set Room_Number=%d where Patient_ID=%d""" %(int(val),int(session['user'])))
					cur.execute("""update In_patient set Room_Number=%d where Patient_ID=%d"""%(int(val),int(session['user'])))
					db.commit()
					session['user']=None
					return render_template('done.html',done=done)
			else:
				error="Room doesnot exist"
		elif session['k']==8:
			val=request.form['consdoc']
			cur.execute("""update Consult set Doctor_ID=%d where Patient_ID=%d""" %(int(val),int(session['user'])))
			session['user']=None
			db.commit()
			done=1
			return render_template('done.html',done=done)
		elif session['k']==9:
			val=request.form['pass']
			cur.execute("""update patPass set password="%s" where Patient_ID=%d""" %(generate_password_hash(val,method="sha1"),int(session['user'])))
			db.commit()
			session['user']=None
			done=1
			return render_template('done.html',done=done)
	return render_template('updateval.html',k=session['k'])


@app.route('/home/appointment',methods=['GET','POST'])
def appointment():
	error=None
	if request.method=='POST':
		username=request.form['username']
		password=request.form['password']
		doc=request.form['docID']
		cur.execute("""select count(1) from patient where Patient_ID=%d""" %int(username))
		if cur.fetchone()[0]:
			cur.execute("""select count(1) from Doctor where Doctor_ID=%d""" %int(doc))
			if cur.fetchone()[0]:
				cur.execute("SELECT password FROM patPass where Patient_ID= %d" %int(username))
				data=cur.fetchone()[0]
				if (check_password_hash(data,password)):
					cur.execute("""insert into Consult values(%d,%d)"""%(int(username),int(doc)))
					db.commit()
					return render_template('appointment1.html')
				else:
					error="Enter a valid password "
			else:
				error="Enter a valid doctor id"
		else:
			error="Enter a valid username"
	return render_template('appointment.html',error=error)

@app.route('/logout')
def logout():
	error=None
	session.pop('username',None)
	return redirect(url_for('home'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)

db.close()
