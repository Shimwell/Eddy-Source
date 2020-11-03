#!/usr/bin/env python3
# Peter Evans
# Cerberus Nuclear Ltd

"""Eddy is a programme to convert the text-based output files from MCNP and SCALE to
a user-friendly HTML format.

Copyright (C) 2020  Cerberus Nuclear Ltd

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


This module is the entry point for Eddy, the MCNP and SCALE to HTML output converter.
If run as __main__, this script asks for an output file and scaling factor, 
determines whether it is an MCNP or SCALE case, and calls either mcnp.mcnp_converter.py 
or scale.scale_converter.py. 
Alternatively, main() can be called directly by another module and provided with the same two arguments.
"""

# Imports from standard library
import sys
import argparse
from tkinter import Tk, simpledialog
from tkinter.filedialog import askopenfilename
# Local imports
# none

if __name__ == "__main__":
    from scale import scale_converter
    from mcnp import mcnp_converter
else:
    from .scale import scale_converter
    from .mcnp import mcnp_converter


def check_if_crit(output_data):
    """Read through output data to check if case is crit or shielding

    Args:
        output_data (list): The text of the output file

    Returns:
        True if kcode found or False if not.

    """
    for line in output_data:
        if 'kcode' in line.lower():
            return True
    return False


def read_file(filename):
    """Read in the output file.

    Args:
        filename (str): The name (and location) of the .out file

    Returns:
        data (list): The lines from the output file
    """
    with open(filename, 'r') as file:
        data = file.readlines()
    return data


def get_args(filename=None, scaling_factor=None):
    """
    Get the args from argparse if they are sent by the command line,
    otherwise open GUI windows to select input file and scaling factor.
    Read in the output data from the mcnp output file.

    Args:
        filename (optional) (str or None): the file path (including the name) of the output file, may be None
        scaling_factor (optioonal) (float or None): the scaling factor to multiply results by, may be None

    Returns:
        filename (str): the file path (including the name) of the output file
        output_data (list): The contents of the output file
        scaling_factor (float): the scaling factor to multiply results by
        crit_case (bool): True if kcode case, otherwise False
    """
    parser = argparse.ArgumentParser(description='MCNP or SCALE output to HTML Converter')
    parser.add_argument("-o", "--file", help="MCNP or SCALE output file")
    parser.add_argument("-sf", "--scaling_factor", type=float, help="Scaling Factor")
    args = parser.parse_args()

    # Get filename (and path) of mcnp output
    if filename is None:            # if filename was not passed as an argument to main()...
        if args.file:               # check if filename was passed as a command line argument
            filename = args.file
        else:                       # open tkinter window for file selection
            Tk().withdraw()
            filename = askopenfilename(
                title="Select Output File",
                filetypes=(("output files", "*.out"), ("all files", "*.*"))
                )
            # check that a file was actually selected:
            assert len(filename) != 0, "No file was selected."
    output_data = read_file(filename)

    # Check if shielding or crit case
    crit_case = check_if_crit(output_data)

    # Ask for scaling factor for shielding cases
    if not crit_case:
        if scaling_factor is None:                          # check if scaling factor was passed as an argument to main()
            if args.scaling_factor:                         # check if scaling factor was passed as a command line argument 
                scaling_factor = args.scaling_factor
            else:                                           # open tkinter window to ask for scaling factor
                Tk().withdraw()
                scaling_factor = simpledialog.askfloat(
                title="Scaling Factor",
                prompt="Please enter a scaling factor to multiply your results by", initialvalue=1,
                )
    # set scaling factor to 1 for crit cases (this variable will not be used)
    else:
        scaling_factor = 1
    # type checking for scaling factor
    if type(scaling_factor) is not float:
        try:
            scaling_factor = float(scaling_factor)
        except ValueError:
            print("The scaling factor should be a floating-point (decimal) number")
            sys.exit()

    assert len(filename) != 0, "You did not select an output file."
    print(f"Output file: {filename}")
    return filename, output_data, scaling_factor, crit_case


def main(filename=None, scaling_factor=None):
    """Entry point to Eddy. Can take filename and scaling factor as arguments.
    Call get_args to find the filename & scaling factor if not provided, and also get the
    output data and determine whether it is a crit case.
    Call read_file() and determines whether it is an MCNP or SCALE case;
    call the relevant converter.

    Args:
        filename (optional) (str): the file path (including the name) of the output file
        scaling_factor (optional) (float): A number by which the results will be multiplied
    """
    filename, output_data, scaling_factor, crit_case = get_args(filename, scaling_factor)
    if 'SCALE' in output_data[2]:
        scale_converter.main(filename, scaling_factor)
    elif 'MCNP' in output_data[0]:
        mcnp_converter.main(filename, scaling_factor, crit_case)
    else:
        raise RuntimeError("This file doesn't seem to be an MCNP or SCALE output?")


if __name__ == "__main__":
    main()
