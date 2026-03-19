# checklist_override.py
from .checklist import PracticeChecklistService

class PracticeChecklistServiceOverride(PracticeChecklistService):
    def create(self, data: dict):
        # Llamamos al método original
        checklist = super().create(data)
        # Extendemos: por ejemplo, añadimos un campo extra para testing
        checklist["extra_field"] = "added_by_override"
        return checklist