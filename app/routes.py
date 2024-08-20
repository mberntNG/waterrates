from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify, Response
from app.extensions import db
from app.models import Utility
from datetime import datetime
import csv
from io import StringIO

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    utilities = Utility.query.all()
    return render_template('home.html', utilities=utilities)

@main.route('/add_utility', methods=['POST'])
def add_utility():
    if request.method == 'POST':
        # Convert the date string to a Python date object
        effective_date = None
        if request.form['effective_date']:
            effective_date = datetime.strptime(request.form['effective_date'], '%Y-%m-%d').date()
        
        # Handle potential blank fields for numeric values
        w_min_bill = float(request.form['w_min_bill']) if request.form['w_min_bill'] else None
        ww_min_bill = float(request.form['ww_min_bill']) if request.form['ww_min_bill'] else None
        
        # Water Blocks
        w_block_1_gals = float(request.form['w_block_1_gals']) if request.form['w_block_1_gals'] else None
        w_block_1_rate = float(request.form['w_block_1_rate']) if request.form['w_block_1_rate'] else None
        w_block_2_gals = float(request.form['w_block_2_gals']) if request.form['w_block_2_gals'] else None
        w_block_2_rate = float(request.form['w_block_2_rate']) if request.form['w_block_2_rate'] else None
        w_block_3_gals = float(request.form['w_block_3_gals']) if request.form['w_block_3_gals'] else None
        w_block_3_rate = float(request.form['w_block_3_rate']) if request.form['w_block_3_rate'] else None
        w_block_4_gals = float(request.form['w_block_4_gals']) if request.form['w_block_4_gals'] else None
        w_block_4_rate = float(request.form['w_block_4_rate']) if request.form['w_block_4_rate'] else None
        w_block_5_gals = float(request.form['w_block_5_gals']) if request.form['w_block_5_gals'] else None
        w_block_5_rate = float(request.form['w_block_5_rate']) if request.form['w_block_5_rate'] else None
        w_block_6_gals = float(request.form['w_block_6_gals']) if request.form['w_block_6_gals'] else None
        w_block_6_rate = float(request.form['w_block_6_rate']) if request.form['w_block_6_rate'] else None
        w_block_7_gals = float(request.form['w_block_7_gals']) if request.form['w_block_7_gals'] else None
        w_block_7_rate = float(request.form['w_block_7_rate']) if request.form['w_block_7_rate'] else None
        w_block_8_gals = float(request.form['w_block_8_gals']) if request.form['w_block_8_gals'] else None
        w_block_8_rate = float(request.form['w_block_8_rate']) if request.form['w_block_8_rate'] else None
        w_block_9_gals = float(request.form['w_block_9_gals']) if request.form['w_block_9_gals'] else None
        w_block_9_rate = float(request.form['w_block_9_rate']) if request.form['w_block_9_rate'] else None
        w_block_10_gals = float(request.form['w_block_10_gals']) if request.form['w_block_10_gals'] else None
        w_block_10_rate = float(request.form['w_block_10_rate']) if request.form['w_block_10_rate'] else None
        
        # Wastewater Blocks
        ww_block_1_gals = float(request.form['ww_block_1_gals']) if request.form['ww_block_1_gals'] else None
        ww_block_1_rate = float(request.form['ww_block_1_rate']) if request.form['ww_block_1_rate'] else None
        ww_block_2_gals = float(request.form['ww_block_2_gals']) if request.form['ww_block_2_gals'] else None
        ww_block_2_rate = float(request.form['ww_block_2_rate']) if request.form['ww_block_2_rate'] else None
        ww_block_3_gals = float(request.form['ww_block_3_gals']) if request.form['ww_block_3_gals'] else None
        ww_block_3_rate = float(request.form['ww_block_3_rate']) if request.form['ww_block_3_rate'] else None
        ww_block_4_gals = float(request.form['ww_block_4_gals']) if request.form['ww_block_4_gals'] else None
        ww_block_4_rate = float(request.form['ww_block_4_rate']) if request.form['ww_block_4_rate'] else None
        ww_block_5_gals = float(request.form['ww_block_5_gals']) if request.form['ww_block_5_gals'] else None
        ww_block_5_rate = float(request.form['ww_block_5_rate']) if request.form['ww_block_5_rate'] else None
        ww_block_6_gals = float(request.form['ww_block_6_gals']) if request.form['ww_block_6_gals'] else None
        ww_block_6_rate = float(request.form['ww_block_6_rate']) if request.form['ww_block_6_rate'] else None
        ww_block_7_gals = float(request.form['ww_block_7_gals']) if request.form['ww_block_7_gals'] else None
        ww_block_7_rate = float(request.form['ww_block_7_rate']) if request.form['ww_block_7_rate'] else None
        ww_block_8_gals = float(request.form['ww_block_8_gals']) if request.form['ww_block_8_gals'] else None
        ww_block_8_rate = float(request.form['ww_block_8_rate']) if request.form['ww_block_8_rate'] else None
        ww_block_9_gals = float(request.form['ww_block_9_gals']) if request.form['ww_block_9_gals'] else None
        ww_block_9_rate = float(request.form['ww_block_9_rate']) if request.form['ww_block_9_rate'] else None
        ww_block_10_gals = float(request.form['ww_block_10_gals']) if request.form['ww_block_10_gals'] else None
        ww_block_10_rate = float(request.form['ww_block_10_rate']) if request.form['ww_block_10_rate'] else None
        
        # Create a new Utility instance with all the fields
        new_utility = Utility(
            city=request.form['city'],
            state=request.form['state'],
            client=request.form['client'],
            population=request.form['population'],
            winter_avg=request.form['winter_avg'],
            meter_size=request.form['meter_size'],
            effective_date=effective_date,
            source=request.form['source'],
            w_min_bill=w_min_bill,
            ww_min_bill=ww_min_bill,
            w_block_1_gals=w_block_1_gals,
            w_block_1_rate=w_block_1_rate,
            w_block_2_gals=w_block_2_gals,
            w_block_2_rate=w_block_2_rate,
            w_block_3_gals=w_block_3_gals,
            w_block_3_rate=w_block_3_rate,
            w_block_4_gals=w_block_4_gals,
            w_block_4_rate=w_block_4_rate,
            w_block_5_gals=w_block_5_gals,
            w_block_5_rate=w_block_5_rate,
            w_block_6_gals=w_block_6_gals,
            w_block_6_rate=w_block_6_rate,
            w_block_7_gals=w_block_7_gals,
            w_block_7_rate=w_block_7_rate,
            w_block_8_gals=w_block_8_gals,
            w_block_8_rate=w_block_8_rate,
            w_block_9_gals=w_block_9_gals,
            w_block_9_rate=w_block_9_rate,
            w_block_10_gals=w_block_10_gals,
            w_block_10_rate=w_block_10_rate,
            ww_block_1_gals=ww_block_1_gals,
            ww_block_1_rate=ww_block_1_rate,
            ww_block_2_gals=ww_block_2_gals,
            ww_block_2_rate=ww_block_2_rate,
            ww_block_3_gals=ww_block_3_gals,
            ww_block_3_rate=ww_block_3_rate,
            ww_block_4_gals=ww_block_4_gals,
            ww_block_4_rate=ww_block_4_rate,
            ww_block_5_gals=ww_block_5_gals,
            ww_block_5_rate=ww_block_5_rate,
            ww_block_6_gals=ww_block_6_gals,
            ww_block_6_rate=ww_block_6_rate,
            ww_block_7_gals=ww_block_7_gals,
            ww_block_7_rate=ww_block_7_rate,
            ww_block_8_gals=ww_block_8_gals,
            ww_block_8_rate=ww_block_8_rate,
            ww_block_9_gals=ww_block_9_gals,
            ww_block_9_rate=ww_block_9_rate,
            ww_block_10_gals=ww_block_10_gals,
            ww_block_10_rate=ww_block_10_rate,
        )
        
        # Add the new utility to the session and commit
        db.session.add(new_utility)
        db.session.commit()
        flash('Utility added successfully!', 'success')
        return redirect(url_for('main.home'))

@main.route('/update_utility/<int:id>', methods=['POST'])
def update_utility(id):
    utility = Utility.query.get_or_404(id)
    if request.method == 'POST':
        # Update basic fields
        utility.city = request.form['city']
        utility.state = request.form['state']
        utility.client = request.form['client']
        utility.population = request.form['population']
        utility.winter_avg = request.form['winter_avg']
        utility.meter_size = request.form['meter_size']
        
        # Handle the effective date field
        if request.form['effective_date']:
            utility.effective_date = datetime.strptime(request.form['effective_date'], '%Y-%m-%d').date()
        else:
            utility.effective_date = None

        utility.source = request.form['source']

        # Handle potential blank fields for numeric values
        utility.w_min_bill = float(request.form['w_min_bill']) if request.form['w_min_bill'] else None
        utility.ww_min_bill = float(request.form['ww_min_bill']) if request.form['ww_min_bill'] else None
        
        # Water Blocks
        utility.w_block_1_gals = float(request.form['w_block_1_gals']) if request.form['w_block_1_gals'] else None
        utility.w_block_1_rate = float(request.form['w_block_1_rate']) if request.form['w_block_1_rate'] else None
        utility.w_block_2_gals = float(request.form['w_block_2_gals']) if request.form['w_block_2_gals'] else None
        utility.w_block_2_rate = float(request.form['w_block_2_rate']) if request.form['w_block_2_rate'] else None
        utility.w_block_3_gals = float(request.form['w_block_3_gals']) if request.form['w_block_3_gals'] else None
        utility.w_block_3_rate = float(request.form['w_block_3_rate']) if request.form['w_block_3_rate'] else None
        utility.w_block_4_gals = float(request.form['w_block_4_gals']) if request.form['w_block_4_gals'] else None
        utility.w_block_4_rate = float(request.form['w_block_4_rate']) if request.form['w_block_4_rate'] else None
        utility.w_block_5_gals = float(request.form['w_block_5_gals']) if request.form['w_block_5_gals'] else None
        utility.w_block_5_rate = float(request.form['w_block_5_rate']) if request.form['w_block_5_rate'] else None
        utility.w_block_6_gals = float(request.form['w_block_6_gals']) if request.form['w_block_6_gals'] else None
        utility.w_block_6_rate = float(request.form['w_block_6_rate']) if request.form['w_block_6_rate'] else None
        utility.w_block_7_gals = float(request.form['w_block_7_gals']) if request.form['w_block_7_gals'] else None
        utility.w_block_7_rate = float(request.form['w_block_7_rate']) if request.form['w_block_7_rate'] else None
        utility.w_block_8_gals = float(request.form['w_block_8_gals']) if request.form['w_block_8_gals'] else None
        utility.w_block_8_rate = float(request.form['w_block_8_rate']) if request.form['w_block_8_rate'] else None
        utility.w_block_9_gals = float(request.form['w_block_9_gals']) if request.form['w_block_9_gals'] else None
        utility.w_block_9_rate = float(request.form['w_block_9_rate']) if request.form['w_block_9_rate'] else None
        utility.w_block_10_gals = float(request.form['w_block_10_gals']) if request.form['w_block_10_gals'] else None
        utility.w_block_10_rate = float(request.form['w_block_10_rate']) if request.form['w_block_10_rate'] else None
        
        # Wastewater Blocks
        utility.ww_block_1_gals = float(request.form['ww_block_1_gals']) if request.form['ww_block_1_gals'] else None
        utility.ww_block_1_rate = float(request.form['ww_block_1_rate']) if request.form['ww_block_1_rate'] else None
        utility.ww_block_2_gals = float(request.form['ww_block_2_gals']) if request.form['ww_block_2_gals'] else None
        utility.ww_block_2_rate = float(request.form['ww_block_2_rate']) if request.form['ww_block_2_rate'] else None
        utility.ww_block_3_gals = float(request.form['ww_block_3_gals']) if request.form['ww_block_3_gals'] else None
        utility.ww_block_3_rate = float(request.form['ww_block_3_rate']) if request.form['ww_block_3_rate'] else None
        utility.ww_block_4_gals = float(request.form['ww_block_4_gals']) if request.form['ww_block_4_gals'] else None
        utility.ww_block_4_rate = float(request.form['ww_block_4_rate']) if request.form['ww_block_4_rate'] else None
        utility.ww_block_5_gals = float(request.form['ww_block_5_gals']) if request.form['ww_block_5_gals'] else None
        utility.ww_block_5_rate = float(request.form['ww_block_5_rate']) if request.form['ww_block_5_rate'] else None
        utility.ww_block_6_gals = float(request.form['ww_block_6_gals']) if request.form['ww_block_6_gals'] else None
        utility.ww_block_6_rate = float(request.form['ww_block_6_rate']) if request.form['ww_block_6_rate'] else None
        utility.ww_block_7_gals = float(request.form['ww_block_7_gals']) if request.form['ww_block_7_gals'] else None
        utility.ww_block_7_rate = float(request.form['ww_block_7_rate']) if request.form['ww_block_7_rate'] else None
        utility.ww_block_8_gals = float(request.form['ww_block_8_gals']) if request.form['ww_block_8_gals'] else None
        utility.ww_block_8_rate = float(request.form['ww_block_8_rate']) if request.form['ww_block_8_rate'] else None
        utility.ww_block_9_gals = float(request.form['ww_block_9_gals']) if request.form['ww_block_9_gals'] else None
        utility.ww_block_9_rate = float(request.form['ww_block_9_rate']) if request.form['ww_block_9_rate'] else None
        utility.ww_block_10_gals = float(request.form['ww_block_10_gals']) if request.form['ww_block_10_gals'] else None
        utility.ww_block_10_rate = float(request.form['ww_block_10_rate']) if request.form['ww_block_10_rate'] else None
        
        # Commit the changes to the database
        db.session.commit()
        flash('Utility updated successfully!', 'success')
        return redirect(url_for('main.home'))


@main.route('/export_utilities')
def export_utilities():
    # Query all utilities from the database
    utilities = Utility.query.all()

    # Create a string buffer to hold the CSV data
    output = StringIO()
    writer = csv.writer(output)

    # Write the CSV header
    writer.writerow([
        "City", "State", "Client", "Population", "Winter Avg", "Meter Size",
        "Effective Date", "Source", "Water Min Bill", "Wastewater Min Bill",
        "W Block 1 Gals", "W Block 1 Rate", "W Block 2 Gals", "W Block 2 Rate",
        "W Block 3 Gals", "W Block 3 Rate", "W Block 4 Gals", "W Block 4 Rate",
        "W Block 5 Gals", "W Block 5 Rate", "W Block 6 Gals", "W Block 6 Rate",
        "W Block 7 Gals", "W Block 7 Rate", "W Block 8 Gals", "W Block 8 Rate",
        "W Block 9 Gals", "W Block 9 Rate", "W Block 10 Gals", "W Block 10 Rate",
        "WW Block 1 Gals", "WW Block 1 Rate", "WW Block 2 Gals", "WW Block 2 Rate",
        "WW Block 3 Gals", "WW Block 3 Rate", "WW Block 4 Gals", "WW Block 4 Rate",
        "WW Block 5 Gals", "WW Block 5 Rate", "WW Block 6 Gals", "WW Block 6 Rate",
        "WW Block 7 Gals", "WW Block 7 Rate", "WW Block 8 Gals", "WW Block 8 Rate",
        "WW Block 9 Gals", "WW Block 9 Rate", "WW Block 10 Gals", "WW Block 10 Rate"
    ])

    # Write the CSV rows
    for utility in utilities:
        writer.writerow([
            utility.city, utility.state, utility.client, utility.population,
            utility.winter_avg, utility.meter_size,
            utility.effective_date.strftime('%Y-%m-%d') if utility.effective_date else '',
            utility.source, utility.w_min_bill, utility.ww_min_bill,
            utility.w_block_1_gals, utility.w_block_1_rate, utility.w_block_2_gals, utility.w_block_2_rate,
            utility.w_block_3_gals, utility.w_block_3_rate, utility.w_block_4_gals, utility.w_block_4_rate,
            utility.w_block_5_gals, utility.w_block_5_rate, utility.w_block_6_gals, utility.w_block_6_rate,
            utility.w_block_7_gals, utility.w_block_7_rate, utility.w_block_8_gals, utility.w_block_8_rate,
            utility.w_block_9_gals, utility.w_block_9_rate, utility.w_block_10_gals, utility.w_block_10_rate,
            utility.ww_block_1_gals, utility.ww_block_1_rate, utility.ww_block_2_gals, utility.ww_block_2_rate,
            utility.ww_block_3_gals, utility.ww_block_3_rate, utility.ww_block_4_gals, utility.ww_block_4_rate,
            utility.ww_block_5_gals, utility.ww_block_5_rate, utility.ww_block_6_gals, utility.ww_block_6_rate,
            utility.ww_block_7_gals, utility.ww_block_7_rate, utility.ww_block_8_gals, utility.ww_block_8_rate,
            utility.ww_block_9_gals, utility.ww_block_9_rate, utility.ww_block_10_gals, utility.ww_block_10_rate
        ])

    # Ensure we reset the buffer's position to the start
    output.seek(0)

    # Return the CSV file as a response
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=utilities.csv"})

@main.route('/delete_utility/<int:id>', methods=['POST'])
def delete_utility(id):
    utility = Utility.query.get_or_404(id)
    db.session.delete(utility)
    db.session.commit()
    flash('Utility deleted successfully!', 'success')
    return redirect(url_for('main.home'))
