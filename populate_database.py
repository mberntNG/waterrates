import csv
from app import create_app, db
from app.models import Utility, Block
from datetime import datetime

def populate_db(csv_file):
    app = create_app()
    with app.app_context():
        # Open the CSV file
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Parse the data for Utility
                utility = Utility(
                    city=row['city'],
                    state=row['state'],
                    client=row['client'],
                    population=int(row['population']) if row['population'] else None,
                    winter_avg=row['winter_avg'],
                    meter_size=row['meter_size'],
                    effective_date=datetime.strptime(row['effective_date'], '%Y-%m-%d').date() if row['effective_date'] else None,
                    source=row['source'],
                    w_min_bill=float(row['w_min_bill']) if row['w_min_bill'] else None,
                    ww_min_bill=float(row['ww_min_bill']) if row['ww_min_bill'] else None
                )
                db.session.add(utility)
                db.session.commit()

                # Add blocks for water
                for i in range(1, 11):
                    gallons_key = f'w_block_{i}_gals'
                    rate_key = f'w_block_{i}_rate'
                    if row[gallons_key] and row[rate_key]:
                        block = Block(
                            gallons=int(row[gallons_key]),
                            rate=float(row[rate_key]),
                            type='water',
                            utility_id=utility.id
                        )
                        db.session.add(block)

                # Add blocks for wastewater
                for i in range(1, 11):
                    gallons_key = f'ww_block_{i}_gals'
                    rate_key = f'ww_block_{i}_rate'
                    if row[gallons_key] and row[rate_key]:
                        block = Block(
                            gallons=int(row[gallons_key]),
                            rate=float(row[rate_key]),
                            type='wastewater',
                            utility_id=utility.id
                        )
                        db.session.add(block)

            # Commit all blocks to the database
            db.session.commit()
            print("Data populated successfully.")

if __name__ == "__main__":
    populate_db('utilities.csv')
