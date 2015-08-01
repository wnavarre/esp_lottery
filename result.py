import cycle

class Result():
    def __init__(self, classes, students):
        self.classes = classes
        self.students = students
        self.known_cycle = None

    def find_negative_cycle(self):
        self.known_cycle = graph.Graph(self).get_negative_cycle()
        return self.known_cycle

