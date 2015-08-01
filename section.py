import concrete
import random

class Lottery():
    def __init__(self, cap):
        assert(cap >= 0)
        self.cap = cap
        self.entries = []

    def can_enter(self):
        return self.cap > 0

    def run(self):
        random.shuffle(self.entries)
        assert(type(self.entries) == type([]))
        self.winners = self.entries[0:self.cap]

    def enter(self, student):
        assert(student not in self.entries)
        if self.can_enter():
            self.entries.append(student.student_id)

    def is_winner(self, student):
        return student.student_id in self.winners

    def size(self):
        return len(self.entries)

class Section():
    def __init__(self, s_id):
        self.s_id = s_id
        self.cap = concrete.section_cap(s_id)
        self.p_id = concrete.get_period(s_id)
        self.students = []

    def clear_lottery(self):
        self.lottery = Lottery(self.cap - len(self.students))

    def unregister(self, student_id):
        self.students.remove(student_id)

    def register(self, student):
        assert(student.student_id not in self.students)
        assert(self.lottery.is_winner(student))
        self.students.append(student.student_id)

    def would_leave_for(self, status):
        assert(status in ["want", "willing"])
        s_id = self.s_id
        if status == "want":
            _f = lambda x: s_id in master.get_student(x).better()
        if status == "willing":
            _f = lambda x: s_id in master.get_student(x).equals()
        return filter(_f, self.students)

    def space(self):
        return self.cap - len(self.students)
    def _moves(self, other, which):
        assert(which in ['wants', 'would'])
        _wants = lambda s: concrete.is_better(s, other, self.s_id)
        _would = lambda s: concrete.is_equal(s, other, self.s_id)
        if which == 'wants':
            _f = _wants
        elif which== 'would':
            _f = _would
        can_ids = filter(_f, self.students)
        _student_object = lambda s: master.get_student(s)
        return map(_student_object, can_ids)

    def wants_moves(self, other):
        if other is None:
            return []
        return self._moves(other, 'wants')

    def would_moves(self, other):
        if other is None:
            return [None]*self.space()
        return self._moves(other, 'would')
