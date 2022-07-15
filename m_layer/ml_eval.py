"""
Coefficients and functions involved in conversion and casting are 
constructed in Python code using strings read in from JSON files.
The Python built-in ``eval()`` function is used.
This function is a security risk, so it is configured here 
to remove access to any of the built-in Python functionality,
while at the same time loading local modules that contain 
useful data.
"""
# Terms in JSON strings for numerical factors are converted to numbers using 
# `eval()`. By importing math_constants, we can include defined constants, like pi.
# Similarly, si_constants defines a number of useful values and ml_math defines
# mathematical operations that can be actioned.

from m_layer import si_constants
from m_layer import math_constants
from m_layer import ml_math 

ml_dict = dict(
    __builtins__= {},   # to improve security using eval
    si = si_constants,
    number = math_constants, 
    ml_math = ml_math 
)

def ml_eval(txt,d={}):
    """
    Return a Python object evaluated from ``txt``
    
    The global dictionary 
    """
    # Unfortunately, during the construction of a lambda function 
    # only global scope can be seen inside the function body.
    # So, if there are parameters to the function,
    # it is necessary to update the dictionary here each time. 
    if len(d):
        d.update(ml_dict)
    else:
        d = ml_dict
        
    return eval(txt,d)
