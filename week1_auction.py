#week1 introduction Python
#author @ ANHTRUNG
#22 Mars 2018

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Table, engine,desc
from sqlalchemy.orm import relationship, session, joinedload, sessionmaker
from sqlalchemy.dialects.postgresql import *

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = 'postgresql://postpres:888@localhost/auctiondb'
db = SQLAlchemy(app)

bidon = db.Table('bidon',
	db.Column('bid_id', db.Integer, db.ForeignKey('bid.id'), primary_key=True),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
   db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
	)

autionned = db.Table('auctionned',
	db.Column('auction_id', db.Integer, db.ForeignKey('auction.id'), primary_key=True),
   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
	)

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	start_time = db.Column(db.DateTime)
	name = db.Column(db.String(120), unique=True, nullable=False)
	description = db.Column(db.String(240),  nullable=False)
	owner = db.Column(db.Integer, ForeignKey('user.id'))
	auctions = db.relationship('Auction', secondary=autionned, lazy='subquery',backref=db.backref( 'item', lazy=True))
	bids= db.relationship('Bid', secondary=bidon, lazy='subquery',backref=db.backref( 'item', lazy=True))
	def __repr__(self):
		return '<Item %r>' % self.itemname

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(120), unique=True, nullable=False)
	asset = db.relationship('Item', backref='user', lazy=True)
	bids = db.relationship('Bid', backref='user', lazy=True)
	auctions = db.relationship('Auction', backref='user', lazy=True)
	def __repr__(self):
		return '<User %r>' % self.username

class Bid(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Float, unique=True, nullable=False)
	auction = db.Column(db.Integer, ForeignKey('auction.id'))
	placeby = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	onitem = db.Column(db.Integer, db.ForeignKey('item.id'),nullable=False)
	def __repr__(self):
		return '<Bid %r>' % self.price

class Auction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Float, unique=True, nullable=False)
	placeby = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	onitem = db.Column(db.Integer, db.ForeignKey('item.id'),nullable=False)
	bids = db.relationship('Bid', backref='auction', lazy=True)
	def __repr__(self):
		return '<Auction %r>' % self.price

#reset old DB
db.drop_all()

#initalize DB
db.create_all()

#create 3 user
u1 = User(id='1',username='UserOne',password='111')
u2 = User(id='2',username='UserSecond',password='222')
u3 = User(id='3',username='UserThree',password='333')

#create an item
i1=Item(id='1',name='baseball',description='golden baseball')

#Item BASEBALL auctionned by UserOne
auc1=Auction(id='1',price='800.80',placeby='1',onitem='1')

#Item BASEBALL bidden by UserSecond for firsttime
bid1 = Bid(id='1',price='801.55',placeby='2',onitem='1',auction='1')

#Item BASEBALL bidden by UserSecond for second time
bid2 = Bid(id='2',price='803.66',placeby='2',onitem='1',auction='1')

#Item BASEBALL bidden by UserThree for firsttime
bid3 = Bid(id='3',price='888.22',placeby='3',onitem='1',auction='1')

#Item BASEBALL bidden by UserThree for second time
bid4 = Bid(id='4',price='899.99',placeby='3',onitem='1',auction='1')

#Save current session
Session = sessionmaker(bind=engine)
se = Session()

#try to find every bids placed on BASEBALL
baseballbids = se.execute("select * from Bid where onitem=:id", {'id':1})
connection = se.connection(Bid)

#Perform a query to find out which user placed the highest bid
highbid_price = Bid.query.order_by(Bid.price).first()
highbid_user_id = Bid.placeby.query.filterby(Bid.price == highbid_price).first()
highbid_user_name= User.query.get(highbid_user_id)
print(highbid_user_name)
