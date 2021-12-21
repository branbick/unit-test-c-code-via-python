# SCRIPT-SPECIFIC RESOURCE: uuid — UUID objects according to RFC 4122: https://docs.python.org/3/library/uuid.html

from cffi import FFI  # load
from uuid import uuid4  # load
from importlib import import_module  # load
from unittest import TestCase  # AddIntsTest

def load(file_name_no_ext):
    # Open the header (.h) and source (.c) files
    with open(f'{file_name_no_ext}.h') as header_file, \
         open(f'{file_name_no_ext}.c') as source_file:
        # Instantiate an FFI object
        ffibuilder = FFI()

        # Register all the user-defined types, variable and function
        # declarations, etc.
        ffibuilder.cdef(header_file.read())

        # Register all the variable and function definitions, etc. Use a
        # random name to circumvent the issue of module caching since the C
        # program contains a global variable that needs to be reinitialized
        # at the start of each of the three tests.
        module_name = f'{file_name_no_ext}_{uuid4().hex}_cffi'
        ffibuilder.set_source(module_name, source_file.read())

        # Build the registered C program
        ffibuilder.compile()

    # Import the module corresponding to the C program and return its lib
    # member. The latter's members are, effectively, the C functions.
    return import_module(module_name).lib


class SumIntsTest(TestCase):

    def setUp(self):
        self.module_lib = load('sum_ints')

    def test_sum_ints_zero(self):
        self.assertEqual(self.module_lib.sum_ints(0), 0)

    def test_sum_ints_one(self):
        self.assertEqual(self.module_lib.sum_ints(1), 1)

    def test_sum_ints_two_then_four(self):
        self.assertEqual(self.module_lib.sum_ints(2), 2)
        self.assertEqual(self.module_lib.sum_ints(4), 2+4)
