from .extensions import db

class Utility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    client = db.Column(db.String(10), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    winter_avg = db.Column(db.String(10), nullable=True)
    meter_size = db.Column(db.String(20), nullable=True)
    effective_date = db.Column(db.Date, nullable=True)
    
    w_min_bill = db.Column(db.Float, nullable=True)

    w_block_1_gals = db.Column(db.Integer, nullable=True)
    w_block_2_gals = db.Column(db.Integer, nullable=True)
    w_block_3_gals = db.Column(db.Integer, nullable=True)
    w_block_4_gals = db.Column(db.Integer, nullable=True)
    w_block_5_gals = db.Column(db.Integer, nullable=True)
    w_block_6_gals = db.Column(db.Integer, nullable=True)
    w_block_7_gals = db.Column(db.Integer, nullable=True)
    w_block_8_gals = db.Column(db.Integer, nullable=True)
    w_block_9_gals = db.Column(db.Integer, nullable=True)
    w_block_10_gals = db.Column(db.Integer, nullable=True)

    w_block_1_rate = db.Column(db.Float, nullable=True)
    w_block_2_rate = db.Column(db.Float, nullable=True)
    w_block_3_rate = db.Column(db.Float, nullable=True)
    w_block_4_rate = db.Column(db.Float, nullable=True)
    w_block_5_rate = db.Column(db.Float, nullable=True)
    w_block_6_rate = db.Column(db.Float, nullable=True)
    w_block_7_rate = db.Column(db.Float, nullable=True)
    w_block_8_rate = db.Column(db.Float, nullable=True)
    w_block_9_rate = db.Column(db.Float, nullable=True)
    w_block_10_rate = db.Column(db.Float, nullable=True)

    ww_min_bill = db.Column(db.Float, nullable=True)

    ww_block_1_gals = db.Column(db.Integer, nullable=True)
    ww_block_2_gals = db.Column(db.Integer, nullable=True)
    ww_block_3_gals = db.Column(db.Integer, nullable=True)
    ww_block_4_gals = db.Column(db.Integer, nullable=True)
    ww_block_5_gals = db.Column(db.Integer, nullable=True)
    ww_block_6_gals = db.Column(db.Integer, nullable=True)
    ww_block_7_gals = db.Column(db.Integer, nullable=True)
    ww_block_8_gals = db.Column(db.Integer, nullable=True)
    ww_block_9_gals = db.Column(db.Integer, nullable=True)
    ww_block_10_gals = db.Column(db.Integer, nullable=True)

    ww_block_1_rate = db.Column(db.Float, nullable=True)
    ww_block_2_rate = db.Column(db.Float, nullable=True)
    ww_block_3_rate = db.Column(db.Float, nullable=True)
    ww_block_4_rate = db.Column(db.Float, nullable=True)
    ww_block_5_rate = db.Column(db.Float, nullable=True)
    ww_block_6_rate = db.Column(db.Float, nullable=True)
    ww_block_7_rate = db.Column(db.Float, nullable=True)
    ww_block_8_rate = db.Column(db.Float, nullable=True)
    ww_block_9_rate = db.Column(db.Float, nullable=True)
    ww_block_10_rate = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Utility {self.city}, {self.state}>'
