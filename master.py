import concrete
import student
import section

classes = {}
students = []
concrete.set_context(120)
def run():
    def _load_classes():
        global classes
        for class_id in concrete.get_sections():
            cl = section.Section(class_id)
            classes[class_id] = cl

    def _load_students():
        global students
        for student_id in concrete.get_students():
            _student = student.Student(student_id)
            students.append(_student)

    _load_classes()
    _load_students()
    periods = [1, 2, 3, 4]

    for p in periods:
        for _student in students:
            _student.set_period(p)
        while True:
            for class_object in classes.values():
                class_object.clear_lottery()
            for _student in students:
                _student.enter_better_lotteries()
                entries = 0
                for class_object in classes.values():
                    entries += class_object.lottery.size()
                    class_object.lottery.run()
            if entries == 0:
                break
            for _student in students:
                _student.choose_best_class()

    for code, obj in classes.items():
        print code, "################################################"
        print obj.students

if __name__ == '__main__':
    run()
