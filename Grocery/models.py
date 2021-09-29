# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 14:37:56 2021

@author: 91902
"""
from Grocery import db,login_manager
from Grocery import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))




class User(db.Model,UserMixin):
    
    id =db.Column(db.Integer(), primary_key=True,autoincrement=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Integer(),nullable=False,default=10000)
    items=db.relationship('Todo',backref='owned_user',lazy=True)

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,ptp):
        self.password_hash=bcrypt.generate_password_hash(ptp).decode('utf-8')
        
    
    def check_password_correction(self, attempted_password):
         return bcrypt.check_password_hash(self.password_hash, attempted_password)
     
    @property
    def prettier_budget(self):
         if  (len(str(self.budget)))>=4:
             return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]} Rs.'
         else:
             return "{} Rs.".format(self.budget)
    def can_purchase(self,itm):
         return self.budget>=itm.price
     
    def can_sell(self,item_obj):
        return item_obj in self.items
    
    def __repr__(self):
        return "Item {}".format(self.username)
    
    def add_budget(self,amnt):
        self.budget=int(amnt)
        db.session.commit()
  

class Item(db.Model):
    id =db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name=db.Column(db.String(length=30),nullable=False,unique=False)
    price=db.Column(db.Integer(),nullable=False)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))
    bought_item=db.Column(db.Integer(),default=0)
    
    
    def buy(self,user):
                self.owner=user.id
                user.budget-=self.price
                self.bought_item=self.price
                db.session.commit()
    def sell(self,user):
                self.bought_item=0
                user.budget+=self.price
                db.session.commit()
    
    
    def __repr__(self):
        return "Item {}".format(self.name)
    
    
class Todo(db.Model):
    id =db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name=db.Column(db.String(length=30),nullable=False,unique=False)
    price=db.Column(db.Integer(),nullable=False)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))
    bought_item=db.Column(db.Boolean)

    
    
    def buy(self,user):
                self.owner=user.id
                user.budget-=self.price
                self.bought_item=True
                db.session.commit()
    def sell(self,user):
                self.bought_item=False
                user.budget+=self.price
                db.session.commit()
    
    
    def __repr__(self):
        return "Item {}".format(self.name)
    
    
    
class Cart(db.Model):
    id =db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name=db.Column(db.String(length=30),nullable=False,unique=False)
    price=db.Column(db.Integer(),nullable=False)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))
    bought_item=db.Column(db.Boolean)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    