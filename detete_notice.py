from yuezixi import db
from yuezixi.models import Make_match,Mked
from datetime import datetime,timedelta
from threading import Timer  
def delete_notice():
	now=datetime.now()
	time=now - timedelta(days=1)
	notices=Make_match.query.filter(Make_match.End_time<time).all()
	for notice in notices:
		mks=Mked.query.filter_by(Make_match=notice).all()
		for mk in mks:
			db.session.delete(mk)
			db.session.commit()
		db.session.delete(notice)
		db.session.commit()

while(1):
	Timer(24*60*60,delete_notice).start()
