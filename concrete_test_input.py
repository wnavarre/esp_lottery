import os

context = {}

def set_context(prog):
    global context
    prog = str(prog)
    HERE = os.path.dirname(__file__)
    TEST_FOLDER = os.path.join(HERE, "test_input")
    students_path = os.path.join(TEST_FOLDER, prog + "_students.csv")
    sections_path = os.path.join(TEST_FOLDER, prog + "_sections.csv")
    context["sections"] = {}
    context["students"] = {}
    with open(sections_path, 'r') as f:
        for line in f:
            vals = line.split(",")
            vals = [val.strip() for val in vals]
            assert(len(vals) == 2)
            vals[1] = int(vals[1])
            context["sections"][vals[0]] = vals[1]
    with open(students_path, 'r') as f:
        for line in f:
            vals = line.split(",")
            vals = [val.strip() for val in vals]
            name = vals[0]
            prefs = []
            equal_mode = False
            rank = 0
            for val in vals[1:]:
                if val == "*":
                    equal_mode = True
                    continue
                if not equal_mode:
                    rank += 1
                equal_mode = False
                prefs.append((val, rank))
            context["students"][name] = dict(prefs)

def get_sections():
    global context
    return context['sections'].keys()

def get_students():
    global context
    return context['students'].keys()

def get_periods():
    return ["P1"]

def get_period(_):
    return "P1"

def section_cap(section_id):
    global context
    return context['sections'][section_id]

def is_equal(student_id, section_A, section_B):
    global context
    return (not
            (is_better(student_id, section_A, section_B)
            or
             is_better(student_id, section_B, section_A)
         )
        )

def get_ranked(pds, student_id):
    return context['students'][student_id].keys()

def is_better(student_id, section_A, section_B):
    if section_A is None:
        return False
    if section_B is None:
        return section_A in get_ranked(("P1",), student_id)
    if section_A not in get_ranked(("P1",), student_id):
        return False
    if section_B not in get_ranked(("P1",), student_id):
        return True
    array = context['students'][student_id]
    return array[section_A] < array[section_B]
