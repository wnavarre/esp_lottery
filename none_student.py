import class

class NoneClass():
    def __init__(self):
        self.s_id = None
        self.cap = float("inf")

    def wants_moves(self, other):
        _no_class = lambda s: s.get_class() is None
        no_class = filter(_no_class, master.get_students())
        _wants_class = lambda s: other in s.better()
        return filter(_wants_class, no_class)

    def would_moves(self, other):
        return []
