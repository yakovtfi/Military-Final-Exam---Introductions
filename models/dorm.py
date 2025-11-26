from models.room import Room

#יצירת מחלקת מעונות שבא יש את השם ואת מספר החדרים שקיים
class Dorm:
    def __init__(self, name, num_rooms=10):
        self._name = name
        self._rooms = [Room(i + 1) for i in range(num_rooms)]

    @property
    def name(self):
        return self._name

    @property
    def rooms(self):
        return self._rooms
#בפונקציות שבניתי נקבל את כל החדרים כמה מאוכלסים כמה פנוים וכו
    def get_room(self, room_number):
        if 1 <= room_number <= len(self._rooms):
            return self._rooms[room_number - 1]
        return None

    def total_capacity(self):
        return sum(room.capacity for room in self._rooms)

    def occupied_slots(self):
        return sum(len(room.soldiers) for room in self._rooms)

    def available_slots(self):
        return self.total_capacity() - self.occupied_slots()

    def get_full_rooms(self):
        return [room for room in self._rooms if room.is_full()]

    def get_partial_rooms(self):
        return [room for room in self._rooms if room.is_partial()]

    def get_empty_rooms(self):
        return [room for room in self._rooms if room.is_empty()]

    def clear_all_rooms(self):
        for room in self._rooms:
            room.clear()
