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
	contents = db.Column(db.String(2048, collation = 'utf8mb4_unicode_ci'))
	comment_no = db.Column(db.Integer)
	episode = db.Column(db.Integer)
	url = db.Column(db.String(2048, collation = 'utf8mb4_unicode_ci'))
	__table_args__ = (UniqueConstraint('modified_ymdt','registered_ymdt','object_id','writer_id','comment_no','episode', name='naverwebtoon_unique'),)
	
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

class NaverNews(db.Model) :
	__tablename__='navernews'
	id = db.Column(db.Integer, primary_key = True)
	commentNo = db.Column(db.Integer)
	contents = db.Column(db.String(2048, collation = 'utf8mb4_unicode_ci'))
	maskedUserId = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	modTime = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	objectId = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	parentCommentNo = db.Column(db.Integer)
	profileUserId = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	regTime = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	userIdNo = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	userName = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	title = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'))
	oid = db.Column(db.Integer)
	aid = db.Column(db.Integer)
	url = db.Column(db.String(2048, collation = 'utf8mb4_unicode_ci'))
	__table_args__ = (UniqueConstraint('commentNo','modTime','objectId','parentCommentNo','userIdNo','regTime','oid','aid', name='navernews_unique'),)

	def __init__(self,commentNo,contents,maskedUserId,modTime,objectId,parentCommentNo,profileUserId,regTime,userIdNo,userName,title,oid,aid,url) :
		self.commentNo = commentNo
		self.contents = contents
		self.maskedUserId = maskedUserId
		self.modTime = modTime
		self.objectId = objectId
		self.parentCommentNo = parentCommentNo
		self.profileUserId = profileUserId
		self.regTime = regTime
		self.userIdNo = userIdNo
		self.userName = userName
		self.title = title
		self.oid = oid
		self.aid = aid
		self.url = url

class SlangWord(db.Model):
	__tablename__ = 'slangword'
	id = db.Column(db.Integer, primary_key = True)
	word = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'), unique=True)
	wordtype = db.Column(db.String(32,collation = 'utf8mb4_unicode_ci'))
	
	def __init__(self, word, wordtype):
		self.word = word
		self.wordtype = wordtype
		

class NormalWord(db.Model):
	__tablename__ = 'normalword'
	id = db.Column(db.Integer, primary_key = True)
	word = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'), unique=True)
	wordtype = db.Column(db.String(32,collation = 'utf8mb4_unicode_ci'))
	
	def __init__(self, word, wordtype):
		self.word = word
		self.wordtype = wordtype

class NicknameWord(db.Model):
	__tablename__ = 'nicknameword'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'), unique=True)
	
	def __init__(self, name):
		self.name = name

class MaliciousComment(db.Model):
	__tablename__ = 'maliciouscomment'
	id = db.Column(db.Integer, primary_key = True)
	websitename = db.Column(db.String(32,collation = 'utf8mb4_unicode_ci'))
	commentNo = db.Column(db.Integer)
	count = db.Column(db.Integer)
	time = db.Column(db.DateTime, nullable=False)

	__table_args__ = (UniqueConstraint('websitename', 'commentNo', name='maliciouscomment_unique'),)
	
	def __init__(self, websitename, commentNo, count):
		self.websitename = websitename
		self.commentNo = commentNo
		self.count = count
		self.time = datetime.now()

class CelebrityName(db.Model):
	__tablename__ = 'celebrityname'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(128, collation = 'utf8mb4_unicode_ci'), unique=True)
	
	def __init__(self, name):
		self.name = name
