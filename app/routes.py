from html import entities
from string import printable
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from markupsafe import Markup
import plotly.graph_objs as go
import plotly.io as pio
from .extensions import db
from .models import Entity, Rate, Block
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import csv
import io

main = Blueprint('main', __name__)

def calculate_distance(lat1, lon1, lat2, lon2):
            R = 3958.8  # Radius of the Earth in Miles
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

@main.route('/')
def home():
    rates = Rate.query.all()
    all_entities = Entity.query.order_by(Entity.entity_name.asc()).all()
    selected_entity_id = request.args.get('selected_entity', type=int)
    selected_entity = Entity.query.get(selected_entity_id) if selected_entity_id else None

    distances = {}
    if selected_entity:
        for entity in all_entities:
            if entity.latitude and entity.longitude and selected_entity.latitude and selected_entity.longitude:
                distance = calculate_distance(selected_entity.latitude, selected_entity.longitude, entity.latitude, entity.longitude)
                distances[entity.id] = round(distance, 2)

    return render_template('home.html', entities=all_entities, selected_entity=selected_entity, distances=distances, rates=rates)

@main.route('/add_entity', methods=['POST'])

def add_entity():
    # Extract entity data
    entity_name = request.form.get('entity_name')
    state = request.form.get('state')
    population = request.form.get('population')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # Convert empty strings to None for numeric fields
    population = int(population) if population else None
    latitude = float(latitude) if latitude else None
    longitude = float(longitude) if longitude else None

    # Check if entity exists by entity_name
    entity = Entity.query.filter_by(entity_name=entity_name).first()
    if not entity:
        entity = Entity(
            entity_name=entity_name,
            state=state,
            population=population,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(entity)
        db.session.commit()

    # Create or update the rate entry
    rate = Rate(
        entity_id=entity.id,
        rate_type=request.form.get('rate_type'),
        rate_class=request.form.get('rate_class'),
        winter_avg=request.form.get('winter_avg'),
        meter_size=request.form.get('meter_size'),
        effective_date=datetime.strptime(request.form.get('effective_date'), '%Y-%m-%d').date() if request.form.get('effective_date') else None,
        source=request.form.get('source'),
        min_bill=request.form.get('min_bill'),
        units=request.form.get('units'),
        other_vol_rates=request.form.get('other_vol_rates'),
        updated_by=request.form.get('updated_by'),
        updated_on=datetime.strptime(request.form.get('updated_on'), '%Y-%m-%d').date() if request.form.get('updated_on') else None,
        checked_by=request.form.get('checked_by'),
        checked_on=datetime.strptime(request.form.get('checked_on'), '%Y-%m-%d').date() if request.form.get('checked_on') else None,
        notes=request.form.get('notes')
    )
    # First, add the rate to the database
    db.session.add(rate)
    db.session.commit()  # Commit the rate to ensure `rate.id` is available

    # Now add the blocks
    for i in range(1, 11):
        volume = request.form.get(f'volume_{i}', '').strip()
        rate_amount = request.form.get(f'block_rate_{i}', '').strip()
    
        if volume and rate_amount:
            try:
                volume = float(volume)
                rate_amount = float(rate_amount)
                block = Block(
                    volume=volume,
                    block_rate=rate_amount,
                    rate_id=rate.id
                )
                db.session.add(block)
            except ValueError:
                flash(f'Invalid volume or rate input for Block {i}. Skipping this block.', 'warning')

    # Commit the blocks
    db.session.commit()



    flash('Entity and rates added/updated successfully!', 'success')
    return redirect(url_for('main.home'))


@main.route('/update_entity/<int:id>', methods=['POST'])
def update_entity(id):
    # Fetch the rate and the related entity
    rate = Rate.query.get_or_404(id)
    entity = rate.entity

    # Update entity's basic information
    entity.entity_name = request.form.get('entity_name')
    entity.state = request.form.get('state')
    entity.population = request.form.get('population') if request.form.get('population') else None
    entity.latitude = request.form.get('latitude') if request.form.get('latitude') else None
    entity.longitude = request.form.get('longitude') if request.form.get('longitude') else None
    
    # Update rate's details
    rate.winter_avg = request.form.get('winter_avg')
    rate.meter_size = request.form.get('meter_size')
    rate.rate_type = request.form.get('rate_type')
    rate.rate_class = request.form.get('rate_class')
    rate.effective_date = datetime.strptime(request.form.get('effective_date'), '%Y-%m-%d').date() if request.form.get('effective_date') else None
    rate.source = request.form.get('source')
    rate.min_bill = request.form.get('min_bill')
    rate.units = request.form.get('units')
    rate.notes = request.form.get('notes')
    rate.updated_by = request.form.get('updated_by')
    rate.updated_on = datetime.strptime(request.form.get('updated_on'), '%Y-%m-%d').date() if request.form.get('updated_on') else None
    rate.checked_by = request.form.get('checked_by')
    rate.checked_on = datetime.strptime(request.form.get('checked_on'), '%Y-%m-%d').date() if request.form.get('checked_on') else None

    db.session.commit()

    # Handle block updates (assuming blocks are updated by ID or added if new)
    existing_blocks = {block.id: block for block in rate.blocks}  # Create a dictionary of existing blocks

    for i in range(1, 11):
        volume = request.form.get(f'volume_{i}')
        rate_amount = request.form.get(f'block_rate_{i}')
        
        # Only process if both volume and rate are provided
        if volume and rate_amount:
            try:
                volume = float(volume)
                rate_amount = float(rate_amount)
                
                # Update existing block if present
                if i <= len(rate.blocks):
                    block = rate.blocks[i-1]
                    block.volume = volume
                    block.block_rate = rate_amount
                else:
                    # Create a new block if necessary
                    new_block = Block(
                        volume=volume,
                        block_rate=rate_amount,
                        rate_id=rate.id
                    )
                    db.session.add(new_block)

            except ValueError:
                flash(f"Error processing block {i}: Invalid volume or rate", 'danger')

    db.session.commit()
    flash('Entity and rates updated successfully!', 'success')
    return redirect(url_for('main.home'))


@main.route('/delete_rate/<int:id>', methods=['POST'])
def delete_rate(id):
    rate = Rate.query.get_or_404(id)
    db.session.delete(rate)
    db.session.commit()
    flash('Rate deleted successfully!', 'success')
    return redirect(url_for('main.home'))


@main.route('/utility_graph', methods=['GET', 'POST'])
def utility_graph():
    usage_amount = int(request.form.get('usage_amount', 2500))  # Default usage amount
    selected_rates = request.form.getlist('selected_utilities')   
    if not selected_rates:
        selected_rates = [str(rate.id) for rate in Rate.query.all()]
    reference_entity_name = request.form.get('reference_entity')
    if reference_entity_name:
        reference_entity = Entity.query.filter_by(entity_name=reference_entity_name).first()
    else:
        reference_entity = None

    rates = Rate.query.filter_by(rate_class="Residential").all()


    table_data = []
    entity_names = []
    water_costs = []
    wastewater_costs = []
    total_costs = []
    distances = []


    for rate in rates:
        # Calculate water cost
        entity_name = rate.entity.entity_name
        state=rate.entity.state
        population=rate.entity.population
        total_cost = 0
        remaining_usage = usage_amount
        calculated_distance = 0

        for block in rate.blocks:
            if remaining_usage > 0:
                block_usage = min(remaining_usage, block.volume)
                total_cost += block_usage / 1000 * block.rate
                remaining_usage -= block_usage
            else:
                break

        # Apply minimum water bill and other volumetric rate
        total_cost = total_cost + rate.min_bill + rate.other_vol_rates * usage_amount

       
        # Total cost
        total_cost = total_cost

        # Store data for the table
        table_data.append({
            'name': entity_name,
            'state':state,
            'population':population,
            'water_cost': total_cost,
            'wastewater_cost': total_cost,
            'total_cost': total_cost,
            'id': rate.id,
            'distance': 0
        })

        # Only include selected utilities in the graph
        if str(rate.id) in selected_rates:
            entity_names.append(entity_name)
            water_costs.append(total_cost)
            wastewater_costs.append(total_cost)
            total_costs.append(total_cost)
            distances.append(calculated_distance) 

    # Create the stacked bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Water', x=entity_names, y=water_costs, marker_color='blue'),
        go.Bar(name='Wastewater', x=entity_names, y=wastewater_costs, marker_color='green')
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
    return render_template('utility_graph.html', graph_html=Markup(graph_html), usage_amount=usage_amount, table_data=table_data, selected_rates=selected_rates)

@main.route('/export_rates', methods=['POST'])
def export_rates():
    data = request.json
    selected_rate_ids = data.get('rates', [])
    
    if not selected_rate_ids:
        return jsonify({'error': 'No rates selected'}), 400

    # Fetch the selected rates from the database
    rates = Rate.query.filter(Rate.id.in_(selected_rate_ids)).all()

    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow([
        'Entity', 'State', 'Type', 'Population', 'Rate Type', 'Rate Class', 'Meter Size', 
        'Effective Date', 'Min Bill', 'Units', 'Block 1 Volume', 'Block 2 Volume', 
        'Block 3 Volume', 'Block 4 Volume', 'Block 5 Volume', 'Block 6 Volume', 
        'Block 7 Volume', 'Block 8 Volume', 'Block 9 Volume', 'Block 10 Volume', 
        'Block 1 Rate', 'Block 2 Rate', 'Block 3 Rate', 'Block 4 Rate', 'Block 5 Rate', 
        'Block 6 Rate', 'Block 7 Rate', 'Block 8 Rate', 'Block 9 Rate', 'Block 10 Rate', 
        'Other Volumetric Rates', 'Source'
    ])
    
    # Write the rate data
    for rate in rates:
        # Extract entity-level data
        entity = rate.entity
        entity_data = [
            entity.entity_name,  # Entity name
            entity.state,        # State
            entity.entity_type,  #Type, e.g. City, District
            entity.population    # Population
        ]
        
        # Extract rate-level data
        rate_data = [
            rate.rate_type,       # Rate Type
            rate.rate_class,      # Rate Class
            rate.meter_size,      # Meter Size
            rate.effective_date,  # Effective Date
            rate.min_bill,        # Minimum Bill
            rate.units            # Units (kgal or CCF)
        ]
        
        # Extract block volumes and rates (up to 10)
        block_volumes = ['' for _ in range(10)]  # Default empty values for up to 10 blocks
        block_rates = ['' for _ in range(10)]    # Default empty values for up to 10 blocks
        
        for i, block in enumerate(rate.blocks[:10]):  # Only take the first 10 blocks
            block_volumes[i] = block.volume
            block_rates[i] = block.block_rate
        
        # Extract remaining fields
        additional_data = [
            rate.other_vol_rates,  # Other volumetric rates
            rate.source            # Source
        ]

        # Combine all data for this row
        row = entity_data + rate_data + block_volumes + block_rates + additional_data
        writer.writerow(row)

    # Create a response with the CSV content
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=rates_export.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

@main.route('/search_entity', methods=['GET'])
def search_entity():
    search_term = request.args.get('query', '').strip()

    if not search_term:
        return jsonify([])  # Return an empty list if no query is provided.

    # Find entities whose name matches the search term (case-insensitive)
    matching_entities = Entity.query.filter(Entity.entity_name.ilike(f"%{search_term}%")).all()

    # Return a list of matching entities with their relevant fields
    results = []
    for entity in matching_entities:
        results.append({
            'id': entity.id,
            'entity_name': entity.entity_name,
            'state': entity.state,
            'entity_type': entity.entity_type,
            'population': entity.population,
            'latitude': entity.latitude,
            'longitude': entity.longitude
        })

    return jsonify(results)



@main.route('/get_entity_details/<int:entity_id>', methods=['GET'])
def get_entity_details(entity_id):
    entity = Entity.query.get(entity_id)

    if entity:
        return jsonify({
            'entity_name': entity.entity_name,
            'state': entity.state,
            'entity_type': entity.entity_type,
            'population': entity.population,
            'latitude': entity.latitude,
            'longitude': entity.longitude
        })
    else:
        return jsonify({'error': 'Entity not found'}), 404

