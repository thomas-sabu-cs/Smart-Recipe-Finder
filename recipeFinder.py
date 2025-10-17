from flask import Flask, request, jsonify, render_template
import requests
app = Flask(__name__)
API_KEY = 'a9f7fe431e564375833a46acf1b790c4'

@app.route('/')
def home():
    return render_template('recipePage.html')
@app.route('/search_recipes', methods=['GET'])
def search_recipes():
    ingredients = request.args.get('ingredients')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch recipes"}), 500
if __name__ == '__main__':
    app.run(debug=True)
