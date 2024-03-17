from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from helpers import login_required, valid_amount
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL
from datetime import date as dt, datetime
import calendar

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///expense.db")

@app.route("/")
@login_required
def index():

    user_categories = db.execute("""SELECT DISTINCT(category_name), SUM(amount) AS amount FROM expense JOIN category
                                 ON expense.category_id = category.id WHERE expense.user_id = ?
                                 GROUP BY expense.category_id""", session["user_id"])
    cat = [cat["category_name"] for cat in user_categories]
    amt_list = [int(amt["amount"]) for amt in user_categories]

    return render_template("index.html", cat_list=cat, amt_list=amt_list)

@app.route("/sort/week", methods=["GET"])
@login_required
def sortweek():
    if request.method == "GET":

        currDate = dt.today()
        starting_day = currDate.day - 6
        starting_year = currDate.year
        starting_month = currDate.month
        if starting_day <= 0:
            starting_month = currDate.month - 1
            if starting_month == 0:
                starting_year -= 1
                starting_month += 12
            lastDay = calendar.monthrange(starting_year, starting_month)[1]
            starting_day = lastDay + starting_day
        
        starting_date = dt(starting_year, starting_month, starting_day)
        sDate = str(starting_date.day) + " " + calendar.month_abbr[starting_date.month] + " " + str(starting_date.year)
        eDate = str(currDate.day) + " " + currDate.strftime("%b") + " " + str(currDate.year)
        currDate = str(currDate)
        
        res = db.execute("""SELECT DISTINCT(category_name), SUM(amount) AS amount FROM expense JOIN category
                            ON expense.category_id = category.id WHERE expense.user_id = ? AND expense.date
                            BETWEEN ? AND ? GROUP BY expense.category_id ORDER BY amount DESC""", session["user_id"], starting_date, currDate)
        
        tt_expense = db.execute("""SELECT SUM(amount) AS amount FROM expense WHERE user_id = ? AND date
                                BETWEEN ? AND ?;""", session["user_id"], starting_date, currDate)[0]['amount']
        
        tt_expense = "{:.2f}".format(float(tt_expense))
        cat = [cat["category_name"] for cat in res]
        amt_list = [int(amt["amount"]) for amt in res]
        data = { 'cat' : cat, 'amt' : amt_list, 'sDate' : sDate, 'eDate' : eDate, 'tt_expense' : tt_expense }

        return jsonify(data)

@app.route("/sort/month", methods=["GET"])
@login_required
def sortmonth():
    
    if request.method == "GET":

        currDate = dt.today()
        starting_day = currDate.day
        starting_month = currDate.month - 1
        starting_year = currDate.year
        if starting_month == 0:
            starting_month += 12
            starting_year -= 1
        lastDay = calendar.monthrange(starting_year, starting_month)[1]
        if starting_day > lastDay:
            starting_day = 1
        
        startDate = dt(starting_year, starting_month, starting_day)
        sDate = startDate.strftime("%d") + " " + startDate.strftime("%b") + " " + str(startDate.year)
        eDate = currDate.strftime("%d") + " " + currDate.strftime("%b") + " " + str(currDate.year)
        
        res = db.execute("""SELECT DISTINCT(category_name), SUM(amount) AS amount FROM expense JOIN category
                                ON expense.category_id = category.id WHERE expense.user_id = ? AND date 
                                BETWEEN ? AND ? GROUP BY expense.category_id ORDER BY amount DESC""", session["user_id"], startDate, currDate)

        tt_expense = db.execute("""SELECT SUM(amount) AS amount FROM expense WHERE user_id = ? AND date
                                BETWEEN ? AND ?;""", session["user_id"], startDate, currDate)[0]['amount']
        
        tt_expense = "{:.2f}".format(float(tt_expense))
        cat = [cat["category_name"] for cat in res]
        amt_list = [int(amt["amount"]) for amt in res]
        data = { 'cat' : cat, 'amt' : amt_list, 'sDate' : sDate, 'eDate' : eDate, 'tt_expense' : tt_expense }

        return jsonify(data)

@app.route("/sort/quarter", methods=["GET"])
@login_required
def sortquarter():

    if request.method == "GET":

        currDate = datetime.now()
        starting_month = currDate.month - 3
        starting_year = currDate.year
        if starting_month <= 0:
            starting_month += 12
            starting_year -= 1

        startDate = datetime(starting_year, starting_month, 1)
        sDate = "1 " + startDate.strftime("%b") + " " + str(startDate.year)
        startDate = startDate.strftime("%Y-%m-%d")
        last_day = calendar.monthrange(currDate.year, currDate.month)[1]  
        eDate = str(last_day) + " " + currDate.strftime("%b") + " " + str(currDate.year)

        res = db.execute("""SELECT DISTINCT(category_name), SUM(amount) AS amount FROM expense JOIN category
                                ON expense.category_id = category.id WHERE expense.user_id = ? AND date 
                                BETWEEN ? AND ? GROUP BY expense.category_id ORDER BY amount DESC""", session["user_id"], startDate, str(currDate))

        tt_expense = db.execute("""SELECT SUM(amount) AS amount FROM expense WHERE user_id = ? AND date
                                BETWEEN ? AND ?;""", session["user_id"], startDate, str(currDate))[0]['amount']
        
        tt_expense = "{:.2f}".format(float(tt_expense))
        cat = [cat["category_name"] for cat in res]
        amt_list = [int(amt["amount"]) for amt in res]
        data = { 'cat' : cat, 'amt' : amt_list, 'sDate' : sDate, 'eDate' : eDate, 'tt_expense' : tt_expense }

        return jsonify(data)
    
@app.route("/sort/year", methods=["GET"])
@login_required
def sortyear():

    if request.method == "GET":

        currDate = datetime.now()
        starting_year = currDate.year - 1
        startDate = datetime(starting_year, currDate.month, 1)
        sDate = "1 " + startDate.strftime("%b") + " " + str(starting_year)
        startDate = startDate.strftime("%Y-%m-%d")
        eDate = str(currDate.day) + " " + currDate.strftime("%b") + " " + str(currDate.year)
        currDate = currDate.strftime("%Y-%m-%d")

        res = db.execute("""SELECT DISTINCT(category_name), SUM(amount) AS amount FROM expense JOIN category
                                ON expense.category_id = category.id WHERE expense.user_id = ? AND date 
                                BETWEEN ? AND ? GROUP BY expense.category_id ORDER BY amount DESC""", session["user_id"], startDate, currDate)

        tt_expense = db.execute("""SELECT SUM(amount) AS amount FROM expense WHERE user_id = ? AND date
                                BETWEEN ? AND ?;""", session["user_id"], startDate, currDate)[0]['amount']
        
        tt_expense = "{:.2f}".format(float(tt_expense))
        cat = [cat["category_name"] for cat in res]
        amt_list = [int(amt["amount"]) for amt in res]
        data = { 'cat' : cat, 'amt' : amt_list, 'sDate' : sDate, 'eDate' : eDate, 'tt_expense' : tt_expense }

        return jsonify(data)

@app.route('/sort/custom', methods=["POST"])
@login_required
def sortcustom():

    if request.method == "POST":

        data = request.get_json()
        startDate = data.get("sDate")
        endDate = data.get("eDate")


        res = db.execute("""SELECT DISTINCT(category_name), SUM(amount) AS amount FROM expense JOIN category
                                ON expense.category_id = category.id WHERE expense.user_id = ? AND date 
                                BETWEEN ? AND ? GROUP BY expense.category_id ORDER BY amount DESC""", session["user_id"], startDate, endDate)

        tt_expense = db.execute("""SELECT SUM(amount) AS amount FROM expense WHERE user_id = ? AND date
                                BETWEEN ? AND ?;""", session["user_id"], startDate, endDate)[0]['amount']
        
        startDate = datetime.strptime(startDate, "%Y-%m-%d")
        endDate = datetime.strptime(endDate, "%Y-%m-%d")
        sDate = str(startDate.day) + " " + startDate.strftime("%b") + " " + str(startDate.year)
        eDate = str(endDate.day) + " " + endDate.strftime("%b") + " " + str(endDate.year)
        
        tt_expense = "{:.2f}".format(float(tt_expense))
        cat = [cat["category_name"] for cat in res]
        amt_list = [int(amt["amount"]) for amt in res]
        data = { 'cat' : cat, 'amt' : amt_list, 'sDate' : sDate, 'eDate' : eDate, 'tt_expense' : tt_expense }

        return jsonify(data)

@app.route("/budgetview", methods=["GET"])
@login_required
def budgetview():

    if request.method == "GET":

        res = db.execute("""SELECT category.category_name AS category, budget.amount AS budget,
                         COALESCE(SUM(CASE WHEN expense.date BETWEEN budget.start AND budget.end
                         THEN expense.amount ELSE 0 END), 0) AS amount FROM category
                         INNER JOIN budget ON category.id = budget.category_id LEFT JOIN
                         expense ON budget.user_id = expense.user_id AND budget.category_id = expense.category_id
                         WHERE budget.user_id = ? AND expense.user_id = ?
                         GROUP BY category.category_name, budget.amount
                         HAVING DATE('now') BETWEEN budget.start AND budget.end;""", session["user_id"], session["user_id"])

        cat = [cat["category"] for cat in res]  
        bud = [bud["budget"] for bud in res]
        amt = [amt["amount"] for amt in res]
        rbud = {}
        ebud = {}
        
        for i in res:
            x = int(i["budget"]) - int(i["amount"])
            if x >= 0:
                rbud[i["category"]] = x
            else:
                ebud[i["category"]] = abs(x)

        data = { 'cat' : cat, 'bud' : bud, 'amt' : amt, 'rbud' : rbud, 'ebud' : ebud }
        return jsonify(data)

@app.route("/login", methods=["GET", "POST"])           
def login():

    session.clear()

    if request.method == "GET":
        
        error_message = request.args.get("error_message")
        if not error_message:
            return render_template("login.html")
        return render_template("login.html", error_message=error_message)
    
    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        error_message="Enter your username"
        return redirect(url_for("login", error_message=error_message))
    elif not password:
        error_message="Enter your password"
        return redirect(url_for("login", error_message=error_message))
    
    user = db.execute("SELECT * FROM users WHERE username = ?;", username)

    if len(user) == 1 and check_password_hash(user[0]["password_hash"], password):
        session["user_id"] = user[0]["id"]
    else:
        error_message="Incorrect username or password"
        return redirect(url_for("login", error_message=error_message))

    return redirect("/")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    error_message = request.args.get("error_message")
    
    if request.method == "GET":
        
        if not error_message:
            return render_template("/register.html")
        
        return render_template("/register.html", error_message=error_message)
        
    username = request.form.get("username")
    password = request.form.get("password")
    pwConfirmation = request.form.get("confirmation")

    # Check if any fields are empty, return with error message
    error_message = ""
    if not username:
        error_message = "Username is required."
        return redirect(url_for("register", error_message=error_message))
    elif not password:
        error_message = "Password is required."
        return redirect(url_for("register", error_message=error_message))
    elif not pwConfirmation:
        error_message = "Confirm your password."
        return redirect(url_for("register", error_message=error_message))
    
    checkUsername = db.execute("SELECT * FROM users WHERE username = ?;", username)
    # Check if username already exists
    if len(checkUsername) != 0:
        error_message = "Username already exists."
        return redirect(url_for("register", error_message=error_message))

    # Add user to db
    pwHash = generate_password_hash(password)
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?);", username, pwHash)

    return redirect("/login")

@app.route("/expense")
@login_required
def expense():

    expenses = db.execute("""SELECT expense.id, category_name, amount, date, description FROM expense JOIN category ON expense.category_id = category.id
                           WHERE user_id = ? ORDER BY date DESC;""", session["user_id"])
    
    category = db.execute("SELECT * FROM category;")

    return render_template("expense.html", expenses=expenses, categories=category)

@app.route("/expense/add", methods=["POST"])
@login_required
def add():

    if request.method == "POST":

        category = request.form.get("category")
        amount = request.form.get("amount")
        desc = request.form.get("description")
        date = datetime.strptime(request.form.get("date"), '%Y-%m-%d').date()
        cat_list = db.execute("SELECT category_name FROM category;")
        check_cat = db.execute("SELECT category_name FROM category WHERE category_name = ?;", category)

        expenses = db.execute("""SELECT expense.id, category_name, amount, date, description FROM expense JOIN category ON expense.category_id = category.id
                           WHERE user_id = ?;""", session["user_id"])
        print(date)
        print(dt.today())
        error_message = ""
        if not category:
            error_message = "Expense category cannot be empty."
            return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
        elif len(check_cat) == 0:
            error_message = "Invalid category."
            return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
        elif not amount:
            error_message = "Expense amount cannot be empty."
            return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
        elif not valid_amount(amount):
            error_message = "Amount must be numeric and more than 0."
            return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
        elif not date:
            error_message = "Date of expense cannot be empty."
            return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
        elif date > dt.today():
            error_message = "Date of expense cannot be later than current date."
            return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
        
        cat = db.execute("SELECT id FROM category WHERE category_name = ?;", category)
        
        catId = cat[0]["id"]    

        db.execute("""INSERT INTO expense (user_id, category_id, amount, date, description)
                   VALUES (?, ?, ?, ?, ?);""", session["user_id"], catId, amount, date, desc)

        return redirect("/expense")
    
@app.route("/expense/edit", methods=["POST"])
@login_required
def edit():

    ex_id = request.form.get("expense_id")
    category = request.form.get("category")
    amount = request.form.get("amount")
    date = datetime.strptime(request.form.get("date"), '%Y-%m-%d').date()
    desc = request.form.get("description")

    queryCat = db.execute("SELECT * FROM category;")
    cat_list = [cat["category_name"] for cat in queryCat]
    expenses = db.execute("""SELECT expense.id, category_name, amount, date, description FROM expense JOIN category ON expense.category_id = category.id
                           WHERE user_id = ?;""", session["user_id"])
    error_message = ""
    if not category or category not in cat_list:
        error_message = "Invalid category."
        return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
    elif not valid_amount(amount):
        error_message = "Invalid amount."
        return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
    elif not date or date > dt.today():
        error_message = "Invalid date."
        return render_template("expense.html", error_message=error_message, categories=cat_list, expenses=expenses)
    
    cat_id = db.execute("SELECT id FROM category WHERE category_name = ?;", category)

    db.execute("""UPDATE expense SET category_id = ?, amount = ?, date = ?, description = ?
               WHERE id = ?;""", cat_id[0]["id"], amount, date, desc, ex_id)

    return redirect("/expense")

@app.route("/expense/delete", methods=["POST"])
@login_required
def delete():
    
    if request.method == "POST":
        
        ex_id = request.form.get("expense_id")

        db.execute("DELETE FROM expense WHERE id = ?;", ex_id)

    return redirect("/expense")

@app.route("/budget")
@login_required
def budget():

    budgets = db.execute("""SELECT budget.id, category_name, amount, start, end FROM budget JOIN category ON budget.category_id = category.id
                         WHERE budget.user_id = ?""", session["user_id"])
    
    categories = db.execute("SELECT * FROM category;")

    return render_template("budget.html", budgets=budgets, categories=categories)

@app.route("/budget/add", methods=["POST"])
@login_required
def add_budget():

    if request.method == "POST":
        
        category = request.form.get("category")
        amount = request.form.get("amount")
        sDate = datetime.strptime(request.form.get("date_start"), '%Y-%m-%d').date()
        eDate = datetime.strptime(request.form.get("date_end"), '%Y-%m-%d').date()
        cat_id = (db.execute("SELECT id FROM category WHERE category_name = ?;", category))[0]["id"]

        budgets = db.execute("""SELECT budget.id, category_name, amount, start, end FROM budget JOIN category ON budget.category_id = category.id
                         WHERE budget.user_id = ?""", session["user_id"])
    
        categories = db.execute("SELECT * FROM category;")

        error_message = ""
        if not category or not cat_id:
            error_message = "Invalid category."
            return render_template("budget.html", budgets=budgets, categories=categories, error_message=error_message)
        elif not valid_amount(amount):
            error_message = "Invalid amount."
            return render_template("budget.html", budgets=budgets, categories=categories,error_message=error_message)
        elif not sDate or not eDate or sDate > eDate:
            error_message = "Invalid date."
            return render_template("budget.html", budgets=budgets, categories=categories,error_message=error_message)

        db.execute("""INSERT INTO budget (category_id, user_id, amount, start, end)
                   VALUES (?, ?, ?, ?, ?);""", cat_id, session["user_id"], amount, str(sDate), str(eDate))

        return redirect("/budget")
    
@app.route("/budget/edit", methods=["POST"])
@login_required
def edit_budget():

    if request.method == "POST":

        budget_id = request.form.get("budget_id")
        category = request.form.get("category")
        amount = request.form.get("amount")
        sDate = datetime.strptime(request.form.get("date_start"), '%Y-%m-%d').date()
        eDate = datetime.strptime(request.form.get("date_end"), '%Y-%m-%d').date()
        cat_id = (db.execute("SELECT id FROM category WHERE category_name = ?;", category))[0]["id"]

        budgets = db.execute("""SELECT budget.id, category_name, amount, start, end FROM budget JOIN category ON budget.category_id = category.id
                         WHERE budget.user_id = ?""", session["user_id"])
    
        categories = db.execute("SELECT * FROM category;")

        error_message = ""
        if not category or not cat_id:
            error_message = "Invalid category."
            return render_template("budget.html", budgets=budgets, categories=categories, error_message=error_message)
        elif not valid_amount(amount):
            error_message = "Invalid amount."
            return render_template("budget.html", budgets=budgets, categories=categories,error_message=error_message)
        elif not sDate or not eDate or sDate > eDate:
            error_message = "Invalid date."
            return render_template("budget.html", budgets=budgets, categories=categories,error_message=error_message)

        db.execute("""UPDATE budget SET category_id = ?, amount = ?, start = ?, end = ?
                   WHERE id = ?;""", cat_id, amount, str(sDate), str(eDate), budget_id)

        return redirect("/budget")
    
@app.route("/budget/delete", methods=["POST"])
@login_required
def del_budget():

    if request.method == "POST":

        budget_id = request.form.get("budget_id")

        db.execute("DELETE FROM budget WHERE id = ?;", budget_id)

        return redirect("/budget")