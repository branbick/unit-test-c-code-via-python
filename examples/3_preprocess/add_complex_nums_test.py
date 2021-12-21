# SCRIPT-SPECIFIC RESOURCES
# - subprocess — Subprocess management: https://docs.python.org/3/library/subprocess.html
# - GCC Option Summary: https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html

from subprocess import run, PIPE
from cffi import FFI  # load
from importlib import import_module  # load
from unittest import TestCase  # AddIntsTest

def preprocess(file):
    # TODO: Figure out what the '-' arg does
    return run(['gcc', '-E', '-P', '-'], input=file, stdout=PIPE, check=True,
               text=True).stdout

def load(file_name_no_ext):
    # Open the header (.h) and source (.c) files
    with open(f'{file_name_no_ext}.h') as header_file, \
         open(f'{file_name_no_ext}.c') as source_file:
        # Instantiate an FFI object
        ffibuilder = FFI()

        # Register all the user-defined types, variable and function
        # declarations, etc. Preprocess the header file first to "remove" the
        # #include statement which cdef can't handle.
        ffibuilder.cdef(preprocess(header_file.read()))

        # Register all the variable and function definitions, etc.
        module_name = f'{file_name_no_ext}_cffi'
        ffibuilder.set_source(module_name, source_file.read())

        # Build the registered C program
        ffibuilder.compile()

    # Import the module corresponding to the C program and return its lib
    # member. The latter's members are, effectively, the C functions.
    return import_module(module_name).lib


class AddComplexNumsTest(TestCase):

    def test_add_complex_nums(self):
        complex_sum = load('add_complex_nums').add_complex_nums([-1.0, 0.5], [3.0, -4.0])
        self.assertEqual(complex_sum.real, 2.0)
        self.assertEqual(complex_sum.imag, -3.5)
