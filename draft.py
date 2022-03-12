def get_customer_by_id(self, id_):
    self.db_cursor.execute(f"select * from customers where id = {id_}")
    customer = self.db_cursor.fetchall()
    if customer:
        selected_customer = Customer(id_=customer[0][0], name=customer[0][1], city=customer[0][2])
        return selected_customer.__dict__
    else:
        return []


def insert_new_customer(self, customer):
    if not isinstance(customer, Customer):
        return False
    if not hasattr(customer, "name") or not hasattr(customer, "city"):
        return False
    self.db_cursor.execute(f'insert into customers (name, city) values ("{customer.name}", "{customer.city}")')
    self.con.commit()
    return True


def update_put_customer(self, id_, values_dict):
    updated_values_dict = {}
    for key, value in values_dict.items():
        if key == 'name' or key == 'city':
            updated_values_dict[key] = value
    if len(list(updated_values_dict.keys())) == 2:
        self.db_cursor.execute(f'update customers set name="{updated_values_dict["name"]}", '
                               f'city="{updated_values_dict["city"]}" where id={id_}')
        self.con.commit()
        return True
    else:
        return False


def update_patch_customer(self, id_, values_dict):
    updated_values_dict = {}
    for key, value in values_dict.items():
        if key == 'name' or key == 'city':
            updated_values_dict[key] = value
    if len(list(updated_values_dict.keys())) == 2:
        self.db_cursor.execute(f'update customers set name="{updated_values_dict["name"]}", '
                               f'city="{updated_values_dict["city"]}" where id={id_}')
        self.con.commit()
        return True
    if 'name' in updated_values_dict:
        self.db_cursor.execute(f'update customers set name="{updated_values_dict["name"]}" where id={id_}')
        self.con.commit()
    if 'city' in updated_values_dict:
        self.db_cursor.execute(f'update customers set city="{updated_values_dict["city"]}" where id={id_}')
        self.con.commit()
    return True


def delete_customer(self, id_):  # can do it with try catch but not raising any errors if id not exists in the db
    self.db_cursor.execute(f'delete from customers where id={id_}')
    self.con.commit()
    return True


def get_user_by_username_and_password(self, username, password):
    self.db_cursor.execute(f'select * from users where username="{username}" and password={password}')
    user = self.db_cursor.fetchall()
    if user:
        selected_user = User(id_=user[0][0], public_id=user[0][1], username=user[0][2], password=user[0][3])
        return selected_user
    else:
        return None


def get_user_by_username(self, username):
    self.db_cursor.execute(f'select * from users where username="{username}"')
    user = self.db_cursor.fetchall()
    if user:
        selected_user = User(id_=user[0][0], public_id=user[0][1], username=user[0][2], password=user[0][3])
        return selected_user
    else:
        return None


def get_user_by_public_id(self, public_id):
    self.db_cursor.execute(f'select * from users where public_id="{public_id}"')
    user = self.db_cursor.fetchall()
    if user:
        selected_user = User(id_=user[0][0], public_id=user[0][1], username=user[0][2], password=user[0][3])
        return selected_user
    else:
        return None


def insert_new_user(self, user):
    if not isinstance(user, User):
        return False
    if not hasattr(user, "username") or not hasattr(user, "password"):
        return False
    self.db_cursor.execute(f'insert into users (public_id, username, password) values '
                           f'("{user.public_id}", "{user.username}", "{user.password}")')
    self.con.commit()
    return True