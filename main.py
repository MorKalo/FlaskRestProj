from Init_db import *
from DbRepo import DbRepo
from Customer import Customer

repo=DbRepo(local_session)
init=Init_db()
#local_session.execute('drop TABLE users CASCADE')
#local_session.execute('drop TABLE customers CASCADE')


#init.reset_all_db()
#create_all_entities()

#init.insert_Data()

local_session.commit()
#repo.add(User(username='mormor', password='1234'))
print(repo.get_customer_by_id(234))
print(repo.get_all_customers())

print(repo.get_all_customers())
print ('user by username is: ')
print(repo.get_user_by_username('EfiMo'))
print ('user by email is: ')
print(repo.get_user_by_email('roiki@gmail.com'))
#repo.delete_customer_by_id(234)
#print(repo.get_all_customers())
repo.post(Customer(fullname='ofri moshe', address='yahuda ealevi'))
print(repo.get_all_customers())