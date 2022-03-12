from Customer import Customer
from User import User
from Logger import Logger
import sqlite3
from flask import Flask, request, jsonify, make_response



class RestDataAccess:

    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
        self.con = sqlite3.connect(db_file_path, check_same_thread=False)
        self.db_cursor = self.con.cursor()
        self.logger = Logger.get_instance()

    def get_all_customers(self, get_cust):
        customers_list = []
        self.db_cursor.execute("select * from customers")
        customers = self.db_cursor.fetchall()
        for customer in customers:
            customers_list.append(Customer(id=customer[0], name=customer[1], city=customer[2]))
        #if len(get_cust) == 0:
        #    return_ls = [customer.__dict__ for customer in customers_ls]
        #    return return_ls
        customers_ans = []
        for c in customers_list:
            if "city" in get_cust.keys():
                if c.city == get_cust['city']:
                    customers_ans.append(c)
        ans = [customer.__dict__ for customer in customers_ans]
        return ans

    def get_user_by_public_id(self, public_id):
        self.db_cursor.execute(f'select * from users where public_id="{public_id}"')
        user = self.db_cursor.fetchall()
        if user:
            user_by_pub_id = User(id=user[0][0], public_id=user[0][1], username=user[0][2], password=user[0][3])
            return user_by_pub_id
        else:
            return None

    def add_new_customer(self, customer):
        if not isinstance(customer, Customer):
            return False
        if len(customer.name)<1:
            return False
        if len(customer.city)<1:
            return False
        self.db_cursor.execute(f'insert into customers (name, city) values ("{customer.name}", "{customer.city}")')
        self.con.commit()
        return True

    def add_new_user(self, user):
        if not isinstance(user, User):
            return False
        if len(user.username)<1:
            return False
        if len(user.password)<1:
            return False
        self.db_cursor.execute(f'insert into users (public_id, username, password) values '
                               f'("{user.public_id}", "{user.username}", "{user.password}")')
        self.con.commit()
        return True