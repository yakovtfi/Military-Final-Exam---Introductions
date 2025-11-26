from enum import Enum


# יצירת מחלקת שיכות מגדרית
class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

#יצירת מחלקת שבודקת אם יש לחייל חדר כבר או שהוא ממתין
class AssignmentStatus(Enum):
    ASSIGNED = "assigned"
    WAITING = "waiting"


#יצירת מחלקת חייל שבאא נעשה את כל הדברים שקשורים לחייל פרטיים אישים וכו
class Soldier:
    def __init__(self, personal_id, first_name, last_name, gender, city, distance_from_base):
        self._personal_id = personal_id
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._city = city
        self._distance_from_base = distance_from_base
        self._status = AssignmentStatus.WAITING
        self._dorm_name = None
        self._room_number = None


    @property
    def personal_id(self):
        return self._personal_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def gender(self):
        return self._gender

    @property
    def city(self):
        return self._city

    @property
    def distance_from_base(self):
        return self._distance_from_base

    @property
    def status(self):
        return self._status
    
    @property
    def dorm_name(self):
        return self._dorm_name
    
    @property
    def room_number(self):
        return self._room_number

    def assign_to_room(self, dorm_name, room_number):
        self._status = AssignmentStatus.ASSIGNED
        self._dorm_name = dorm_name
        self._room_number = room_number

    def unassign(self):
        self._status = AssignmentStatus.WAITING
        self._dorm_name = None
        self._room_number = None

    def to_dict(self):
        return {
            "personal_id": self._personal_id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "gender": self._gender.value,
            "city": self._city,
            "distance_from_base": self._distance_from_base,
            "status": self._status.value,
            "dorm_name": self._dorm_name,
            "room_number": self._room_number
        }








