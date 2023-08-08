class RowManager:
    def __init__(self):
        self.index = 0
        self.row_number = 0

    def increment_index(self):
        if self.index > 4:
            self.row_number += 1
            self.index = 0 
            return True
        else:
            self.index += 1
            return False
