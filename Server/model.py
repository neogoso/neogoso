# -*- coding: utf-8 -*-
from app.core import server
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from datetime import datetime

db = server.db

class NaverWebtoon(db.Model) :
	__tablename__='naverwebtoon'
	id = db.Column(db.Integer, primary_key = True)
	registered_ymdt = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	enc_writer_id = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	writer_nickname = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	modified_ymdt = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	object_id = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	writer_id = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	contents = db.Column(db.String(4096, collation = 'utf8mb4_unicode_ci'))
	comment_no = db.Column(db.Integer)
	episode = db.Column(db.Integer)
	__table_args__ = (UniqueConstraint('modified_ymdt','registered_ymdt','object_id','writer_id','comment_no', name='_customer_location_uc'),)

	def __init__ (self, registered_ymdt, enc_writer_id, writer_nickname, modified_ymdt,
					object_id, writer_id, contents, comment_no, episode) :
		self.registered_ymdt = registered_ymdt
		self.enc_writer_id = enc_writer_id
		self.writer_nickname = writer_nickname
		self.modified_ymdt = modified_ymdt
		self.object_id = object_id
		self.writer_id = writer_id
		self.contents = contents
		self.comment_no = comment_no
		self.episode = episode
