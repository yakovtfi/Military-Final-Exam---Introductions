from flask import Flask,request,jsonify
from models.dorm import Dorm
from utils.csv import CSVParser
from base_manager.base_manager import BaseManager
from database.db import DatabaseManager


app = Flask(__name__)

db_manager = DatabaseManager()
db_manager.connect()
base_manager = BaseManager(db_manager=db_manager)


#ניתוח טבלאות ונבדוק את התקינות שלהם
@app.route('/initializeScheme', methods=['POST'])
def initialize_scheme():
    try:
        db_manager.clear_all()
        db_manager.initialize_schema()

        base_manager.add_dorm(Dorm("Dorm A"))
        base_manager.add_dorm(Dorm("Dorm B"))

        return jsonify({"message": "Database schema initialized successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#פה נבדוק אם הקבצים שלנו קימים אם לא נחזיר שגיאה בהתאם ואם כן נחזיר בסדר
@app.route('/assignWithCsv', methods=['POST'])
def assign_with_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File must be CSV"}), 400

    try:
        file_content = file.read()
        soldiers, errors = CSVParser.parse_csv_file(file_content)

        if not soldiers and errors:
            return jsonify({"error": "No valid soldiers found", "parse_errors": errors}), 400

        base_manager.assign_soldiers(soldiers)

        result = base_manager.get_assignment_summary()

        if errors:
            result["parse"] = errors

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#פה נחפש את החייל אם הוא קיים בקובץ לפי מספר אישי וכו
@app.route('/search', methods=['GET'])
def search_soldier():
    personal_id = request.args.get('personal_id')

    if not personal_id:
        return jsonify({"error": "personal_id parameter required"}), 400

    soldier = base_manager.get_soldier_by_id(personal_id)

    if not soldier:
        return jsonify({"error": "Soldier not found"}), 404

    result = {
        "personal_id": soldier.personal_id,
        "first_name": soldier.first_name,
        "last_name": soldier.last_name,
        "assigned": soldier.status.value == "assigned"
    }

    if soldier.status.value == "assigned":
        result["dorm"] = soldier.dorm_name
        result["room"] = soldier.room_number
    else:
        result["status"] = "waiting"

    return jsonify(result), 200

#פה נקבת את הדוח של תפוסת חדרים האם אם מלאים ריקים וכו
@app.route('/space', methods=['GET'])
def space_report():
    try:
        report = base_manager.get_space_report()
        return jsonify({"dorms": report}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#פה נקבל את דוח רשימת המתנה טנבדוק אלו חילים שובצו ואלו לא
@app.route('/waitingList', methods=['GET'])
def waiting_list():
    try:
        waiting_soldiers = base_manager.get_waiting_soldiers()
        
        soldiers_list = []
        for soldier in waiting_soldiers:
            soldiers_list.append({
                "personal_id": soldier.personal_id,
                "first_name": soldier.first_name,
                "last_name": soldier.last_name,
                "gender": soldier.gender.value,
                "city": soldier.city,
                "distance_from_base": soldier.distance_from_base
            })
        
        return jsonify({
            "count": len(soldiers_list),
            "soldiers": soldiers_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    try:
        db_manager.initialize_schema()

        if not base_manager.get_dorms():
            base_manager.add_dorm(Dorm("Dorm A"))
            base_manager.add_dorm(Dorm("Dorm B"))

        base_manager.load_from_database()

        app.run(debug=True, port=5000)
    finally:
        db_manager.close()
#לסיכום בניתי פה שרת שנותן ניתוח טבלאות אתחול טבלאות ובודקים את הקבצים אם הם csv אם הם קימים אם יש להם שם
# בניתי שרת שבודק את הדוח של החדרים מלאים או לא
#עוד אחד שבניתי בודק איזה חילים ממתנים ואלו לא
#וגם בנינו שרת שאפשר לחפש את החייל לפי המספר האישי שלו
#מקווה שהכל מובן

