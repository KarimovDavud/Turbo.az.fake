from __future__ import print_function



_value_list = [
    1000, 900, 500, 400,
    100, 90, 50, 40,
    10, 9, 5, 4,
    1
]
_symbol_list = [
    'M', 'CM', 'D', 'CD',
    'C', 'XC', 'L', 'XL',
    'X', 'IX', 'V', 'IV',
    'I'
]

def int_to_roman(num:int) -> str:
    """Converts num to uppercase roman numerals"""
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // _value_list[i]):
            roman_num += _symbol_list[i]
            num -= _value_list[i]
        i += 1
    return roman_num


roman_dict_upper = {
    'I': 1,    'V': 5,
    'X': 10,   'L': 50,
    'C': 100,  'D': 500,
    'M': 1000,
}
roman_dict_lower = {k.lower(): v for (k, v) in roman_dict_upper.items()}
roman_dict = {**roman_dict_upper, **roman_dict_lower}

def roman_to_int(string:str) -> int:
    """Converts ascii roman numerals (uppercase or lowercase) to the number they represent"""
    result = 0
    last = 0
    did_pair = False
    for char in string:
        current = roman_dict[char]
        result += current
        if last and current > last and not did_pair:
            result -= 2 * last
            did_pair = True
        else: did_pair = False
        last = current
    return result


if __name__ == '__main__':
    import random, sys
    test = (len(sys.argv) > 1 and int(sys.argv[1])) or random.randint(1, 10000)
    print(test)
    roman_test = int_to_roman(test)
    print(roman_test)
    unroman_test = roman_to_int(roman_test)
    print(unroman_test, unroman_test == test)