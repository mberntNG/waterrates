import csv
from datetime import datetime
from app import create_app, db
from app.models import Utility

app = create_app()

with app.app_context():
    db.create_all()

    with open('WaterRates.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Normalize headers by stripping whitespace and converting to lowercase
        reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

        for row in reader:
            try:
                effective_date = datetime.strptime(row['effective_date'], '%m/%d/%Y').date() if row['effective_date'] and row['effective_date'] != '#####' else None
                utility = Utility(
                    source=row.get('source'),
                    city=row.get('city'),
                    state=row.get('state'),
                    client=row.get('client'),
                    population=int(row['population']) if row.get('population') else None,
                    winter_avg=row.get('winter_avg'),
                    meter_size=row.get('meter_size'),
                    effective_date=effective_date,
                    w_min_bill=float(row['w_min_bill']) if row.get('w_min_bill') else None,
                    w_block_1_gals=int(row['w_block_1_gals']) if row.get('w_block_1_gals') else None,
                    w_block_1_rate=float(row['w_block_1_rate']) if row.get('w_block_1_rate') else None,
                    w_block_2_gals=int(row['w_block_2_gals']) if row.get('w_block_2_gals') else None,
                    w_block_2_rate=float(row['w_block_2_rate']) if row.get('w_block_2_rate') else None,
                    w_block_3_gals=int(row['w_block_3_gals']) if row.get('w_block_3_gals') else None,
                    w_block_3_rate=float(row['w_block_3_rate']) if row.get('w_block_3_rate') else None,
                    w_block_4_gals=int(row['w_block_4_gals']) if row.get('w_block_4_gals') else None,
                    w_block_4_rate=float(row['w_block_4_rate']) if row.get('w_block_4_rate') else None,
                    w_block_5_gals=int(row['w_block_5_gals']) if row.get('w_block_5_gals') else None,
                    w_block_5_rate=float(row['w_block_5_rate']) if row.get('w_block_5_rate') else None,
                    w_block_6_gals=int(row['w_block_6_gals']) if row.get('w_block_6_gals') else None,
                    w_block_6_rate=float(row['w_block_6_rate']) if row.get('w_block_6_rate') else None,
                    w_block_7_gals=int(row['w_block_7_gals']) if row.get('w_block_7_gals') else None,
                    w_block_7_rate=float(row['w_block_7_rate']) if row.get('w_block_7_rate') else None,
                    w_block_8_gals=int(row['w_block_8_gals']) if row.get('w_block_8_gals') else None,
                    w_block_8_rate=float(row['w_block_8_rate']) if row.get('w_block_8_rate') else None,
                    w_block_9_gals=int(row['w_block_9_gals']) if row.get('w_block_9_gals') else None,
                    w_block_9_rate=float(row['w_block_9_rate']) if row.get('w_block_9_rate') else None,
                    w_block_10_gals=int(row['w_block_10_gals']) if row.get('w_block_10_gals') else None,
                    w_block_10_rate=float(row['w_block_10_rate']) if row.get('w_block_10_rate') else None,
                    ww_min_bill=float(row['ww_min_bill']) if row.get('ww_min_bill') else None,
                    ww_block_1_gals=int(row['ww_block_1_gals']) if row.get('ww_block_1_gals') else None,
                    ww_block_1_rate=float(row['ww_block_1_rate']) if row.get('ww_block_1_rate') else None,
                    ww_block_2_gals=int(row['ww_block_2_gals']) if row.get('ww_block_2_gals') else None,
                    ww_block_2_rate=float(row['ww_block_2_rate']) if row.get('ww_block_2_rate') else None,
                    ww_block_3_gals=int(row['ww_block_3_gals']) if row.get('ww_block_3_gals') else None,
                    ww_block_3_rate=float(row['ww_block_3_rate']) if row.get('ww_block_3_rate') else None,
                    ww_block_4_gals=int(row['ww_block_4_gals']) if row.get('ww_block_4_gals') else None,
                    ww_block_4_rate=float(row['ww_block_4_rate']) if row.get('ww_block_4_rate') else None,
                    ww_block_5_gals=int(row['ww_block_5_gals']) if row.get('ww_block_5_gals') else None,
                    ww_block_5_rate=float(row['ww_block_5_rate']) if row.get('ww_block_5_rate') else None,
                    ww_block_6_gals=int(row['ww_block_1_gals']) if row.get('ww_block_6_gals') else None,
                    ww_block_6_rate=float(row['ww_block_1_rate']) if row.get('ww_block_6_rate') else None,
                    ww_block_7_gals=int(row['ww_block_2_gals']) if row.get('ww_block_7_gals') else None,
                    ww_block_7_rate=float(row['ww_block_2_rate']) if row.get('ww_block_7_rate') else None,
                    ww_block_8_gals=int(row['ww_block_3_gals']) if row.get('ww_block_8_gals') else None,
                    ww_block_8_rate=float(row['ww_block_3_rate']) if row.get('ww_block_8_rate') else None,
                    ww_block_9_gals=int(row['ww_block_4_gals']) if row.get('ww_block_9_gals') else None,
                    ww_block_9_rate=float(row['ww_block_4_rate']) if row.get('ww_block_9_rate') else None,
                    ww_block_10_gals=int(row['ww_block_5_gals']) if row.get('ww_block_10_gals') else None,
                    ww_block_10_rate=float(row['ww_block_5_rate']) if row.get('ww_block_10_rate') else None

                )
                db.session.add(utility)
            except Exception as e:
                print(f"Error processing row: {row}")
                print(e)
            
        db.session.commit()
