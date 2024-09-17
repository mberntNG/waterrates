import csv
from datetime import datetime
from app import create_app  # Import your Flask app factory
from app.extensions import db
from app.models import Entity, Rate, Block

def populate_entities():
    with open('TxDOT_City_Boundaries.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entity = Entity(
                entity_name=row['entity'],
                entity_type='City',  # Or specify logic to determine entity_type
                state=row['state'],
                population=int(row['population']) if row['population'] else None,
                area_sq_mi=float(row['area_sq_mi']) if row['area_sq_mi'] else None,
                latitude=float(row['latitude']) if row['latitude'] else None,
                longitude=float(row['longitude']) if row['longitude'] else None
            )
            db.session.add(entity)
        db.session.commit()

def populate_rates_and_blocks():
    with open('utilities - Copy.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Find or create the entity based on the name
            entity = Entity.query.filter_by(entity_name=row['entity']).first()
            if not entity:
                print(f"Entity '{row['entity']}' not found in the Entity table.")
                continue

            # Create the Rate entry
            rate = Rate(
                entity_id=entity.id,
                winter_avg=row['winter_avg'],
                meter_size=row['meter_size'],
                effective_date=datetime.strptime(row['effective_date'], '%Y-%m-%d').date() if row['effective_date'] else None,
                source=row['source'],
                min_bill=float(row['min_bill']) if row['min_bill'] else None,
                rate_class=row['rate_class'],
                rate_type=row['rate_type'],
                units='kgal',
                other_vol_rates=float(row['other_vol_rates']) if row['other_vol_rates'] else None,
                updated_on=datetime.strptime(row['updated_on'], '%Y-%m-%d').date() if row['updated_on'] else None,
                updated_by=row['updated_by'],
                checked_on=datetime.strptime(row['checked_on'], '%Y-%m-%d').date() if row['checked_on'] else None,
                checked_by=row['checked_by'],
                notes=row['notes']
            )

            # Add rate to the session and commit it
            db.session.add(rate)
            db.session.commit()

            # Add debugging statement after creating the rate
            print(f"Created rate: {rate.id} for entity {entity.entity_name}")

            # Add water blocks
            for i in range(1, 11):
                volume_key = f'block_{i}_vol'
                block_rate_key = f'block_{i}_rate'  # Renamed to avoid overwriting `rate`

                # Ensure both values exist and can be converted before creating the Block
                if row.get(volume_key) and row.get(block_rate_key):
                    try:
                        volume = int(row[volume_key])
                        block_rate = float(row[block_rate_key])  # Renamed to avoid conflict with the `rate` object
                    except ValueError as e:
                        print(f"Skipping invalid block data: {e}")
                        continue  # Skip to the next block if conversion fails

                    # Debugging to see if values are correct
                    print(f"Creating block with volume={volume}, block_rate={block_rate} for rate_id={rate.id}")

                    block = Block(
                        volume=volume,
                        block_rate=block_rate,  # This is the rate for the block, renamed from 'rate'
                        rate_id=rate.id  # Correctly associate the block with the `Rate` object
                    )
                    db.session.add(block)

            db.session.commit()  # Commit all blocks for this rate


def populate_database():
    app = create_app()  # Create an instance of the Flask app
    with app.app_context():  # Push the app context
        populate_entities()
        populate_rates_and_blocks()

if __name__ == '__main__':
    populate_database()
