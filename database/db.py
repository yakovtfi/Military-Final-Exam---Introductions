import sqlite3
from models.Soldier import Soldier, Gender

#פה יצרתי את מנהל הדאטה שבא נעשה את כל החיבורים ניצור רת כל הטבלאות של מעונות חיילים וכו וגם נכניס לתוכן (לכל טבלה) את הדברים שאם קשורים אליהם
class DatabaseManager:
    def __init__(self, db_path='base.db'):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

    def close(self):
        if self.connection:
            self.connection.close()

    def initialize_schema(self):
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS soldiers (
                personal_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                city TEXT NOT NULL,
                distance_from_base REAL NOT NULL,
                status TEXT NOT NULL,
                dorm_name TEXT,
                room_number INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dorms (
                name TEXT PRIMARY KEY,
                num_rooms INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                dorm_name TEXT NOT NULL,
                room_number INTEGER NOT NULL,
                capacity INTEGER NOT NULL,
                PRIMARY KEY (dorm_name, room_number),
                FOREIGN KEY (dorm_name) REFERENCES dorms(name)
            )
        ''')

        self.connection.commit()

    def save_soldier(self, soldier):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO soldiers 
            (personal_id, first_name, last_name, gender, city, distance_from_base, status, dorm_name, room_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            soldier.personal_id,
            soldier.first_name,
            soldier.last_name,
            soldier.gender.value,
            soldier.city,
            soldier.distance_from_base,
            soldier.status.value,
            soldier.dorm_name,
            soldier.room_number
        ))
        self.connection.commit()

    def save_soldiers(self, soldiers):
        for soldier in soldiers:
            self.save_soldier(soldier)

    def get_all_soldiers(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM soldiers')
        rows = cursor.fetchall()

        soldiers = []
        for row in rows:
            gender = Gender.MALE if row['gender'] == 'male' else Gender.FEMALE
            soldier = Soldier(
                row['personal_id'],
                row['first_name'],
                row['last_name'],
                gender,
                row['city'],
                row['distance_from_base']
            )

            if row['status'] == 'assigned':
                soldier.assign_to_room(row['dorm_name'], row['room_number'])

            soldiers.append(soldier)

        return soldiers

    def get_soldier_by_id(self, personal_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM soldiers WHERE personal_id = ?', (personal_id,))
        row = cursor.fetchone()

        if not row:
            return None

        gender = Gender.MALE if row['gender'] == 'male' else Gender.FEMALE
        soldier = Soldier(
            row['personal_id'],
            row['first_name'],
            row['last_name'],
            gender,
            row['city'],
            row['distance_from_base']
        )

        if row['status'] == 'assigned':
            soldier.assign_to_room(row['dorm_name'], row['room_number'])

        return soldier

    def save_dorm(self, dorm):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO dorms (name, num_rooms)
            VALUES (?, ?)
        ''', (dorm.name, len(dorm.rooms)))

        for room in dorm.rooms:
            cursor.execute('''
                INSERT OR REPLACE INTO rooms (dorm_name, room_number, capacity)
                VALUES (?, ?, ?)
            ''', (dorm.name, room.room_number, room.capacity))

        self.connection.commit()

    def clear_soldiers(self):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM soldiers')
        self.connection.commit()

    def clear_all(self):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM soldiers')
        cursor.execute('DELETE FROM rooms')
        cursor.execute('DELETE FROM dorms')
        self.connection.commit()
