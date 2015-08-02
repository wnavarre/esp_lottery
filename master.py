import concrete
import student
import section
import time

def run():
    sections = {}
    students = []
    periods = []
    concrete.set_context(120)
    def _load_classes():
        all_section_ids = concrete.get_sections()
        for class_id in all_section_ids:
            cl = section.Section(class_id)
            sections[class_id] = cl
    def _load_students():
        for student_id in concrete.get_students():
            _student = student.Student(student_id, sections)
            students.append(_student)

    _load_classes()
    _load_students()
    periods = concrete.get_periods()

    for p in periods:
        start = time.clock()
        for _student in students:
            _student.set_period(p)
        stop = time.clock()
        total_time_period_setting += stop - start
        while True:
            for class_object in sections.values():
                class_object.clear_lottery()
            for _student in students:
                _student.enter_better_lotteries()
                entries = 0
            for class_object in sections.values():
                entries += class_object.lottery.size()
                class_object.lottery.run()
            if entries == 0:
                break
            for _student in students:
                _student.choose_best_class()

    for code, obj in sections.items():
        print code, "################################################"
       import concrete
import student
import section
import time


if __name__ == '__main__':
    for i in range(1):
        run()
