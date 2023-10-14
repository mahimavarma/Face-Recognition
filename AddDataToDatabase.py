import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("face recog vsc/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://face-attendance-491f4-default-rtdb.firebaseio.com/"
})

ref = db.reference('Doctors')
data = {
    "321654":
    {
        "name": "Mahima Varma",
        "major":"Orthopedic",
        "starting_year": 2020,
        "total-attendance": 7,
        "standing":"A+",
        "year": 12,
        "last_attendence": "2022-12-11 00:54:34"
    },
    "852741":
    {
        "name": "Emily Blunt",
        "major":"Theatre",
        "starting_year": 2000,
        "total-attendance": 40,
        "standing":"A+",
        "year": 1,
        "last_attendence": "2022-12-30 00:54:34"
    },
    "963852":
    {
        "name": "Elon Musk",
        "major":"Technology",
        "starting_year": 2017,
        "total-attendance": 32,
        "standing":"A+",
        "year": 2,
        "last_attendence": "2022-12-30 00:54:34"
    }
}

for key,value in data.items():
    ref.child(key).set(value)
