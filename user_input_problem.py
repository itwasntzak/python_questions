def user_input(prompt, before=None):
    '''
    prompt is displayed to user before they input anything, must be a string
    before is on the same line before the users input, must be a string
    '''
    # not unit testible, requires user input
    print(prompt, end='')
    if before:
        return input(before)
    return input()
    

def check_text(user_input, spaces=False, symbols=None):
    '''
    symbols needs to be a string of characters to allow the user to enter
    '''
    if symbols and not isinstance(symbols, str):
        raise TypeError

    import re

    if spaces is True and symbols:
        pattern = r'^[a-zA-Z ' + symbols + ']$'
    elif symbols:
        pattern = r'^[a-zA-Z' + symbols + ']$'
    elif spaces is True:
        pattern = r'^[a-zA-Z ]$'
    else:
        pattern = r'^[a-zA-Z]$'

    for character in user_input:
        if not re.match(pattern, character):
            return False

    return True


def input_text(prompt, spaces=False, symbols=None):
    if symbols and not isinstance(symbols, str):
        raise TypeError

    error_message = '\nError, please enter alpha characters'
    if spaces is True and symbols:
        error_message += f', spaces, or these {symbols}'
    elif spaces is True:
        error_message += ' or spaces'
    elif symbols:
        error_message += f' or these {symbols}'

    text = user_input(prompt)
    while not check_text(text, spaces, symbols):
        print(error_message)
        text = user_input(prompt)
    
    return text


def check_confirm(user_input):
    '''
    checks that the user has input y or n to confirm different things
    '''
    if not isinstance(user_input, str):
        raise TypeError(f'user_input needs to be a string not {type(user_input)}')

    import re
    if re.match('^[y]$', user_input, flags=re.IGNORECASE):
        return True
    elif re.match('^[n]$', user_input, flags=re.IGNORECASE):
        return False


def confirm(data_string):
    import re
    from resources.strings import confirm_text
    from utility.utility import add_newlines

    prompt = add_newlines(data_string) + confirm_text
    prompt = add_newlines(prompt)

    user_choice = user_input(prompt)
    while not re.match('^[yn]$', user_choice, flags=re.IGNORECASE):
        print('\nError, please enter Y for yes or N for no')
        user_choice = user_input(prompt)

    return check_confirm(user_choice)


class User_Input():
    def __init__(self, prompt):
        self.prompt = prompt

    def location(self):
        location = input_text(self.prompt, spaces=True, symbols=',./&?!:;()[]-+%')
        while not confirm(location):
            location = input_text(self.prompt, spaces=True, symbols=',./&?!:;()[]-+%')

        return location


# unittests
import unittest

class Test_User_Input(unittest.TestCase):
    def test_check_confirm(self):
        from utility.user_input import check_confirm

        # true
        self.assertTrue(check_confirm('y'))
        self.assertTrue(check_confirm('Y'))
        # false
        self.assertFalse(check_confirm('n'))
        self.assertFalse(check_confirm('N'))
        # raise errors
        with self.assertRaises(TypeError):
            check_confirm(1.5)
            check_confirm(7)
            check_confirm([x for x in range(5)])
            check_confirm(None)

    def test_check_text(self):
        from utility.user_input import check_text

        # true
        self.assertTrue(check_text('hello'))
        self.assertTrue(check_text('hello world', spaces=True))
        self.assertTrue(check_text('hello, world/earth & mars', spaces=True, symbols=',&/'))

        # false
        self.assertFalse(check_text('hello world'))
        self.assertFalse(check_text('hello, world/earth & mars'))
