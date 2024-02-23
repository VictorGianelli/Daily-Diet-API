from flask import Flask, request, jsonify
from models.meal import Meal
from database import db
from flask_login import LoginManager # , login_user, current_user, logout_user, login_required
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/meal-crud'

db.init_app(app)
#Session <- conexão ativa

@app.route("/")
def hello():
    return "Data base is up and running" 

@app.route("/meal", methods=["POST"])
def create_meal():
  data = request.json
  username = data.get("username")
  description = data.get("description")
  on_diet = data.get("on_diet")

  if username and description:
    # hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    meal = Meal(username = username, description = description, registered_at = datetime.now(), on_diet = on_diet) # 
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Refeição cadastrado com sucesso"})

  return jsonify({"message": "Dados invalidos"}), 400

@app.route('/meal/<int:id_meal>', methods=["PUT"])
def update_meal(id_meal):
  data = request.json
  meal = Meal.query.get(id_meal)

  if meal:
    meal.username = data.get("username")
    meal.description = data.get("description")
    meal.registered_at = datetime.now()
    meal.on_diet = data.get("on_diet")
    db.session.commit()

    return jsonify({"message": f"Refeição {id_meal} atualizado com sucesso"})
  
  return jsonify({"message": "Refeição não encontrado"}), 404

@app.route('/meal/<int:id_meal>', methods=["DELETE"])
def delete_meal(id_meal):
  meal = Meal.query.get(id_meal)

  if meal:
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": f"Refeição {id_meal} deletado com sucesso"})
  
  return jsonify({"message": "Refeição não encontrado"}), 404

@app.route('/meal/<int:id_meal>', methods=["GET"])
def read_meal(id_meal):
  meal = Meal.query.get(id_meal)

  if meal:
    return {
            "id": meal.id,
            "username": meal.username,
            "description": meal.description, 
            "registered_at": meal.registered_at, 
            "on_diet": meal.on_diet
            }
  
  return jsonify({"message": "Refeição não encontrado"}), 404

@app.route('/meal', methods=["GET"])
def read_all_meal():
  
  all_meals = Meal.query.all()
  meal_list = []
  for meal in all_meals:
      meal_list.append({
          "id": meal.id,
          "username": meal.username,
          "description": meal.description, 
          "registered_at": meal.registered_at, 
          "on_diet": meal.on_diet
      })
  return jsonify(meal_list)

if __name__ == '__main__':
  app.run(debug=True)