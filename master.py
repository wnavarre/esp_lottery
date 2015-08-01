import concrete
import student
import section

classes = {}
students = []

def run():
    def _load_classes():
        global classes
        for class_id in concrete.get_classes():
            cl = section.Section(class_id)
            classes[class_id] = cl

    def _load_students():
        global students
        for student_id in concrete.get_students():
            student = student.Student(student_id)
            students.append(student)

    _load_classes()
    _load_students()
    periods = [1, 2, 3, 4]

    for p in periods:
        for student in students:
            student.set_period(p)
        while True:
            for class_object in classes.values():
                class_object.clear_lottery()
            for student in students:
                student.enter_better_lotteries()
                entries = 0
                for class_object in classes.values():
                    entries += class_object.lotteries.size()
                    class_object.lottery.run()
            if entries == 0:
                break
            for student in students:
                student.choose_best_class()
    
