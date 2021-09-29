from os import name
from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/set_budget',methods=['GET','POST'])
@login_required
def set_budget():
    form=SetBudgetForm()
    if form.validate_on_submit():
        current_user.add_budget(form.new_budget.data)
        
        
        flash("RS. {} set as budget successfully ".format(form.new_budget.data), category='success')
        
        return redirect(url_for('set_budget'))
    if(form.errors!={}):
        for err in form.errors.values():
            flash("There was an error {}".format(err),category='danger')
    return render_template('set_budget.html',form=form)

@app.route('/set_budget',methods=['GET','POST'])
@login_required
def set_budget():
    form=SetBudgetForm()
    if form.validate_on_submit():
        current_user.add_budget(form.new_budget.data)
        
        
        flash("RS. {} set as budget successfully ".format(form.new_budget.data), category='success')
        
        return redirect(url_for('set_budget'))
    if(form.errors!={}):
        for err in form.errors.values():
            flash("There was an error {}".format(err),category='danger')
    return render_template('set_budget.html',form=form)

@app.route('/grocery', methods=['GET','POST'])
@login_required
def grocery_page():
    '''purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulations! You purchased {p_item_object.name} for {p_item_object.price}', category='success')
            else:
                flash(f"Unfortunately you don't have enough money to purchase {p_item_object.name} ", category='danger')
        
        # Sell item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulations! You sold {s_item_object.name} back to market ! ', category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name} ", category='danger')

        return redirect(url_for('grocery_page'))
  
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('grocery.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)'''

    
    todo=Todo.query.all()
    cart=Cart.query.all()
    todo=Todo.query.filter_by(owner=current_user.id)
    cart=Cart.query.filter_by(owner=current_user.id)
       
    return render_template('market2.html',todo=todo,cart=cart)

@app.route('/add_item',methods=['GET','POST'])
def add_item():
    fname=request.form.get('item')
    fprice=request.form.get('price')
   
    if(fname=="" or fprice==""):
        flash('Item Name or price cannot be empty', category='danger')
    
    else:
        if(fprice.isnumeric()):
            new=Todo(name=fname, price=fprice, bought_item=False, owner=current_user.id)
            db.session.add(new)
            db.session.commit()
            flash("{} Added successfully ".format(new.name), category='success')
        else:
             flash('Price must be an integer', category='danger')
    
    return redirect(url_for("market_page"))

@app.route('/update_item/<int:todo_id>')
def update_item(todo_id):
    
    todo=Todo.query.filter_by(id=todo_id).first()
    
    if(todo.bought_item==False):
        if current_user.can_purchase(todo):
            todo.buy(current_user)
            c=Cart(name=todo.name, price=todo.price,owner=current_user.id)
            db.session.add(c)
            db.session.commit()
            flash("YOU HAVE SUCCESSFULLY ADDED {} for {} Rs.".format(todo.name,todo.price),category='success')
        else:
                flash("YOU DONT HAVE ENOUGH MONEY, PLEASE SET NEW BUDGET ACCORDINGLY", category='danger')
    else:
        todo.sell(current_user)
        
    
    
    db.session.commit()
    
    return redirect(url_for("market_page"))

@app.route('/delete_item/<int:todo_id>')
def delete_item(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for("market_page"))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                              email_address = form.email_address.data, 
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account Created Successfully ! You are now logged in as {user_to_create.username}', category='success') 

        return redirect(url_for('grocery_page'))
    if form.errors != {}: # if there are no errors from validatinos
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user : {err_msg}', category='danger')
    return render_template('register.html', form=form) 

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('grocery_page'))
        else:
            flash('USername and password are not matched! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

if __name__=="__main__":
    app.run(debug=True) 
