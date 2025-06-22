from controller.sql import Sql

db = Sql("userDatabase.db")

create_user = db.create_user
auth_user = db.user_login
user_exists = db.user_exists