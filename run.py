from backend.app import create_app
from backend.app.extensions import db
from flask_migrate import Migrate
from backend.app.models import User, Company, Application, Model, Query

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Company": Company,
        "Application": Application,
        "Model": Model,
        "Query": Query,
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
