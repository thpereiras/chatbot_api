from api import db, bcrypt, UserModel
import datetime
class Administration():

  @staticmethod
  def create_admin_user(name, login, password):
    Administration.delete_user(login)
    user = UserModel(name, login, password, timestamp = datetime.datetime.now())
    try:
      result = db.session.add(user)
      db.session.commit()
    except BaseException as e:
      print(e.orig)

  @staticmethod
  def delete_user(login):
    user_exists = UserModel.query.filter_by(login=login).first()
    if user_exists is not None:
      db.session.delete(user_exists)
      db.session.commit()
