from dependencies import db


class Keywords(db.Model):
    __tablename__ = "keywords"
    # __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String, nullable=False)
    gen_date = db.Column(db.Date, nullable=False)
    week_no = db.Column(db.Integer, nullable=True)
