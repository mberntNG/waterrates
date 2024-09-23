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
        min_bill=request.form.get('min_bill') if request.form.get('min_bill') else 0,
        units=request.form.get('units'),
        other_vol_rates=request.form.get('other_vol_rates') if request.form.get('other_vol_rates') else 0,
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


@main.route('/calculate_rates', methods=['GET', 'POST'])
def calculate_rates():
    # Fetch all entities along with their related rates and blocks
    entities = Entity.query.options(
        db.joinedload(Entity.rates).joinedload(Rate.blocks)
    ).all()

    # Check for POST to calculate rates or display page initially
    if request.method == 'POST':
        volume = float(request.form.get('volume', 2000))  # default to 2000
        unit = request.form.get('unit', 'kgal')  # default to kgal
        winter_avg_volume = float(request.form.get('winter_avg', 7000))  # default to 7000
        rate_type = request.form.get('rate_type', 'both')  # water/wastewater/both
        
        # Perform calculations 
        results = calculate_rate_for_entities(entities, volume, unit, winter_avg_volume, rate_type)
        
        # Pass the calculated results to the template
        for result in results:
            result.water_bill = result.water_bill or 0.0
            result.wastewater_bill = result.wastewater_bill or 0.0
            result.total_bill = result.total_bill or 0.0

        return render_template('calculate_rates.html', entities=entities, results=results)
    
    return render_template('calculate_rates.html', entities=entities)

def calculate_rate_for_entities(entities, volume, unit, winter_avg_volume, rate_type):
    results = {}

    for entity in entities:
        for rate in entity.rates:
            # Group by entity_name, rate_class, and meter_size
            key = (entity.entity_name, rate.rate_class, rate.meter_size)
            if key not in results:
                results[key] = {
                    'entity': entity.entity_name or "N/A",
                    'rate_class': rate.rate_class or "N/A",
                    'meter_size': rate.meter_size or "N/A",
                    'population': entity.population or 0,
                    'water_bill': 0.0,
                    'wastewater_bill': 0.0,
                    'total_bill': 0.0,
                    'distance': 0,
                }

            # Determine if winter average applies (for wastewater)
            max_volume = volume
            if rate.winter_avg == 'Yes' and rate.rate_type == 'Wastewater':
                max_volume = min(volume, winter_avg_volume)

            # Calculate the bill
            total_volume = max_volume/1000 if rate.rate_type == 'Wastewater' else volume/1000
            block_total = 0
            remaining_volume = total_volume

            # Calculate block rates
            for block in rate.blocks:
                block_volume = min(block.volume or 0, remaining_volume)
                block_total += block_volume * (block.block_rate or 0)
                remaining_volume -= block_volume
                if remaining_volume <= 0:
                    break

            # Add minimum bill and other volumetric rates (with None handling)
            total_bill = (rate.min_bill or 0) + block_total + ((rate.other_vol_rates or 0) * total_volume)

            if rate.rate_type == 'Water':
                results[key]['water_bill'] = total_bill
            elif rate.rate_type == 'Wastewater':
                results[key]['wastewater_bill'] = total_bill

            results[key]['total_bill'] = results[key]['water_bill'] + results[key]['wastewater_bill']
            

    return list(results.values())





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

