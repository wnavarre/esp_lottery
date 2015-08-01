import arbitrage.arbitrage as arbitrage
import tools
import random

class Graph():
    def __init__(self, result):
        graph_dict = {}
        for student in result.students.values():
            student_section = student.get_current_period().section
            if student_section not in graph_dict:
                graph_dict[student_section] = {}
            for class_id in student.equals():
                graph_dict[student_section][class_id] = 0
        for student in result.students.values():
            student_section = student.get_current_period().section
            if student_section not in graph_dict:
                graph_dict[student_section] = {}
            for class_id in student.better():
                graph_dict[student_section][class_id] = -1
        for cl in master.get_classes():
            if cl.space():
                if cl.s_id not in graph:
                    graph[cl.s_id] = {}
                graph[cl.s_id][None] = 0

    def get_negative_cycle(self):
        return arbitrage.find_negative_weight_cycle(self.graph)

def make_shift(src, dest, wants, woulds, number):
    random.shuffle(wants)
    random.shuffle(woulds)

    src_ob = master.get_class(src)
    dst_ob = master.get_class(dst)
    
    wants_number = min(len(wants), number)
    woulds_number = max(number - wants_number, 0)
    assert(woulds_number <= len(woulds))

    # Note that will might be a list of None's.  
    will = wants[0:wants_number] + woulds[0:woulds_number]
    for student in will:
        if student is None:
            continue
        dst_ob.register(student)
        student.set_class(dst)
        src_ob.unregister(student)


def eliminate_cycle(result, cycle):
    moves = zip(cycle, shifted_left(cycle))
    wants = {} #Store ppl who want to move. 
    woulds = {} #Store ppl who wouldn't mind moving but not WANT. 
    for src, dst in moves:
        wants[(src, dst)] = master.get_class(src).wants_moves(dst)
        woulds[(src, dst)] = master.get_class(src).would_moves(dst)
    min_can = min(len(wants[i]) + len(woulds[i]) for i in moves)
    max_want = max(len(wants.values()))
    will = min(min_can, max_want)
    for src, dst in moves:
        make_shift(src, dest, wants, would, number)
