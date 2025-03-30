from models import ToDoModel

class ToDoService:
    def __init__(self):
        self.model = ToDoModel()

    def create(self, params):
        """Creates a new To-Do item"""
        return self.model.create(params)

    def update(self, item_id, params):
        """Updates an existing To-Do item"""
        return self.model.update(item_id, params)

    def delete(self, item_id):
        """Soft deletes a To-Do item"""
        return self.model.delete(item_id)

    def list(self):
        """Lists all non-deleted To-Do items"""
        return self.model.list_items()

    def get_by_id(self, item_id):
        """Retrieves a specific To-Do item by its ID"""
        return self.model.get_by_id(item_id)

