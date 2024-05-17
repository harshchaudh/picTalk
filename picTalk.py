from app import db, create_app
from flask_migrate import Migrate
from app.config import Config

app = create_app(Config)
migrate= Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)