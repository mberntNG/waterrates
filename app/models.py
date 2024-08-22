from .extensions import db

class Utility(db.Model):
    __tablename__ = 'utility'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    client = db.Column(db.String(10), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    winter_avg = db.Column(db.String(10), nullable=True)
    meter_size = db.Column(db.String(20), nullable=True)
    effective_date = db.Column(db.Date, nullable=True)
    source = db.Column(db.String(100), nullable=True)
    w_min_bill = db.Column(db.Float, nullable=True)
    ww_min_bill = db.Column(db.Float, nullable=True)
    
    # Single relationship to blocks
    blocks = db.relationship('Block', back_populates='utility', lazy=True, cascade="all, delete-orphan")

    @property
    def water_blocks(self):
        return [block for block in self.blocks if block.type == 'water']

    @property
    def wastewater_blocks(self):
        return [block for block in self.blocks if block.type == 'wastewater']


class Block(db.Model):
    __tablename__ = 'block'

    id = db.Column(db.Integer, primary_key=True)
    gallons = db.Column(db.Integer, nullable=True)
    rate = db.Column(db.Float, nullable=True)
    type = db.Column(db.String(50), nullable=False)  # "water" or "wastewater"
    utility_id = db.Column(db.Integer, db.ForeignKey('utility.id'), nullable=False)
    
    # Back-populate relationship
    utility = db.relationship('Utility', back_populates='blocks')
