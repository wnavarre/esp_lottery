import master
import concrete
import tools

class Period():
    def __init__(self, period_id, student_id):
        self.student_id = student_id
        self.period_id = period_id
        self.section = None
        self.equals_cache = (float("nan"), None)
        better = concrete.get_ranked((period_id,), student_id)
        self.better = better
    def get_section_id(self):
        return (self.section.s_id if self.section else None)
    def get_better(self):
        f = lambda poss: concrete.is_better(self.student_id, poss, self.get_section_id())
        self.better = filter(f, self.better)
        return self.better
    def get_equals(self):
        section_id = self.get_section_id()
        if self.equals_cache[0] == section_id:
            return self.equals_cache[1]
        f = lambda poss: concrete.is_equal(self.student_id, poss, section_id)
        equals = filter(f, concrete.get_ranked((self.period_id,), self.student_id))
        try:
            equals.remove(section_id)
        except ValueError:
            if section_id is not None:
                raise
        self.equals_cache = (section_id, equals)
        return equals

class Student():
    def __init__(self, student_id, all_sections):
        self.all_sections = all_sections
        self.student_id = student_id
        self.periods = {}

    def get_current_period(self):
        return self.periods[self.period]

    def set_period(self, p_id):
        self.period = p_id
        if p_id not in self.periods:
            self.periods[p_id] = Period(p_id, self.student_id)

    def set_class(self, cl):
        self.get_current_period().section = cl
 
    def get_class(self):
        return self.get_current_period().section

    def enter_better_lotteries(self):
        better = self.get_current_period().get_better()
        for c in better:
            class_object = self.all_sections[c]
            class_object.lottery.enter(self)

    def choose_best_class(self):
        def _did_win(c):
            class_object = self.all_sections[c]
            return class_object.lottery.is_winner(self)
        poss = filter(_did_win, self.get_current_period().better)
        if not len(poss) > 0:
            return
        if self.get_current_period().section:
            self.get_current_period().section.unregister(self.student_id)
            self.get_current_period().section = None
        student_id = self.student_id
        gt = lambda a, b: concrete.is_better(student_id, a, b)
        assert(len(poss) > 0)
        best = tools.max_with_gt(poss, gt)
        self.get_current_period().section = self.all_sections[best]
        self.all_sections[best].register(self)
    
    def better(self):
        #list of better classes

        period = self.get_current_period()
        return period.get_better()

    def equals(self): 
        #list of equally good classes
        period = self.get_current_period()
        return period.get_equals()
