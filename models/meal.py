from database import db
from flask_login import UserMixin

class Meal(db.Model, UserMixin):
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False)
  description = db.Column(db.String(80), nullable=False) 
  registered_at = db.Column(db.DateTime(), nullable=False) 
  on_diet = db.Column(db.Boolean(), nullable=False, default=False) 