from app import app, db, Petrol

with app.app_context():
    db.create_all()
    print("Database tables created!")

    petrolType1 = Petrol(name="Unleaded", price=1.80)
    petrolType2 = Petrol(name="Diesel", price=1.90)
    petrolType3 = Petrol(name="Premium", price = 2.10)

    db.session.add(petrolType1)
    db.session.add(petrolType2)
    db.session.add(petrolType3)
    db.session.commit()
    print("Petrol data added to database")