To make a test: 

  1. Make a file [test-name]_sections.csv and [test-name]_students.csv

  2. In the sections file, simply write a file whose lines are a pair "section_id,section_capacity".  No heading is needed.  
 
  3. In the students file, each line should be "student_name,first_choice,second_choice,..." etc
     (To indicate that there is a tie-- that a student prefers two classes equally, place a "*" as a class between them: "student_name,first_choice,*,tied_for_first,*,also_tied_for_first,second" etc). 

To use a test: 
  1. Edit master.py; find the call to "set_context".  Change the passed value to a string representing test-name.  
  2. Edit concrete.py; ensure that it contains only the line "from concrete_test_input import *"
  3. Run master.py (e.g., master.py). 

Outputs: 
  1. Several iterations of the lottery. "BEFORE CYCLING" section is output of a naive lottery. "AFTER CYCLING" section is the output of the same lottery after removing cycles.
