import plotly.graph_objs as go
import plotly.io as pio
from flask import Blueprint, render_template, request, redirect, url_for, flash
from markupsafe import Markup
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

@main.route('/utility_graph', methods=['GET', 'POST'])
def utility_graph():
    usage_amount = int(request.form.get('usage_amount', 2500))  # Default usage amount to 2500 gallons

    # Get selected utilities or default to all if none are selected
    selected_utilities = request.form.getlist('selected_utilities')
    if not selected_utilities:
        selected_utilities = [str(utility.id) for utility in Utility.query.all()]

    utilities = Utility.query.all()
    utility_names = []
    water_costs = []
    wastewater_costs = []
    total_costs = []
    table_data = []

    for utility in utilities:
        # Calculate water cost
        water_total_cost = 0
        remaining_usage = usage_amount

        for block in utility.water_blocks:
            if remaining_usage > 0:
                block_usage = min(remaining_usage, block.gallons)
                water_total_cost += block_usage / 1000 * block.rate
                remaining_usage -= block_usage
            else:
                break

        # Apply minimum water bill
        water_total_cost = water_total_cost + utility.w_min_bill

        # Calculate wastewater cost
        wastewater_total_cost = 0
        remaining_usage = usage_amount

        for block in utility.wastewater_blocks:
            if remaining_usage > 0:
                block_usage = min(remaining_usage, block.gallons)
                wastewater_total_cost += block_usage / 1000 * block.rate
                remaining_usage -= block_usage
            else:
                break

        # Apply minimum wastewater bill
        wastewater_total_cost = wastewater_total_cost + utility.ww_min_bill

        # Total cost
        total_cost = water_total_cost + wastewater_total_cost

        # Store data for the table
        table_data.append({
            'name': utility.city,
            'water_cost': water_total_cost,
            'wastewater_cost': wastewater_total_cost,
            'total_cost': total_cost,
            'id': utility.id
        })

        # Only include selected utilities in the graph
        if str(utility.id) in selected_utilities:
            utility_names.append(utility.city)
            water_costs.append(water_total_cost)
            wastewater_costs.append(wastewater_total_cost)
            total_costs.append(total_cost)

    # Create the stacked bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Water', x=utility_names, y=water_costs, marker_color='blue'),
        go.Bar(name='Wastewater', x=utility_names, y=wastewater_costs, marker_color='green')
    ])

    fig.update_layout(
        title=f'Total Water and Wastewater Costs by Utility for {usage_amount} Gallons',
        xaxis_title='Utility',
        yaxis_title='Total Cost (USD)',
        barmode='stack'
    )

    # Generate the HTML for the plot
    graph_html = pio.to_html(fig, full_html=False)

    # Pass the graph HTML, table data, selected utilities, and usage amount to the template
    return render_template('utility_graph.html', graph_html=Markup(graph_html), usage_amount=usage_amount, table_data=table_data, selected_utilities=selected_utilities)



