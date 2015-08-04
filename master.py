import concrete
import student
import section
import time
import cycle
import random

def run():
    sections = {}
    students = []
    students_dict = {}
    periods = []
    concrete.set_context(120)
    def _load_classes():
        all_section_ids = concrete.get_sections()
        for class_id in all_section_ids:
            cl = section.Section(class_id, students_dict)
            sections[class_id] = cl
    def _load_students():
        for student_id in concrete.get_students():
            _student = student.Student(student_id, sections)
            students.append(_student)
            students_dict[student_id] = _student
    _load_classes()
    _load_students()
    periods = concrete.get_periods()

    for p in periods:
        for _student in students:
            _student.set_period(p)
        while True:
            for class_object in sections.values():
                class_object.clear_lottery()
            for _student in students:
                # Enter lotteries for all sections they'd
                # prefer over their currently-assigned section AND
                # has space.  (LIMITED TO SPECIFIED PERIOD!)
                _student.enter_better_lotteries()
                entries = 0
            for class_object in sections.values():
                # Count how many students actually entered
                # the lotteries, and run each lottery.
                entries += class_object.lottery.size()
                class_object.lottery.run()
            if entries == 0:
                # If nobody entered a lottery, we are done.
                break
            for _student in students:
                # Students choose the best class
                # among those whose lotteries they won.
                _student.choose_best_class()
    while True:
        print "Preparing to find cycle"
        graph = cycle.Graph(students, sections)
        print "Finding cycle..."
        neg_cycle = graph.get_negative_cycle()
        if not neg_cycle:
            break;
        print "Eliminating cycle..."
        graph.eliminate_cycle(neg_cycle)
    return graph.graph

if __name__ == '__main__':
    count = 0
    for i in range(20):
        out = run()
        print out
