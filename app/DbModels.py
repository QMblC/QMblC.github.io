from cfg import app, db

class UserDb(db.Model):
    id = db.Column(db.String(20), primary_key = True, nullable = False)
    location  = db.Column(db.String(200))
    division = db.Column(db.String(200))
    departament = db.Column(db.String(200))
    team = db.Column(db.String(200))
    profession = db.Column(db.String(200))
    name = db.Column(db.String(100))
    job_type = db.Column(db.String(100))
    
    def __repr__(self) -> str:
        return '<User %r>' % self.id
    
    def create_table():
        with app.app_context():
            db.create_all()

    def delete_table():
        with app.app_context():
            db.drop_all()

with app.app_context():
    db.create_all()
        