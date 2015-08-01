import sys
sys.path.append("/home/devsite/esp")
sys.path.append("/home/devsite/esp/useful_scripts")
import esp
import script_setup

import os


from esp.program.controllers.lottery import LotteryAssignmentController
from esp.program.models import Program
context = {}

def set_context(program_id):
    global context
    context = {}
    prog = Program.objects.get(id=program_id)
    context['lac'] = LotteryAssignmentController(prog)

    # Make section tuples and put them in a dict.
    _st = lambda s: (s.emailcode(), s)
    sections = dict(map(_st, context['lac'].sections))
    context['sections'] = sections

def get_sections():
    global context
    return context['sections'].keys()

def get_students():
    global context
    lac = context['lac']
    return list(lac.student_ids)

def get_periods():
    global context
    _id = lambda t: t.id
    return map(_id, context['lac'].timeslots)

def get_period(section_id):
    global context
    sections = context['sections']
    section = sections[section_id]
    tbs = section.time_blocks()
    assert(len(list(tbs))==1)
    return tbs[0].id

def section_cap(section_id):
    global context
    section = context['sections'][section_id]
    return section.capacity

def is_equal(student_id, section_A, section_B):
    if section_A is None and section_B is None:
        return True
    if section_A is None or section_B is None:
        return False
    int_A = _get_student_interest(student_id, section_A)
    int_B = _get_student_interest(student_id, section_B)
    return int_A == int_B

def get_ranked(pds, student_id):    
    _btn = lambda c: is_better(student_id, c, None)
    out = filter(_btn, context['sections'].keys())
    if pds is not None:
        _pd_match = lambda c: get_period(c) in pds
        out = filter(_pd_match, all_ranked)
    return out

def is_better(student_id, section_A, section_B):
    if section_A is None:
        return False
    if section_B is None:
        interest_A = _get_student_interest(student_id, section_A)
        priority_A = _get_student_priority(student_id, section_A)
        return bool(interest_A or priority_A)

    priority_A = _get_student_priority(student_id, section_A)
    priority_B = _get_student_priority(student_id, section_B)
    if bool(priority_A) and bool(priority_B):
        return priority_A < priority_B
    elif bool(priority_A) or bool(priority_B):
        return bool(priority_A)
    
    interest_A = _get_student_interest(student_id, section_A)
    interest_B = _get_student_interest(student_id, section_B)
    if interest_A == interest_B:
        return False
    else:
        return interest_A

def _get_student_interest(student_id, class_id):
    global context
    sections = context['sections']
    lac = context['lac']
    stud_i = lac.student_indices[student_id]
    class_ob_id = sections[class_id].id
    cl_i = lac.section_indices[class_ob_id]
    assert cl_i >= 0, "Invalid class ID "+str(class_id) +", "+str(class_ob_id)
    assert stud_i >= 0, "Invalid student ID"
    array = lac.interest
    return array[stud_i, cl_i]

def _get_student_priority(student_id, class_id):
    global context
    sections = context['sections']
    lac = context['lac']
    stud_i = lac.student_indices[student_id]
    cl_i = lac.section_indices[sections[class_id].id]
    assert cl_i >= 0, "Invalid class ID"
    assert stud_i >= 0, "Invalid student ID"
    priority_arrays = lac.priority
    for i in range(len(priority_arrays)):
        array = priority_arrays[i]
        if array[stud_i, cl_i]:
            return i
    return False
