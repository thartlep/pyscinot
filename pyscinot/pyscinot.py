"""Main module."""

#-------------------------------------------------------------------------
def scientific_notation(number, **kwargs):
    """
    scientific_notation(number, LaTeX = False, significant_figures = None, suppress_extras = True, e_notation = False, upper_case = True)

    Format number(s) in scientific notation.

    Parameters
    ----------
    number : number or iterable of numbers
        Value(s) to be formatted.
    LaTeX : bool, optional
        If False (default), numbers are formatted in plain text. Otherwise, LaTeX math format is used.
    significant_figures : None or integer, optional
        If None (default), all digits are printed. Otherwise, number(s) are formatted with specified number of significant figures.
    suppress_extras : bool, optional
        If True (default), unnecessary zeros are suppressed, and a mantissa of 1 would also be suppressed.
    e_notation: bool, optional
        If False (default), the format is {mantissa}\\times10^{exponent} (for LaTeX math) or {mantissa}x10^{exponent}(for plain text). Otherwise, the format is {mantissa}E{exponent} (for upper_case=True) or {mantissa}e{exponent} (for uppercase=False).
    upper_case: bool, optional
        If True (default), an upper case "E" is used in e-notation. Otherwise, a lower case "e" is used.
    """
    return custom_notation(number, engineering_notation = False, **kwargs)

#-------------------------------------------------------------------------
def engineering_notation(number, **kwargs):
    """
    engineering_notation(number, LaTeX = False, significant_figures = None, suppress_extras = True, e_notation = False, upper_case = True)

    Format number(s) in engineering notation. Same as pyscinot.scientific_notation except that the exponent is limited to multiples of 3.

    Parameters
    ----------
    number : number or iterable of numbers
        Value(s) to be formatted.
    LaTeX : bool, optional
        If False (default), numbers are formatted in plain text. Otherwise, LaTeX math format is used.
    significant_figures : None or integer, optional
        If None (default), all digits are printed. Otherwise, number(s) are formatted with specified number of significant figures.
    suppress_extras : bool, optional
        If True (default), unnecessary zeros are suppressed, and a mantissa of 1 would also be suppressed.
    e_notation: bool, optional
        If False (default), the format is {mantissa}\\times10^{exponent} (for LaTeX math) or {mantissa}x10^{exponent}(for plain text). Otherwise, the format is {mantissa}E{exponent} (for upper_case=True) or {mantissa}e{exponent} (for uppercase=False).
    upper_case: bool, optional
        If True (default), an upper case "E" is used in e-notation. Otherwise, a lower case "e" is used.
    """
    return custom_notation(number, engineering_notation = True, **kwargs)

#-------------------------------------------------------------------------
def custom_notation(number, **kwargs):
    try:
        number_iterator = iter(number)
    except TypeError as te:
        return custom_notation_one(number, **kwargs)
    else:
        return_list = []
        for this_number in number:
            return_list.append(custom_notation_one(this_number, **kwargs))
        return return_list

#-------------------------------------------------------------------------
def custom_notation_one(number, engineering_notation = False, LaTeX = False, significant_figures = None, suppress_extras = True, e_notation = False, upper_case = True):

    from math import floor, ceil, log10

    exponent = int(floor(log10(number)))
    if engineering_notation:
        exponent = 3*int(floor(exponent/3.))
    mantissa = 10**(log10(number)-exponent)


    # Mantissa string
    if significant_figures is not None:
        significant_figures = max(0, significant_figures - ceil(log10(mantissa)))
        i = significant_figures
        if suppress_extras:
            for j in range(significant_figures, 0, -1):
                if round(mantissa,i) == round(mantissa,i-1):
                    i = j-1
        i = max(i,0)
        mantissa_string = '{:.{n_after}f}'.format(round(mantissa,i), n_after=i)
        suppress_mantissa_and_separator = (round(mantissa,i) == 1 and suppress_extras and not e_notation)
    else:
        mantissa_string = '{:g}'.format(mantissa)
        suppress_mantissa_and_separator = (mantissa == 1. and suppress_extras and not e_notation)

    # Separator string between mantissa and exponent
    if e_notation:
        if upper_case:
            separator_string = 'E'
        else:
            separator_string = 'e'
        base_string = ''
    else:
        if LaTeX:
            separator_string = r'$\times'
            base_string = r'10^'
        else:
            separator_string = 'x'
            base_string = '10^'

    # Exponent string
    if LaTeX and not e_notation:
        exponent_string = r'{{{:d}}}$'.format(exponent)
    else:
        exponent_string = '{:d}'.format(exponent)

    # Put all together and return
    return (not suppress_mantissa_and_separator)*(mantissa_string+separator_string)+suppress_mantissa_and_separator*(LaTeX and not e_notation)*'$'+base_string+exponent_string
