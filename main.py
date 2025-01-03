from flask import render_template, jsonify
import config
from models import Trail
from config import db


app = config.connex_app.app
app.add_api = config.connex_app.add_api
app.add_api(config.basedir / "swagger.yml")

@app.route('/')
def home():
    try:
        trails = Trail.query.all()
        return render_template('home.html', trail=trails)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000, debug=True)