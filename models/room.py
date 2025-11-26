
#יצירת מחלקת חדר שבא ניקח את מספר החדר ואת הקיבולת של החדר
class Room:
    def __init__(self, room_number, capacity=8):
        self._room_number = room_number
        self._capacity = capacity
        self._soldiers = []


    @property
    def room_number(self):
        return self._room_number

    @property
    def capacity(self):
        return self._capacity

    @property
    def soldiers(self):
        return self._soldiers

#פה בניתי פונקציות שבודקות את מצב החדר האם הוא מלא או רק האם יש עוד מקומות באותו חדר להוסיף חייל וכו
    def is_full(self):
        return len(self._soldiers) >= self._capacity

    def is_empty(self):
        return len(self._soldiers) == 0

    def is_partial(self):
        return 0 < len(self._soldiers) < self._capacity

    def available_slots(self):
        return self._capacity - len(self._soldiers)

    def add_soldier(self, soldier):
        if self.is_full():
            return False
        self._soldiers.append(soldier)
        return True

    def remove_soldier(self, soldier):
        if soldier in self._soldiers:
            self._soldiers.remove(soldier)
            return True
        return False

    def clear(self):
        self._soldiers.clear()
