from flask import Flask, render_template, request, flash
import sqlite3
import csv
import hashlib
import random


app = Flask(__name__)

host = 'http://127.0.0.1:5000/'



# set as part of the config
SECRET_KEY = 'many random bytes'

# or set directly on the app
app.secret_key = 'many random bytes'


connection = sqlite3.connect('database.db',  check_same_thread=False)
cursor = connection.cursor()
cursor2 = connection.cursor()
transactionID = 2000



#populate Address Table (address_id,zipcode,street_num,street_name)
cursor.execute('CREATE TABLE IF NOT EXISTS Address (address_id TEXT PRIMARY KEY, zipcode INTEGER, street_num INTEGER, street_name TEXT)')
file = open('Address.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Address (address_id,zipcode,street_num,street_name) VALUES(?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Buyers Table (email,first_name,last_name,gender,age,home_address_id,billing_address_id)
cursor.execute('CREATE TABLE IF NOT EXISTS Buyers (email TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, gender TEXT, age INTEGER, home_address_id TEXT, billing_address_id TEXT, FOREIGN KEY(email) REFERENCES Users (email), FOREIGN KEY(home_address_id) REFERENCES Address (address_ID), FOREIGN KEY(billing_address_id) REFERENCES Address (address_ID))')
file = open('Buyers.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Buyers (email,first_name,last_name,gender,age,home_address_id,billing_address_id) VALUES(?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Categories Table (parent_category,category_name)
cursor.execute('CREATE TABLE IF NOT EXISTS Categories (parent_category TEXT,category_name TEXT PRIMARY KEY)')
file = open('Categories.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Categories (parent_category,category_name) VALUES(?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Credit_Cards Table credit_card_num,card_code,expire_month,expire_year,card_type,Owner_email
cursor.execute('CREATE TABLE IF NOT EXISTS Credit_Cards (credit_card_num TEXT PRIMARY KEY,card_code INTEGER,expire_month INTEGER,expire_year INTEGER,card_type TEXT,Owner_email TEXT,  FOREIGN KEY(Owner_email) REFERENCES Users (email))')
file = open('Credit_Cards.csv')
contents = csv.reader(file)
insert_records = "INSERT OR IGNORE INTO Credit_Cards (credit_card_num,card_code,expire_month,expire_year,card_type,Owner_email) VALUES (?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Local_Vendors (Email,Business Name,Business Address ID,Customer Service Number)
cursor.execute('CREATE TABLE IF NOT EXISTS Local_Vendors (email TEXT PRIMARY KEY,business_name TEXT,business_address_ID TEXT,customer_service_number TEXT,  FOREIGN KEY(email) REFERENCES Users (email))')
file = open('Local_Vendors.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Local_Vendors (email,business_name,business_address_ID,customer_service_number) VALUES (?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Orders (Transaction_ID,Seller_Email,Listing_ID,Buyer_Email,Date,Quantity,Payment)
cursor.execute('CREATE TABLE IF NOT EXISTS Orders (Transaction_ID TEXT PRIMARY KEY,Seller_Email TEXT,Listing_ID INTEGER,Buyer_Email TEXT,Date TEXT,Quantity INTEGER,Payment INTEGER, FOREIGN KEY(Seller_email) REFERENCES Sellers (email), FOREIGN KEY(Buyer_Email) REFERENCES Buyers (email), FOREIGN KEY(Listing_ID) REFERENCES Product_Listing (Listing_ID))')
file = open('Orders.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Orders (Transaction_ID,Seller_Email,Listing_ID,Buyer_Email,Date,Quantity,Payment) VALUES (?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Product_Listing (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity)
cursor.execute('CREATE TABLE IF NOT EXISTS Product_Listing (Seller_Email TEXT,Listing_ID TEXT PRIMARY KEY,Category TEXT,Title TEXT,Product_Name TEXT,Product_Description TEXT,Price TEXT,Quantity INTEGER, FOREIGN KEY(Seller_email) REFERENCES Users (email), FOREIGN KEY(Category) REFERENCES Categories (category_name))')
file = open('Product_Listing.csv', errors='ignore',encoding='utf8' )
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Product_Listing (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Ratings Table (Buyer_Email TEXT,Seller_Email TEXT,Rating INTEGER,Rating_Desc TEXT)
cursor.execute('CREATE TABLE IF NOT EXISTS Ratings (Buyer_Email TEXT,Seller_Email TEXT,Rating INTEGER,Rating_Desc TEXT, FOREIGN KEY(Seller_email) REFERENCES Sellers (email), FOREIGN KEY(Buyer_Email) REFERENCES Buyers (email))')
file = open('Ratings.csv')
contents = csv.reader(file)
insert_records = "INSERT INTO Ratings (Buyer_Email,Seller_Email,Rating,Rating_Desc) VALUES (?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Reviews Table (Buyer_Email,Seller_Email,Listing_ID,Review_Desc)
cursor.execute('CREATE TABLE IF NOT EXISTS Reviews (Buyer_Email TEXT ,Seller_Email TEXT,Listing_ID TEXT ,Review_Desc TEXT, FOREIGN KEY(Seller_email) REFERENCES Sellers (email), FOREIGN KEY(Buyer_Email) REFERENCES Buyers (email), FOREIGN KEY(Listing_ID) REFERENCES Product_Listing (Listing_ID), PRIMARY KEY(Buyer_Email, Listing_ID))')
file = open('Reviews.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Reviews (Buyer_Email,Seller_Email,Listing_ID,Review_Desc) VALUES (?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Sellers Table (email,routing_number,account_number,balance)
cursor.execute('CREATE TABLE IF NOT EXISTS Sellers (email TEXT PRIMARY KEY,routing_number TEXT,account_number INTEGER,balance INTEGER,  FOREIGN KEY(email) REFERENCES Users (email))')
file = open('Sellers.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Sellers (email,routing_number,account_number,balance) VALUES (?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Users table (email,password)
cursor.execute('CREATE TABLE IF NOT EXISTS Users (email TEXT PRIMARY KEY, password TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS Users2 (email TEXT PRIMARY KEY, hashed_password TEXT)')
file = open('Users.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Users (email, password) VALUES(?, ?)"
cursor.executemany(insert_records, contents)

file.close()

#populate Zipcode_Info (zipcode,city,state_id,population,density,county_name,timezone)
cursor.execute('CREATE TABLE IF NOT EXISTS Zipcode_Info (zipcode TEXT PRIMARY KEY,city TEXT,state_id TEXT,population,density,county_name,timezone)')
file = open('Zipcode_Info.csv')
contents = csv.reader(file)
insert_records = "INSERT OR REPLACE INTO Zipcode_Info (zipcode,city,state_id,population,density,county_name,timezone) VALUES (?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_records, contents)
file.close()

#populate Soldout (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity)
cursor.execute('CREATE TABLE IF NOT EXISTS Soldout (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity)')
cursor = connection.execute('SELECT * FROM Product_Listing where Quantity = 0')
soldout = cursor.fetchall()
for i in range(0, len(soldout)):
    cursor.execute('INSERT INTO Soldout (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity) VALUES (?,?,?,?,?,?,?,?)', (soldout[i][0], soldout[i][1],soldout[i][2],soldout[i][3],soldout[i][4],soldout[i][5],soldout[i][6],soldout[i][7],))
cursor.execute(' DELETE FROM Product_Listing WHERE quantity = 0')
print(soldout)
file.close()

#create removed table 
cursor.execute('CREATE TABLE IF NOT EXISTS Removed (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity,Date)')
#create sellerapplication table 
cursor.execute('CREATE TABLE IF NOT EXISTS applySeller (buyer_email)')
# Committing the changes
cursor.execute('CREATE TABLE IF NOT EXISTS applyCategory (category)')
# Committing the changes
connection.commit()
 
# closing the database connection


#Route to main page
@app.route('/')
def home():
    #hash passwords and restore them
    cursor = connection.execute('SELECT email, password FROM Users')
    for row in cursor.fetchall():
        line = row
        for item in line:
                test1 = line[0]
                unhashed_password= line[1]
                hashed_password = hashlib.sha256(unhashed_password.encode('utf-8')).hexdigest()
        cursor2.execute('INSERT INTO Users2(email,hashed_password) VALUES (?,?)', (test1, hashed_password))
        #print(test1 + "..." + unhashed_password + "..." + hashed_password)
    cursor.execute("DROP TABLE Users")
    cursor.execute("ALTER TABLE Users2 RENAME TO Users")
    connection.commit()
    return render_template("login.html")

#Route to main page
@app.route('/login')
def home2():
    return render_template("login.html")

#Route to info page
@app.route('/info')
def func1():
    #Retreive info of buyer
    cursor = connection.execute('SELECT first_name FROM Buyers where email = ?', (username, ))
    first_name = str(cursor.fetchall())
    first_name = first_name[3:-4]
    cursor = connection.execute('SELECT last_name FROM Buyers where email = ?', (username, ))
    last_name = str(cursor.fetchall())
    last_name = last_name[3:-4]
    cursor = connection.execute('SELECT age FROM Buyers where email = ?', (username, ))
    age = str(cursor.fetchall())
    age = age[2:4]
    cursor = connection.execute('SELECT gender FROM Buyers where email = ?', (username, ))
    gender = str(cursor.fetchall())
    gender = gender[3:-4]
    cursor = connection.execute('SELECT home_address_id FROM Buyers where email = ?', (username, ))
    home_address_id = str(cursor.fetchall())
    home_address_id = home_address_id[3:-4]
    cursor = connection.execute('SELECT zipcode,street_num,street_name FROM Address where address_ID = ?', (home_address_id, ))
    list = cursor.fetchall()
    print(list)
    zippy = list[0][0]
    address_num = list[0][1]
    street_address = list[0][2]
    cursor = connection.execute('SELECT city,state_id FROM Zipcode_Info where zipcode = ?', (zippy, ))
    list = cursor.fetchall()
    city = list[0][0]
    state_id = list[0][1]
    cursor = connection.execute('SELECT credit_card_num FROM Credit_Cards where Owner_email = ?', (username, ))
    card_num = str(cursor.fetchall())
    card_num = card_num[14:-4]
    return render_template("info.html", var1=username, var2=first_name, var3=last_name, var4=age, var5=gender, var6=zippy, var7=address_num, var8=street_address, var9=city, var10= state_id, var11= card_num)

#Route to info page
@app.route('/listings')
def func2():
    categories = []
    sub1 = []
    sub2 = []
    #Get categories
    cursor = connection.execute('SELECT category_name FROM Categories where parent_category = "Root"')
    #categories = cursor.fetchall()
    categories = cursor.fetchall()
    cursor = connection.execute('SELECT category_name FROM Categories where parent_category = "Root"')
    for i in range(0,len(categories)):
        categories[i] = str(categories[i])[2:-3]
    print(categories)
    for j in range(0, len(categories)):
        cursor = connection.execute('SELECT category_name FROM Categories where parent_category = ?', (categories[j], ))
        temp = cursor.fetchall()
        for obj in range(0,len(temp)):
            next = temp[obj]
            next = str(next)[2:-3]
            sub1.append(next)
    for k in range(0, len(sub1)):
         cursor = connection.execute('SELECT category_name FROM Categories where parent_category = ?', (sub1[k], ))
         temp = cursor.fetchall()
         for obj2 in range(0,len(temp)):
            next2 = temp[obj2]
            next2 = str(next2)[2:-3]
            sub2.append(next2)
    print(sub1)
    print(sub2)
    return render_template("listings.html", categories=categories, sub1=sub1, sub2=sub2)

#Route to info page
@app.route('/apply')
def func3():
    return render_template("apply.html")


@app.route('/', methods=['POST'])
def func4():
    global username 
    username = request.form['Username']
    password = request.form['Password']
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    #print("Attempted Username = " + username)
    #print("Attempted Password = " + password)
    cursor = connection.execute('SELECT email, hashed_password FROM Users where email = ? AND hashed_password = ?', (username,password))
    checkTuple = cursor.fetchall()
    print(checkTuple)
    print("Number of return results: " +str(len(checkTuple)))
    #check if valid login
    if(str(len(checkTuple))=="0"):
        print("USERNAME or PASSWORD INCORRECT")
        app.secret_key='12345'
        flash('Thank you for registering')
        return render_template('loginFail.html')
    if username == "admin":
        return render_template('admin_homepage.html')
    if(str(len(checkTuple))=="1"):
        print("SUCCESS")
        cursor = connection.execute('SELECT email FROM Buyers where email = ?', (username,))
        checkBuyerStatus = cursor.fetchall()
        buyerStatus = str(len(checkBuyerStatus))
        cursor = connection.execute('SELECT email FROM Sellers where email = ?', (username,))
        checkSellerStatus = cursor.fetchall()
        sellerStatus = str(len(checkSellerStatus))
        #print(checkBuyerStatus)
        #check status of user logging in
        if(str(len(checkBuyerStatus))=="1"):
            print("This User is a Buyer")
            print(buyerStatus)
            print(sellerStatus)
        if(str(len(checkSellerStatus))=="1"):
            print("This User is a Seller")
            print(buyerStatus)
            print(sellerStatus)
        
        if sellerStatus == "1":
            if buyerStatus == "1":
                return render_template('seller_homepage.html')
            else:
                return render_template('seller_homepage.html')
        else:
            return render_template('buyer_homepage.html')

    #user_check = cursor.fetchone()[0]
    #password_check = cursor.fetchone()[1]

    #print("the username to check: " + user_check)
    #print("the password to check: " + password_check)
    
    #print(cursor.fetchall())
    return render_template('login.html')


@app.route('/')
def func5():
    return render_template("login.html")

@app.route('/main')
def func6():
    return render_template("buyer_homepage.html")

@app.route('/testtt', methods=['POST'])
def func7():
    #retreive category information selected
    category = request.form.get('category', '')
    subcategory1 = request.form.get('sub1', '')
    subcategory2 = request.form.get('sub2', '')
    print(category)
    print(subcategory1)
    print(subcategory2)
    #reset filters
    categories = []
    sub1 = []
    sub2 = []
    ratings = []
    cursor = connection.execute('SELECT category_name FROM Categories where parent_category = "Root"')
    #categories = cursor.fetchall()
    categories = cursor.fetchall()
    cursor = connection.execute('SELECT category_name FROM Categories where parent_category = "Root"')
    for i in range(0,len(categories)):
        categories[i] = str(categories[i])[2:-3]
   # print(categories)
    for j in range(0, len(categories)):
        cursor = connection.execute('SELECT category_name FROM Categories where parent_category = ?', (categories[j], ))
        temp = cursor.fetchall()
        for obj in range(0,len(temp)):
            next = temp[obj]
            next = str(next)[2:-3]
            sub1.append(next)
    for k in range(0, len(sub1)):
         cursor = connection.execute('SELECT category_name FROM Categories where parent_category = ?', (sub1[k], ))
         temp = cursor.fetchall()
         for obj2 in range(0,len(temp)):
            next2 = temp[obj2]
            next2 = str(next2)[2:-3]
            sub2.append(next2)
    #end filtering
    #retreive product information:
    if(subcategory2!="none"):
        print("Sub2 was selected")
        cursor = connection.execute('SELECT * FROM Product_Listing where Category = ?', (subcategory2, ))
        products = cursor.fetchall()

        #get rating and products
        averageList = []
        for i in range(0,len(products)):
            print(products[i][0])
            cursor = connection.execute('SELECT Rating FROM Ratings where Seller_Email = ?', (products[i][0], ))
            ratings = cursor.fetchall()
            for i in range(0, len(ratings)):
                ratings[i] = str(ratings[i])[1:-2]
            print(ratings)
            total = 0
            for j in range(0, len(ratings)):
                total = total + int(ratings[j])
            if len(ratings) != 0:
                average = total / len(ratings)
            else:
                average = "No Ratings Yet"
            averageList.append(average)
            print(average)
        print(averageList)

        return render_template("listings2.html", products=products, len=len(products), categories=categories, sub1=sub1, sub2=sub2, averageList=averageList)
    else:
        if(subcategory1!="none"):
            print("Sub2 was none")
            cursor = connection.execute('SELECT * FROM Product_Listing where Category = ?', (subcategory1, ))
            products = cursor.fetchall()
            averageList = []
            for i in range(0,len(products)):
                print(products[i][0])
                cursor = connection.execute('SELECT Rating FROM Ratings where Seller_Email = ?', (products[i][0], ))
                ratings = cursor.fetchall()
                for i in range(0, len(ratings)):
                    ratings[i] = str(ratings[i])[1:-2]
                print(ratings)
                total = 0
                for j in range(0, len(ratings)):
                    total = total + int(ratings[j])
                if len(ratings) != 0:
                    average = total / len(ratings)
                else:
                    average = "No Ratings Yet"
                averageList.append(average)
                print(average)
            print(averageList)
            return render_template("listings2.html", products=products, len=len(products), categories=categories, sub1=sub1, sub2=sub2, averageList=averageList) 
        else:
            print("Sub1 and Sub2 are empty")
            cursor = connection.execute('SELECT * FROM Product_Listing where Category = ?', (category, ))
            products = cursor.fetchall()
            averageList = []
            for i in range(0,len(products)):
                print(products[i][0])
                cursor = connection.execute('SELECT Rating FROM Ratings where Seller_Email = ?', (products[i][0], ))
                ratings = cursor.fetchall()
                for i in range(0, len(ratings)):
                    ratings[i] = str(ratings[i])[1:-2]
                print(ratings)
                total = 0
                for j in range(0, len(ratings)):
                    total = total + int(ratings[j])
                if len(ratings) != 0:
                    average = round(total / len(ratings), 1)
                else:
                    average = "No Ratings Yet"
                averageList.append(average)
                print(average)
            print(averageList)

            return render_template("listings2.html", products=products, len=len(products), categories=categories, sub1=sub1, sub2=sub2, averageList=averageList) 


    return render_template("listings2.html", categories=categories, sub1=sub1, sub2=sub2)

@app.route('/placeOrder', methods=['POST'])
def func8():
    #function for placing an order and storing information
    global purchasedProduct
    purchasedProduct = request.form.get('product')
    print("The buyer has selected to buy product: " + purchasedProduct)
    purchasedProduct = purchasedProduct[-4:]
    print("Buyer: " + username)
    print("Product ID:" + purchasedProduct)
    if purchasedProduct[0]== " ":
        purchasedProduct = purchasedProduct[2:]
    if purchasedProduct[0]== "#":
        purchasedProduct = purchasedProduct[1:]
    print("Product ID:" + purchasedProduct)
    cursor = connection.execute('SELECT * FROM Product_Listing where Listing_ID = ?', (int(purchasedProduct), ))
    sellerInfo = cursor.fetchall()
    cursor = connection.execute('SELECT credit_card_num FROM Credit_Cards where Owner_email = ?', (username, ))
    card_num = str(cursor.fetchall())
    card_num = card_num[14:-4]
    return render_template("orderConfirm.html", username=username, product_id=sellerInfo[0][1], product_name=sellerInfo[0][3], seller_email=sellerInfo[0][0], price=sellerInfo[0][6], card_num = card_num)


@app.route('/PurchaseConfirmed')
def func9():
    #do transaction stuff
    transactionID = random.randint(2000,9999)
    cursor = connection.execute('SELECT * FROM Product_Listing where Listing_ID = ?', (int(purchasedProduct), ))
    transactionInfo = cursor.fetchall()
    print("Current Quantity = " + str(transactionInfo[0][7]))
    print("New Quantity should be = " + str(transactionInfo[0][7]-1))
    cursor.execute('UPDATE Product_Listing SET Quantity = ? WHERE Listing_ID = ?', (transactionInfo[0][7]-1, purchasedProduct, ))
    print(username + " bought Product ID:" + purchasedProduct + " from " + transactionInfo[0][0])
    cursor.execute('INSERT INTO Orders(Transaction_ID,Seller_Email,Listing_ID,Buyer_Email,Date,Quantity,Payment) VALUES (?,?,?,?,?,?,?)', (transactionID, transactionInfo[0][0], transactionInfo[0][1], username, "4/1/22", 1, transactionInfo[0][6]))
    cursor = connection.execute('SELECT * FROM Product_Listing where Quantity = 0')
    soldout = cursor.fetchall()
    for i in range(0, len(soldout)):
        cursor.execute('INSERT INTO Soldout (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity) VALUES (?,?,?,?,?,?,?,?)', (soldout[i][0], soldout[i][1],soldout[i][2],soldout[i][3],soldout[i][4],soldout[i][5],soldout[i][6],soldout[i][7],))
    cursor.execute(' DELETE FROM Product_Listing WHERE quantity = 0')
    connection.commit()
    return render_template("Confirmation.html")

@app.route('/review')
def func10():
    tempy2 = []
    cursor = connection.execute('SELECT * FROM Orders where Buyer_Email = ?', (username, ))
    orders = cursor.fetchall()
    print(orders)
    #retreive review information
    for i in range(0, len(orders)):
        cursor = connection.execute('SELECT * FROM Orders where Listing_ID = ?', (orders[i][2], ))
        tempy = cursor.fetchall()
        print(tempy)
        tempy2.append(tempy[0][3])
    print(orders)
    print(tempy2)
    return render_template("review.html", orders=orders, len=len(orders), tempy2=tempy2)

@app.route('/infoSeller')
def func11():
    #retreive seller information
    cursor = connection.execute('SELECT * FROM Sellers where email = ?', (username, ))
    sellerInfo = cursor.fetchall()
    print(sellerInfo)
    cursor = connection.execute('SELECT Rating FROM Ratings where Seller_Email = ?', (username, ))
    ratings = cursor.fetchall()
    for i in range(0, len(ratings)):
        ratings[i] = str(ratings[i])[1:-2]
    print(ratings)
    total = 0
    for j in range(0, len(ratings)):
        total = total + int(ratings[j])
    print(total)
    if len(ratings) != 0:
        average = total / len(ratings)
    else:
        average = "No Ratings Yet"
    return render_template("infoSeller.html", sellerInfo=sellerInfo, average=average)

@app.route('/sellerHome')
def func12():
    return render_template("seller_homepage.html")

@app.route('/newListing')
def func13():
    cursor = connection.execute('SELECT DISTINCT category_name FROM Categories')
    categories = sorted(cursor.fetchall())
    for i in range(0, len(categories)):
        categories[i] = str(categories[i])[2:-3]
    return render_template("newListing.html", username=username, categories=categories)

@app.route('/confirmListing', methods=['POST'])
def func14():
    #publish a new listing functionality:
    category = request.form.get('category', '')
    title = request.form.get('title', '')
    product_name = request.form.get('product_name', '')
    product_description = request.form.get('product_description', '')
    price = request.form.get('price', '')
    quantity = request.form.get('quantity', '')
    Listing_ID = random.randint(3000,9999)
    cursor.execute('INSERT INTO Product_Listing(Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity) VALUES (?,?,?,?,?,?,?,?)', (username, Listing_ID, category, title, product_name, product_description, price, quantity))
    connection.commit()
    print(username + category + title + product_name + product_description + price + str(quantity))
    return render_template("seller_homepage.html")

@app.route('/removeListing')
def func15():
    #remove listing functionality
    cursor = connection.execute('SELECT * FROM Product_Listing where Seller_Email = ?', (username, ))
    listed = cursor.fetchall()
    print(listed)
    cursor = connection.execute('SELECT * FROM Orders where Seller_Email = ?', (username, ))
    sold = cursor.fetchall()
    return render_template("removeListing.html", listed=listed, len=len(listed), sold=sold, len2=len(sold))

@app.route('/review', methods=['POST'])
def func16():
    order = request.form.get('order', '')
    print(username + " is leaving review for " + order)
    return render_template("productReview.html", order=order)

@app.route('/productReview', methods=['POST'])
def func17():
    #new review functionality
    productReview = request.form.get('review', '')
    Listing_ID = request.form.get('productReview', '')
    Listing_ID = Listing_ID[-4:]
    if Listing_ID[0]== " ":
        Listing_ID = Listing_ID[2:]
    if Listing_ID[0]== "#":
        Listing_ID = Listing_ID[1:]
    cursor = connection.execute('SELECT Seller_Email FROM Orders where Listing_ID = ?', (Listing_ID, ))
    seller_email = str(cursor.fetchone())
    seller_email = seller_email[2:-3]
    try:
        cursor.execute('INSERT INTO Reviews(Buyer_Email,Seller_Email,Listing_ID,Review_Desc) VALUES (?,?,?,?)', (username, seller_email, Listing_ID, productReview))
    except sqlite3.IntegrityError:
        print("Product has already been reviewed")
        return render_template("reviewError.html")
    print(username + seller_email + Listing_ID + productReview)
    connection.commit()
    return render_template("buyer_homepage.html")

@app.route('/reviewSeller', methods=['POST'])
def func18():
    #render reatings page:
    seller = request.form.get('seller', '')
    print(username + " is leaving review for " + seller)
    return render_template("sellerReview.html", seller=seller)

@app.route('/sellerReview', methods=['POST'])
def func19():
    #new ratings functionality:
    rating = request.form.get('rating', '')
    seller = request.form.get('sellerReview', '')
    seller = seller[12:]
    print("Rating for seller: " + str(rating))
    print(seller)
    cursor.execute('INSERT INTO Ratings(Buyer_Email,Seller_Email,Rating,Rating_Desc) VALUES (?,?,?,?)', (username, seller, rating, "null"))
    return render_template("buyer_homepage.html")

@app.route('/remove', methods=['POST'])
def func20():
    product = request.form.get('product', '')
    product = str(product)[16:]
    print("Product Listing to Remove: " + product)
    cursor = connection.execute('SELECT * FROM Product_Listing where Listing_ID = ?', (product, ))
    remove = cursor.fetchall()
    print(remove)
    #Save removed product information for admin
    cursor.execute('INSERT INTO Removed (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity,Date) VALUES (?,?,?,?,?,?,?,?,?)', (remove[0][0],remove[0][1],remove[0][2],remove[0][3],remove[0][4],remove[0][5],remove[0][6],remove[0][7],"4/4/22"))
    cursor.execute(' DELETE FROM Product_Listing WHERE Listing_ID = ?', (str(product), ))
    connection.commit()
    return render_template("seller_homepage.html")

@app.route('/readReview', methods=['POST'])
def func21():
    #fetch reviews:
    product = request.form.get('reviewButton', '')
    product = str(product)[22:]
    print("Product Reviews of " + str(product))
    cursor = connection.execute('SELECT * FROM Reviews where Listing_ID = ?', (product, ))
    reviews = cursor.fetchall()
    print(reviews)
    return render_template("readReview.html", reviews=reviews, len=len(reviews))

@app.route('/allProduct')
def func22():
    cursor = connection.execute('SELECT * FROM Product_Listing')
    products = cursor.fetchall()
    return render_template("allProducts.html", products=products, len=len(products))

@app.route('/removedProduct')
def func23():
    #fetch removed products
    cursor = connection.execute('SELECT * FROM Removed')
    products = cursor.fetchall()
    return render_template("removedProducts.html", products=products, len=len(products))

@app.route('/applySeller', methods=['POST'])
def func24():
    #allow for buyers to apply to sell
    cursor.execute('INSERT INTO applySeller (buyer_email) VALUES (?)', (username, ))
    connection.commit()
    return render_template("buyer_homepage.html") 

@app.route('/approveSellers')
def func25():
    #function for admin to approve sellers
    cursor = connection.execute('SELECT * FROM applySeller')
    applicants = cursor.fetchall()
    for i in range(0,len(applicants)):
        applicants[i] = str(applicants[i])[2:-3]
    connection.commit()
    return render_template("approveSellers.html", applicants=applicants, len=len(applicants)) 

@app.route('/applyCategory')
def func26():
    return render_template("applyCategory.html")

@app.route('/applyCat', methods=['POST'])
def func27():
    #function for sellers to request new categories
    category = request.form.get('category', '')
    print(category)
    cursor.execute('INSERT INTO applyCategory (category) VALUES (?)', (category, ))
    connection.commit()
    return render_template("seller_homepage.html")

@app.route('/approveCategory')
def func28():
    #function for admin to approve new categories
    cursor = connection.execute('SELECT * FROM applyCategory')
    categories = cursor.fetchall()
    for i in range(0,len(categories)):
        categories[i] = str(categories[i])[2:-3]
    connection.commit()
    return render_template("approveCategory.html", categories=categories, len=len(categories)) 

@app.route('/newpassword', methods=['POST'])
def func29():
    #change password function
    newpassword = request.form.get('newpassword', '')
    print(newpassword)
    newpassword = hashlib.sha256(newpassword.encode('utf-8')).hexdigest()
    cursor.execute('UPDATE Users SET hashed_password = ? WHERE email = ?', (newpassword, username ))
    return render_template("buyer_homepage.html")



if __name__ == "__main__":
    
    app.run()





# TO DO Still:
# - Add go home button for view listings
# - Emoji on info page
# - Extra Credit

