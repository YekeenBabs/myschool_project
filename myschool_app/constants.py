# constants.py
from typing import List, Tuple

GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
BLOOD_GROUP_CHOICES = [('B+', 'B+'), ('A+', 'A+'), ('O+', 'O+')]
STUDENT_CLASS_CHOICES = [('J.S.S. 1', 'J.S.S. 1'), ('J.S.S. 2', 'J.S.S. 2'), ('J.S.S. 3', 'J.S.S. 3'),
                         ('S.S.S. 1', 'S.S.S. 1'), ('S.S.S. 2', 'S.S.S. 2'), ('S.S.S. 3', 'S.S.S. 3')]
SECTION_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]
DEPARTMENT_CHOICES: list[tuple[str, str]] = [('Art', 'Art'), ('Commercial', 'Commercial'), ('Science', 'Science'),
                                             ('dept1', 'Department 1'),
                                             ('dept2', 'Department 2'), ]
