from  models.Soldier import AssignmentStatus
from Assignment.assignment import DistanceBased


class BaseManager:
    def __init__(self, assignment=None, db_manager=None):
        self._dorms = []
        self._soldiers = {}
        self._waiting_list = []
        self._assignment = assignment or DistanceBased()
        self._db_manager = db_manager

    def add_dorm(self, dorm):
        self._dorms.append(dorm)
        if self._db_manager:
            self._db_manager.save_dorm(dorm)

    def get_dorms(self):
        return self._dorms

    def get_dorm_by_name(self, name):
        for dorm in self._dorms:
            if dorm.name == name:
                return dorm
        return None

    def set_assignment(self, strategy):
        self._assignment = strategy

    def assign_soldiers(self, soldiers):
        self.clear_all_assignments()

        sorted_soldiers = self._assignment.sort_soldiers(soldiers)

        for soldier in sorted_soldiers:
            self._soldiers[soldier.personal_id] = soldier

        for soldier in sorted_soldiers:
            assigned = False
            for dorm in self._dorms:
                for room in dorm.rooms:
                    if not room.is_full():
                        room.add_soldier(soldier)
                        soldier.assign_to_room(dorm.name, room.room_number)
                        assigned = True
                        break
                if assigned:
                    break

            if not assigned:
                self._waiting_list.append(soldier)

        if self._db_manager:
            self._db_manager.save_soldiers(self._soldiers.values())

    def clear_all_assignments(self):
        for dorm in self._dorms:
            dorm.clear_all_rooms()

        for soldier in self._soldiers.values():
            soldier.unassign()

        self._waiting_list.clear()

    def get_soldier_by_id(self, personal_id):
        return self._soldiers.get(personal_id)

    def get_all_soldiers(self):
        return list(self._soldiers.values())

    def get_assigned_soldiers(self):
        return [s for s in self._soldiers.values() if s.status == AssignmentStatus.ASSIGNED]

    def get_waiting_soldiers(self):
        sorted_waiting = self._assignment.sort_soldiers(self._waiting_list)
        return sorted_waiting

    def get_assignment_summary(self):
        assigned_count = len(self.get_assigned_soldiers())
        waiting_count = len(self._waiting_list)

        soldiers_info = []
        for soldier in self._soldiers.values():
            soldier_data = {
                "personal_id": soldier.personal_id,
                "first_name": soldier.first_name,
                "last_name": soldier.last_name,
                "assigned": soldier.status == AssignmentStatus.ASSIGNED
            }

            if soldier.status == AssignmentStatus.ASSIGNED:
                soldier_data["dorm"] = soldier.dorm_name
                soldier_data["room"] = soldier.room_number
            else:
                soldier_data["status"] = "waiting"

            soldiers_info.append(soldier_data)

        return {
            "summary": {
                "assigned": assigned_count,
                "waiting": waiting_count
            },
            "soldiers": soldiers_info
        }

    def get_space_report(self):
        report = []
        for dorm in self._dorms:
            full_rooms = len(dorm.get_full_rooms())
            partial_rooms = len(dorm.get_partial_rooms())
            empty_rooms = len(dorm.get_empty_rooms())

            report.append({
                "dorm": dorm.name,
                "full_rooms": full_rooms,
                "partial_rooms": partial_rooms,
                "empty_rooms": empty_rooms
            })

        return report

    def load_from_database(self):
        if not self._db_manager:
            return

        soldiers = self._db_manager.get_all_soldiers()

        self._soldiers.clear()
        self._waiting_list.clear()
        for dorm in self._dorms:
            dorm.clear_all_rooms()

        for soldier in soldiers:
            self._soldiers[soldier.personal_id] = soldier

            if soldier.status == AssignmentStatus.ASSIGNED:
                dorm = self.get_dorm_by_name(soldier.dorm_name)
                if dorm:
                    room = dorm.get_room(soldier.room_number)
                    if room:
                        room.add_soldier(soldier)
            else:
                self._waiting_list.append(soldier)
