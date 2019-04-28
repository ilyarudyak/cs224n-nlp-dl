def is_contain_digits_check(s):
    return any(char.isdigit() for char in s)


def is_contain_2_or_more_digits_check(s):
    return sum([char.isdigit() for char in s]) > 1


def is_camel_case_and_start_with_capital_check(s):
    sr = s[1:]
    return sr != sr.lower() and sr != sr.upper() and not s[0].islower()
