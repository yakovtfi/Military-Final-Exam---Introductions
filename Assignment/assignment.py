from abc import ABC, abstractmethod


#פה אנחנו עישנו את המיון לפי מרחק שכל חייל גר מהבסיס
class Assignment(ABC):
    @abstractmethod
    def sort_soldiers(self,soldiers):
        pass

class DistanceBased(Assignment):
    def sort_soldiers(self, soldiers):
        return sorted(soldiers, key=lambda s: s.distance_from_base, reverse=True)


# עכשיו נילך לבנות בקובץ ניפרד את המערכת שמנהלת את כל הבסיס