#mongodb database of user info
class User(db.Document):
	name = db.StringField(max_length=255, required=True)
	idNumber = db.StringField(max_length=255, required=True)

user1 = User(name="Lili Borland", idNumber="03171993")
user1.save()

#confirm documents exist in the test data collection
db.user1.find({name:"Lili Borland"})