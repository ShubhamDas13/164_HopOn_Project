from flask import Flask,render_template,request,redirect
from random import randint,choice
import requests
from connector import *
from datetime import datetime,date
global signup_customer,login_customer,signup_driver,login_driver
id_customer = 0
id_driver = 0
id_trip = 0
insertqueryDriver = ""
# id_customer = "39385812"

signup_customer = 0
login_customer = 0
signup_driver = 0
login_driver = 0

vehicle = {
    'reg_no':None,
    'type':None,
    'total_seats':None,
    'model':None,
    'model_year':None,
    'prime':None,
    'AC':None,
    'Wifi':None
}


driver = {
    'id':None,
    'name':None,
    'age':None,
    'phone_no':None,
    'aadhar':None,
    'exp':None,
    'rating':None,
    'earnings':None,
    'reg_no':None,
}

customer = {
    'id':None,
    'name':None,
    'phone_no':None,
    'email':None,
    'age':None,
    'mode_of_payment':None
}

trip = {
    'id':None,
    'booking_time':None,
    'date':None,
    'pickup_loc':None,
    'drop_loc':None,
    'distance':None,
    'pickup_time':None,
    'waiting_time':None,
    'total_time':None,
    'done':None,
    'ongoing':None
}

transactions = {
    'id':None,
    'customer_id':None,
    'driver_id':None,
    'mode_of_payment':None,
    'Coupon':'Trip50'

}

host = "localhost"
user = "root"
password = "pass"
db = "HOPON_DB"
print("Connecting to the server")
connect = ConnectMySQL(host,user,password,db)
print("Connected")

# temp_password = "123456789"

# print("Query 1")

# print("Output:")
# query1 = "select * from NOTIFICATIONS;"
# data = giveQuery(connect, query1)
# for i in data:
#     print(i)

app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def index():
    if login_customer == 1:
        return Home()
    else:
        return render_template('index.html')
    

@app.route('/customerSignup', methods = ['POST','GET'])
def customerSignup():
    global login_customer,signup_customer
    signup_customer = 1
    login_customer = 0
    return render_template('customerSignup.html')

@app.route('/customerLogin', methods = ['POST','GET'])
def customerLogin():
    global login_customer,signup_customer
    login_customer = 1
    signup_customer = 0
    return render_template('customerLogin.html')

@app.route('/driverSignup', methods = ['POST','GET'])
def driverSignup():
    global login_driver,signup_driver
    signup_driver = 1
    login_driver = 0
    return render_template('driverSignup.html')

# insertquery = "insert into CUSTOMERS (Customer_ID, C_name, C_age, email_ID, C_Phone_No, C_Mode_of_payment) values (39385812, 'Godart Rosenvasser', 70, 'grosenvassers@sina.com.cn', 6423445474, 'CASH/UPI');"
@app.route('/driverLogin', methods = ['POST','GET'])
def driverLogin():
    global login_driver,signup_driver
    login_driver = 1
    signup_driver = 0
    return render_template('driverLogin.html')


@app.route('/bookTrip', methods = ['POST','GET'])
def bookTrip():
    global login_customer,signup_customer
    if login_customer == 0 and signup_customer == 0:
        return customerSignup()
    global id_customer
    if request.method == 'POST':
        if signup_customer == 1:
            query = "select Customer_ID from CUSTOMERS;"
            Customerids = giveQuery(connect, query)
            l = []
            for i in Customerids:
                l.append(i[0])
            id_cus = max(l)+1
            customer['id'] = str(id_cus)
            customer['name'] = request.form.get("name")
            customer['phone_no'] = str(request.form.get("phone"))
            customer['email'] = request.form.get("email")
            customer['age'] = str(request.form.get("age"))
            customer['mode_of_payment'] = request.form.get("payment")
            insertquery = "insert into CUSTOMERS (Customer_ID, C_name, C_age, email_ID, C_Phone_No, C_Mode_of_payment) values ("+customer['id']+",'"+customer['name']+"',"+customer['age']+",'"+customer['email']+"','"+customer['phone_no']+"','"+customer['mode_of_payment']+"');"
            insertQuerry(connect, insertquery)
            signup_customer = 1
            id_customer = id_cus
        elif login_customer==1:
            query = "select Customer_ID from CUSTOMERS;"
            cusdata = giveQuery(connect, query)
            id_fetch = request.form.get("driver-id")
            print(id_fetch)
            l = []
            for i in cusdata:
                l.append(int(i[0]))
            print(l)
        
            query = "select * from CUSTOMERS where Customer_ID="+str(id_fetch)+";"
            cus_data = giveQuery(connect, query)
            customer['id'] = cus_data[0][0]
            customer['name'] = cus_data[0][1]
            customer['age'] = cus_data[0][2]
            customer['email'] = cus_data[0][3]
            customer['phone_no'] = cus_data[0][4]
            customer['mode_of_payment'] = cus_data[0][5]
            id_customer = id_fetch
            login_customer =1

    return render_template('bookTrip.html')


@app.route('/transaction', methods = ['POST','GET'])
def transaction():
    global id_trip
    if request.method == 'POST':
        pickup = request.form.get("pickup")
        drop = request.form.get("drop")
        query = "select Trip_ID from TRIP;"
        Tripids = giveQuery(connect, query)
        l = []
        for i in Tripids:
            l.append(int(i[0]))
        id_tr = max(l)+1
        trip_id = id_tr
        id_trip = trip_id
        time = datetime.now()
        d = date.today()
        Booking_time = time.strftime('%H:%M')
        drophr = int(time.strftime('%H'))+randint(1,3)
        if drophr>=24:
            drophr-=24
        dropminute = randint(0,59)
        drop_time = str(drophr)+":"+str(dropminute)
        Waiting_time = randint(5,15)
        PickUP_Time =time.strftime('%H')+":"+str(int(time.strftime('%M'))+Waiting_time)
        picklist = PickUP_Time.split(':')
        droplist = drop_time.split(':')
        triptime = 0
        if droplist[0]>picklist[0]:
            triptime+=(int(droplist[0])-int(picklist[0]))*60 + int(droplist[1]) - int(picklist[1])
        isOngoning = 1
        isDone = 0
        Distance = triptime*40 #speed
        Total_time = Waiting_time+triptime
        Trip_date = d.strftime("%d/%m/%Y")
        insertquery = "insert into TRIP (Trip_ID, Booking_time, Trip_date, Pickup_Location, Drop_Location, Distance, Pickup_time, Waiting_time, Total_time, isOngoing, isDone) values ('"+str(trip_id)+"','"+Booking_time+"','"+Trip_date+"','"+pickup+"','"+drop+"','"+str(Distance)+"','"+PickUP_Time+"','"+str(Waiting_time)+"','"+str(Total_time)+"','"+str(isOngoning)+"','"+str(isDone)+"');"
        updatequery1 = "UPDATE TRIP SET isDone = 1 WHERE Trip_ID ="+ str(id_trip)+";"
        updatequery2 = "UPDATE TRIP SET isOngoing = 0 WHERE Trip_ID ="+ str(id_trip)+";"
        
        insertQuerry(connect, insertquery)
        insertQuerry(connect, updatequery1)
        insertQuerry(connect, updatequery2)

    return render_template('transaction.html')
# insert into TRIP (Trip_ID, Booking_time, Trip_date, Pickup_Location, Drop_Location, Distance, Pickup_time, Waiting_time, Total_time, isOngoing, isDone) values (200, '22:00', '14/08/2022', 'South Africa', 'Russia', 21045.64, '0:07', 8, 76, 0, 1);



@app.route('/driver', methods = ['POST','GET'])
def driverHome():
    return render_template('driver.html')

@app.route('/vehicle', methods = ['POST','GET'])
def vehicleHome():
    if request.method == 'POST':
        global id_driver, insertqueryDriver
        if signup_driver == 1:
            query = "select Driver_ID from DRIVER;"
            driverids = giveQuery(connect, query)
            l = []
            for i in driverids:
                l.append(int(i[0]))
            id_dr = max(l)+1
            id_driver =  id_dr
            print(id_driver)
            driver['id'] = str(id_driver)
            driver['name'] = request.form.get("name")
            driver['age'] = request.form.get("age")
            driver['phone_no'] = request.form.get("phone-number")
            driver['aadhar'] = request.form.get("adhar-number")
            driver['exp'] = request.form.get("experience")
            driver['earning'] = request.form.get("earnings")
            driver['reg_no'] = request.form.get("vehicle-registration-number")
            insertqueryDriver = "insert into DRIVER (Driver_ID, D_name, Age, Phone_no, Aadhar_no, Experience, Rating, Earnings, Registration_no) values ("+driver['id']+",'"+driver['name']+"',"+driver['age']+","+driver['phone_no']+","+driver['aadhar']+",'"+driver['exp']+"',5,"+driver['earning']+",'"+driver['reg_no']+"');"
            # insertQuerry(connect, insertquery)
        elif login_driver == 1:
            query = "select Driver_ID from DRIVER;"
            driverdata = giveQuery(connect, query)
            dr_id = request.form.get("driver-id")
            if dr_id not in driverdata:
                return redirect("/driverSignup")
            else:
                query = "select * from DRIVER where Driver_ID="+str(dr_id)+";"
                driverdata = giveQuery(connect, query)
                driver['id'] = query[0][0]
                driver['name'] = query[0][1]
                driver['age'] = query[0][2]
                driver['phone_no'] = query[0][3]
                driver['aadhar'] = query[0][4]
                driver['exp'] = query[0][5]
                driver['rating'] = query[0][6]
                driver['earnings'] = query[0][7]
                driver['reg_no'] = query[0][8]
    return render_template('vehicle.html')

@app.route('/Done', methods = ['POST','GET'])
def Done():
    global id_customer
    if request.method == "POST":
        mot = request.form.get("payment")
        query = "select Transaction_ID from TRANSACTIONS;"
        Tripids = giveQuery(connect, query)
        l = []
        for i in Tripids:
            l.append(int(i[0]))
        id_tr = max(l)+1
        Transaction_ID = str(id_tr)

        TripID_tran = str(id_trip)
        CustomerID_tran = str(id_customer)
        print(id_customer)
        query = "select Driver_ID from DRIVER;"
        drid = giveQuery(connect, query)
        for j in drid:
            l.append(j[0])
        DriverID_tran = str(choice(l))
        Mode_of_Payment = mot
        Coupon = 'Trip50'
        insertquery = "insert into TRANSACTIONS (Transaction_ID, TripID_tran, CustomerID_tran, DriverID_tran, Mode_of_Payment, Coupon) values ("+Transaction_ID+",'"+TripID_tran+"',"+CustomerID_tran+","+DriverID_tran+",'"+Mode_of_Payment+"','"+Coupon+"');"
        insertQuerry(connect, insertquery)
        print(insertquery)
    return render_template('ThankYou.html')
#insert into TRANSACTIONS (Transaction_ID, TripID_tran, CustomerID_tran, DriverID_tran, Mode_of_Payment, Coupon) values (4380258544, '1', 20367371, 1716874, 'CASH/UPI', 'Trip50');

# vehicle = {
#     'reg_no':None,
#     'type':None,
#     'total_seats':None,
#     'model':None,
#     'model_year':None,
#     'prime':None,
#     'AC':None,
#     'Wifi':None
# }


@app.route('/DriverRegisterDone', methods = ['POST','GET'])
def DriverRegisterDone():
    if request.method == "POST":
        vehicle['reg_no'] = request.form.get("regno")
        vehicle['type'] = request.form.get("vehicle-type")
        vehicle['total_seats'] = request.form.get("seats")
        vehicle['model'] = request.form.get("model")
        vehicle['model_year'] = request.form.get("model-year")
        print(request.form.get("prime-ride"))
        if request.form.get("prime-ride") == None:
            vehicle['prime'] = "false"
        else:
            vehicle['prime'] = "true"
        if request.form.get("ac") == None:
            vehicle['AC'] = "false"
        else:
            vehicle['AC'] = "true"
        if request.form.get("wifi") == None:
            vehicle['Wifi'] = "false"
        else:
            vehicle['Wifi'] = "true"
        insertquery = "insert into VEHICLES (Reg_no, V_type, Total_Seats, V_Model, Model_Year, Prime_ride, Air_Conditioned, Wifi) values ('"+vehicle['reg_no']+"','"+vehicle['type']+"',"+vehicle['total_seats']+",'"+vehicle['model']+"','"+vehicle['model_year']+"',"+vehicle['prime']+","+vehicle['AC']+","+vehicle['Wifi']+");"
        insertQuerry(connect, insertquery)
        insertQuerry(connect, insertqueryDriver)
    return render_template('ThankYouDriver.html')

@app.route('/Home', methods = ['POST','GET'])
def Home():
    return render_template('Home.html')

@app.route('/UserProfile', methods = ['POST','GET'])
def UserProfile():
    data = []
    q = "select * from CUSTOMERS where Customer_ID="+id_customer+";"
    d = giveQuery(connect,q)
    for i in d[0]:
        data.append(i)
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        email = request.form.get("email")
        Phone = request.form.get("phone")
        dele = request.form.get("delete")
        if dele == "delete":
            delquery = "DELETE FROM CUSTOMERS WHERE Customer_ID = '"+id_customer +"';"
            insertQuerry(connect, delquery)
        if name != data[1]:
            upquery = "UPDATE CUSTOMERS SET C_name = "+name+" WHERE Customer_ID = '"+ id_customer+"';"
            insertQuerry(connect, upquery)
        if age != data[4]:
            upquery = "UPDATE CUSTOMERS SET C_age = "+age+" WHERE Customer_ID = '"+ id_customer+"';"
            insertQuerry(connect, upquery)
        if email != data[3]:
            upquery = "UPDATE CUSTOMERS SET email_ID = "+email+" WHERE Customer_ID = '"+ id_customer+"';"
            insertQuerry(connect, upquery)
        if Phone != data[2]:
            upquery = "UPDATE CUSTOMERS SET C_Phone_No = "+Phone+" WHERE Customer_ID = '"+ id_customer +"';"
            insertQuerry(connect, upquery)

# insertquery = "insert into CUSTOMERS (Customer_ID, C_name, C_age, email_ID, C_Phone_No, C_Mode_of_payment) values (39385812, 'Godart Rosenvasser', 70, 'grosenvassers@sina.com.cn', 6423445474, 'CASH/UPI');"
    return render_template('userProfile.html', userdata=data)

if __name__=="__main__":
    app.run(debug=True)
    
