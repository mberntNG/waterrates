from flask import Blueprint, render_template, request, redirect, url_for, flash
from .extensions import db
from .models import Utility, Block
from datetime import datetime

# Define the blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    utilities = Utility.query.all()
    return render_template('home.html', utilities=utilities)

@main.route('/add_utility', methods=['POST'])
def add_utility():
    # Collect form data
    city = request.form.get('city')
    state = request.form.get('state')
    client = request.form.get('client')
    population = request.form.get('population')
    winter_avg = request.form.get('winter_avg')
    meter_size = request.form.get('meter_size')
    effective_date_str = request.form.get('effective_date')
    source = request.form.get('source')
    w_min_bill_str = request.form.get('w_min_bill')
    ww_min_bill_str = request.form.get('ww_min_bill')

    # Convert effective_date_str to date
    if effective_date_str:
        effective_date = datetime.strptime(effective_date_str, '%Y-%m-%d').date()
    else:
        effective_date = None

    # Convert bill values to float, handling empty strings
    w_min_bill = float(w_min_bill_str) if w_min_bill_str else None
    ww_min_bill = float(ww_min_bill_str) if ww_min_bill_str else None

    # Create the Utility instance
    new_utility = Utility(
        city=city,
        state=state,
        client=client,
        population=population,
        winter_avg=winter_avg,
        meter_size=meter_size,
        effective_date=effective_date,
        source=source,
        w_min_bill=w_min_bill,
        ww_min_bill=ww_min_bill
    )
    db.session.add(new_utility)
    db.session.commit()

    # Add associated water blocks
    for i in range(1, 11):
        gallons = request.form.get(f'water_gallons_{i}')
        rate = request.form.get(f'water_rate_{i}')
        if gallons or rate:
            new_block = Block(
                gallons = float(gallons) if gallons else 0,
                rate = float(rate) if rate else 0,
                type='water',
                utility_id=new_utility.id  # Use the utility_id
            )
            db.session.add(new_block)

    # Add associated wastewater blocks
    for i in range(1, 11):
        gallons = request.form.get(f'wastewater_gallons_{i}')
        rate = request.form.get(f'wastewater_rate_{i}')
        if gallons or rate:
            new_block = Block(
                gallons = float(gallons) if gallons else 0,
                rate = float(rate) if rate else 0,
                type='wastewater',
                utility_id=new_utility.id  # Use the utility_id
            )
            db.session.add(new_block)

    db.session.commit()
    flash('Utility and blocks added successfully!', 'success')
    return redirect(url_for('main.home'))

@main.route('/update_utility/<int:id>', methods=['POST'])
def update_utility(id):
    # Fetch the utility to be updated
    utility = Utility.query.get_or_404(id)

    # Update the utility's fields with new form data
    utility.city = request.form.get('city')
    utility.state = request.form.get('state')
    utility.client = request.form.get('client')
    utility.population = request.form.get('population')
    utility.winter_avg = request.form.get('winter_avg')
    utility.meter_size = request.form.get('meter_size')

    effective_date_str = request.form.get('effective_date')
    if effective_date_str:
        utility.effective_date = datetime.strptime(effective_date_str, '%Y-%m-%d').date()
    else:
        utility.effective_date = None

    utility.source = request.form.get('source')

    w_min_bill_str = request.form.get('w_min_bill')
    ww_min_bill_str = request.form.get('ww_min_bill')
    utility.w_min_bill = float(w_min_bill_str) if w_min_bill_str else None
    utility.ww_min_bill = float(ww_min_bill_str) if ww_min_bill_str else None

    # Update existing water blocks and add new ones, or delete if cleared
    for i in range(1, 11):
        gallons = request.form.get(f'water_gallons_{i}')
        rate = request.form.get(f'water_rate_{i}')
        if gallons or rate:
            if i <= len(utility.water_blocks):
                block = utility.water_blocks[i - 1]
                block.gallons = float(gallons) if gallons else 0
                block.rate = float(rate) if rate else 0
            else:
                # If the block doesn't exist, create a new one
                new_block = Block(
                    gallons=float(gallons) if gallons else 0,
                    rate=float(rate) if rate else 0,
                    type='water',
                    utility_id=utility.id
                )
                db.session.add(new_block)
        elif i <= len(utility.water_blocks):
            # If both gallons and rate are empty, delete the block
            db.session.delete(utility.water_blocks[i - 1])

    # Update existing wastewater blocks and add new ones, or delete if cleared
    for i in range(1, 11):
        gallons = request.form.get(f'wastewater_gallons_{i}')
        rate = request.form.get(f'wastewater_rate_{i}')
        if gallons or rate:
            if i <= len(utility.wastewater_blocks):
                block = utility.wastewater_blocks[i - 1]
                block.gallons = float(gallons) if gallons else 0
                block.rate = float(rate) if rate else 0
            else:
                # If the block doesn't exist, create a new one
                new_block = Block(
                    gallons=float(gallons) if gallons else 0,
                    rate=float(rate) if rate else 0,
                    type='wastewater',
                    utility_id=utility.id
                )
                db.session.add(new_block)
        elif i <= len(utility.wastewater_blocks):
            # If both gallons and rate are empty, delete the block
            db.session.delete(utility.wastewater_blocks[i - 1])

    # Commit the changes to the database
    db.session.commit()

    flash('Utility updated successfully!', 'success')
    return redirect(url_for('main.home'))


@main.route('/delete_utility/<int:id>', methods=['POST'])
def delete_utility(id):
    utility = Utility.query.get_or_404(id)
    db.session.delete(utility)
    db.session.commit()
    flash('Utility deleted successfully!', 'success')
    return redirect(url_for('main.home'))

@main.route('/export_utilities', methods=['GET'])
def export_utilities():
    utilities = Utility.query.all()
    # Implement export logic here, e.g., generating a CSV file
    return "Export functionality not implemented yet."
