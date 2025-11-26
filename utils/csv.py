import csv
import io
from models.Soldier import Soldier, Gender

#פה ניקח את הקובץ csv שלנו ונבדוק רם המספר אישי מתחיל ב 8 נבדוק שיכות מגדרית וכו
class CSVParser:
    @staticmethod
    def validate_personal_id(personal_id):
        if not personal_id:
            return False
        if not personal_id.startswith('8'):
            return False
        if not personal_id.isdigit():
            return False
        return True

    @staticmethod
    def validate_gender(gender):
        gender_lower = gender.lower()
        if gender_lower in ['male']:
            return Gender.MALE
        elif gender_lower in ['female']:
            return Gender.FEMALE
        return None

    @staticmethod
    def validate_distance(distance):
        try:
            return float(distance)
        except ValueError:
            return None

    @staticmethod
    def parse_csv_file(file_content):
        soldiers = []
        errors = []

        text_content = file_content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(text_content))

        for row_num, row in enumerate(csv_reader, start=2):
            try:
                personal_id = row.get('personal_id', '').strip()
                first_name = row.get('first_name', '').strip()
                last_name = row.get('last_name', '').strip()
                gender_str = row.get('gender', '').strip()
                city = row.get('city', '').strip()
                distance_str = row.get('distance_from_base', '').strip()

                if not CSVParser.validate_personal_id(personal_id):
                    errors.append(f"Row {row_num}: Invalid personal_id '{personal_id}'")
                    continue

                gender = CSVParser.validate_gender(gender_str)
                if gender is None:
                    errors.append(f"Row {row_num}: Invalid gender '{gender_str}'")
                    continue

                distance = CSVParser.validate_distance(distance_str)
                if distance is None:
                    errors.append(f"Row {row_num}: Invalid distance '{distance_str}'")
                    continue

                if not first_name or not last_name or not city:
                    errors.append(f"Row {row_num}: Missing required fields")
                    continue

                soldier = Soldier(personal_id, first_name, last_name, gender, city, distance)
                soldiers.append(soldier)

            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
                continue

        return soldiers, errors
