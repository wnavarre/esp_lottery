import arbitrage.arbitrage as arbitrage
import tools
import random

class Graph():
    def __init__(self, students, sections):
        self.students = students
        self.sections = sections
        self.graph_dict = {}
        self.graph = self.graph_dict
        graph = self.graph_dict
        graph_dict = self.graph_dict
        _section_to_id = lambda x: x.s_id if x is not None else None
        for student in students:
            student_section = student.get_current_period().section
            if _section_to_id(student_section) not in graph_dict:
                graph_dict[_section_to_id(student_section)] = {}
            for class_id in student.equals():
                graph_dict[_section_to_id(student_section)][class_id] = 0
                if class_id not in graph_dict:
                    graph_dict[class_id] = {}
        for student in students:
            student_section = student.get_current_period().section
            if _section_to_id(student_section) not in graph_dict:
                graph_dict[_section_to_id(student_section)] = {}
            for class_id in student.better():
                graph_dict[_section_to_id(student_section)][class_id] = -1
                if class_id not in graph_dict:
                    graph_dict[class_id] = {}
        for cl in sections.values():
            if cl.space():
                if cl.s_id not in graph:
                    graph[cl.s_id] = {}
                graph[cl.s_id][None] = 0

    def get_negative_cycle(self):
        return arbitrage.find_cycle(self.graph)

    def make_shift(self, src, dst, wants, woulds, number):
        print "MOVING STUDENTS#############"
        print "SRC", src
        print "DST", dst
        random.shuffle(wants)
        random.shuffle(woulds)

        src_ob = self.sections[src]
        dst_ob = self.sections[dst]
        print "WANTS", [x.student_id for x in wants]
        print "WOULDS", [x.student_id for x in woulds]
        wants_number = min(len(wants), number)
        woulds_number = max(number - wants_number, 0)
        assert(woulds_number <= len(woulds))

        # Note that will might be a list of None's.
        will = wants[0:wants_number] + woulds[0:woulds_number]
        for student in will:
            print student.student_id
            if student is None:
                continue
            dst_ob.register(student, override=True)
            student.set_class(self.sections[dst])
            src_ob.unregister(student.student_id)

    def eliminate_cycle(self, cycle):
        moves = zip(cycle, tools.shifted_left(cycle[:-1]))
        wants = {} #Store ppl who want to move. 
        woulds = {} #Store ppl who wouldn't mind moving but not WANT. 
        for src, dst in moves:
            wants[(src, dst)] = self.sections[src].wants_moves(dst)
            woulds[(src, dst)] = self.sections[src].would_moves(dst)
        min_can = min(len(wants[i]) + len(woulds[i]) for i in moves)
        max_want = max(len(ls) for ls in wants.values())
        will = min(min_can, max_want)
        for src, dst in moves:
            self.make_shift(src, dst, wants[(src, dst)], woulds[(src, dst)], will)
