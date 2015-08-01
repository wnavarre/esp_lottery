import master
import concrete

class Period():
    def __init__(self, period_id, student_id):
        self.student_id = student_id
        self.period_id = period_id
        self.section = None
        better = concrete.get_ranked((period_id,), student_id)
        correct_p = lambda c: c.p_id == self.p_id
        self.better = filter(correct_p, better)
        
    def get_better(self):
        f = lambda poss: concrete.is_better(self.s_id, poss, self.section.s_id)
        self.better = filter(f, self.better)
        return self.better

class Student():
    def __init__(self, student_id):
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
            class_object = master.get_class(c)
            class_object.lottery.enter(self)

    def choose_best_class(self):
        def _did_win(c):
            class_object = master.get_class(c)
            return class_object.lottery.is_winner(self)
        poss = filter(_did_win, self.lottery.better)
        if len(poss) > 0:
            self.get_current_period().section.unregister()
            self.get_current_period().section = None
        student_id = self.student_id
        gt = lambda a, b: concrete.is_better(student_id, a, b)
        best = max_with_gt(poss, gt)
        self.get_current_period().section = best
        master.get_class(best).register(self)
    
    def better(self):
        #list of better classes

        period = self.get_current_period()
        return period.get_better()

    def equals(self):
        #list of equally good classes

        period = self.get_current_period()
        return period.get_equals()
