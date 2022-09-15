"""
Coefficients and functions involved in conversion and casting are 
constructed in Python code using strings read in from JSON files.
The Python built-in ``eval()`` function is used.
This function is a security risk, so it is configured here 
to remove access to any of the built-in Python functionality,
while at the same time loading local modules that contain 
useful data.
"""
import re

# Terms in JSON strings for numerical factors are converted to numbers using 
# `eval()`. By importing math_constants, we can include defined constants, like pi.
# Similarly, si_constants defines a number of useful values and ml_math defines
# mathematical operations.

from m_layer import si_constants
from m_layer import math_constants
from m_layer import ml_math 

ml_dict = dict(
    __builtins__= {},   # to improve security using eval
    si = si_constants,
    number = math_constants, 
    ml_math = ml_math 
)

# These all assume a trimmed string with no leading or trailing white space
# re_int = re.compile( r'^[+-]?[0-9]+$' )
# re_float = re.compile( r'^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$' )
re_int_ratio = re.compile( r'^([+-]?[0-9]+){1}/([0-9]+){1}$' )

# In a mixed ratio we accept powers of 10 in standard form (e.g., 1E9), but 
# they need special treatment
re_mixed_ratio = re.compile( 
    r'^'     
    r'1[eE][+]?\d{1,3}/([0-9]+)|'     
    r'1[eE][+]?\d{1,3}/1[eE][+]?\d{1,3}|'     
    r'([+-]?[0-9]+){1}/1[eE][+]?\d{1,3}'     
    r'$'
)

def ml_eval(txt,d={}):
    """
    Return a Python object evaluated from ``txt``
    
    """
    # Unfortunately, during the construction of a lambda function 
    # only global scope can be seen inside the function body.
    # So, if there are parameters to the function,
    # it is necessary to update the dictionary here each time. 
    if len(d):
        d.update(ml_dict)
    else:
        d = ml_dict
       

    # Regular expressions handle the various formats that `txt` may take:
    txt = txt.strip()
    
    token = re_int_ratio.search(txt)
    if token is not None:
        txt = "ml_math.Fraction( {} )".format( token.group() )
        
    else:         
        token = re_mixed_ratio.search(txt)
        if token is not None:
            num, den = token.group().split('/')
            txt = "ml_math.Fraction( {}, {} )".format( int(float(num)), int(float(den)) )      
     
    return eval(txt,d)
