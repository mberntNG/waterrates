from .extensions import db
from datetime import datetime

class Entity(db.Model):
    __tablename__ = 'entity'

    id = db.Column(db.Integer, primary_key=True)
    entity_name = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=False)
    population = db.Column(db.Integer, nullable=True)
    area_sq_mi = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Relationship to Rate
    rates = db.relationship('Rate', back_populates='entity', lazy=True, cascade="all, delete-orphan")


class Rate(db.Model):
    __tablename__ = 'rate'

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    winter_avg = db.Column(db.String(10), nullable=True)
    rate_type = db.Column(db.String(10), nullable=True)  # Specifies 'water' or 'wastewater'
    rate_class = db.Column(db.String(50), nullable=True) # Specifies 'Residential', 'Commercial', 'etc.'
    meter_size = db.Column(db.String(20), nullable=True)
    effective_date = db.Column(db.Date, nullable=True)
    source = db.Column(db.String(400), nullable=True)
    min_bill = db.Column(db.Float, nullable=True)
    other_vol_rates = db.Column(db.Float, nullable=True)
    units = db.Column(db.String(4), nullable=True)
    updated_on = db.Column(db.Date, nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    checked_on = db.Column(db.Date, nullable=True)
    checked_by = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # Relationship back to Entity
    entity = db.relationship('Entity', back_populates='rates')

    # Relationship to Block
    blocks = db.relationship('Block', back_populates='rate', lazy=True, cascade="all, delete-orphan")


class Block(db.Model):
    __tablename__ = 'block'

    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer, nullable=True)
    block_rate = db.Column(db.Float, nullable=True)  # Renamed to avoid conflict with 'Rate'
    rate_id = db.Column(db.Integer, db.ForeignKey('rate.id'), nullable=False)

    # Relationship back to Rate
    rate = db.relationship('Rate', back_populates='blocks')