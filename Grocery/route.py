# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 14:38:36 2021

@author: 91902
"""
from Grocery import db
from sqlalchemy import and_, or_, not_
from Grocery import app
from flask import render_template,redirect,url_for,flash,get_flashed_messages,request
from Grocery.models import Item,User,Todo,Cart
from Grocery.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm,AddItemForm,SetBudgetForm,BuyForm
from flask_login import login_user,logout_user,login_required,current_user

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
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




@app.route('/add_itemwx1w',methods=['GET','POST'])
@login_required
def add_item1():
    form=AddItemForm()
    if form.validate_on_submit():
        item_to_add=Item(name=form.item_name.data,price=form.price.data,owner=current_user.id)
        db.session.add(item_to_add)
        db.session.commit()
        flash("{} Added successfully ".format(item_to_add.name), category='success')
        
        return redirect(url_for('add_item'))
    if(form.errors!={}):
        for err in form.errors.values():
            flash("There was an error {}".format(err),category='danger')
    return render_template('add_item.html',form=form)
    
    
    


@app.route('/market',methods=['GET','POST'])
@login_required
def market_page():
    ''''form=PurchaseItemForm()
    selling_form=SellItemForm()
    buy_form=BuyForm()
    if request.method=="POST":
       
        purchased_item=request.form.get('purchased_item')
      
        item_price=request.form.get('item_price')

        item_id=request.form.get('item_id')
       
        p_item=Item.query.join().filter(Item.name==purchased_item,Item.price==item_price,Item.id==item_id).first()
        
        
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.buy(current_user)
                
                flash("YOU HAVE SUCCESSFULLY ADDED {} for {} Rs.".format(p_item.name,p_item.price),category='success')
            
            else:
                flash("YOU DONT HAVE ENOUGH MONEY", category='danger')
    
    
        
    
   
        sold_item=request.form.get('sold_item')
       
        sold_item_price=request.form.get('sold_item_price')
       
        sold_item_id=request.form.get('sold_item_id')
      
        s_item=Item.query.join().filter(Item.name==sold_item,Item.price==sold_item_price,Item.id==sold_item_id).first()
        
        
        if s_item:
           
            if current_user.can_sell(s_item):
                s_item.sell(current_user)
                flash("{} Removed from cart having price {}".format(s_item.name,s_item.price),category='success')
            else:
                    flash("SOMETHING WENT WRONG", category='danger')
        
        return redirect(url_for('market_page'))
    
    
    if request.method=="GET": 
        #item=Item.query.all()
        item=Item.query.filter_by(owner=current_user.id)
        own=current_user.id

        
        
        owned_items=Item.query.join().filter(Item.owner==current_user.id,Item.bought_item>0)
        uname=User.query.filter_by(id=current_user.id).first()
        
    
        
    if(request.method=="GET"):
        if(request.method=="GET"):
            total_price=request.form.get('total_price') 
            
        
        
        flash("{}".format(total_price))
                
                   
                            
                        
                        
                
         
        
            
    return render_template('market2.html',items=item,form=form,owned_items=owned_items,selling_form=selling_form,buy_form=buy_form,uname=str(uname.username).upper())'''
        

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



@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash("Account Created Successfully! You are logged in as {}".format(user_to_create.username), category='success')
        
    
        
        return redirect(url_for('market_page'))
    if(form.errors!={}):
        for err in form.errors.values():
            flash("There was an error {}".format(err),category='danger')
    return render_template('register.html',form=form)








@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash("Success! You are logged in as {}".format(attempted_user.username), category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')
  

    return render_template('login.html', form=form)






        

@app.route('/logout')
def logout_page():
    logout_user()
    flash("YOU HAVE BEEN LOGGED OUT",category="info")
    return redirect(url_for('home_page'))
    


if __name__=="__main__":
    app.run(debug=True)     