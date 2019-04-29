# digits and punctuation
def is_contain_digits_check(s):
    return any(char.isdigit() for char in s)


def is_contain_2_or_more_digits_check(s):
    return sum([char.isdigit() for char in s]) > 1


def is_contain_dot_and_len2_check(s):
    return '.' in s and len(s) == 2


# case checks
def is_camel_case_check(s):
    return s != s.lower() and s != s.upper()


def is_only_first_letter_capitalized_check(s):
    if len(s) == 1:
        return s[0].isupper()
    else:
        return s[0].isupper() and s[1:].islower()


def is_all_caps_check(s):
    return s.isupper()


def is_lower_case_check(s):
    return s.islower()


# first and last characters
def is_end_with_vowel_check(s):
    return s[-1] in 'aeiou'


def is_end_in_the_list(n, ending_list, s):
    return len(s) > n and s[-n:] in ending_list





