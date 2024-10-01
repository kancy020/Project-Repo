from app import app, db, Petrol

with app.app_context():
    db.create_all()
    print("Database tables created!")
