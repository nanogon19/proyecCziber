from backend.app.extensions import db

company_application = db.Table(
    'company_application',
    db.Column('company_id', db.String, db.ForeignKey('companies.id_emp'), primary_key=True),
    db.Column('application_id', db.String, db.ForeignKey('applications.id_app'), primary_key=True)
)
