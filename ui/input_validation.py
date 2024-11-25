def get_integer(prompt="Please enter a whole number: ", ge=None, le=None, gt=None, lt=None):
    """
    Function to prompt for and return a valid integer.
    :param le:
    :param gt:
    :param errStr:
    :param lt:
    :param ge:
    :param prompt: string Optional string to use as prompt
    :return: val, integer Valid integer
    """
    val = 0
    while True:
        try:
            val = int(input(prompt))
            if lt is not None and val >= lt:
                print(F"Value must be less than {lt}!")
                continue
            if ge is not None and val < ge:
                print(F"Value must be greater than or equal to {ge}!")
                continue
            if gt is not None and val <= gt:
                print(F"Value must be greater than {gt}")
                continue
            if le is not None and val > le:
                print(F"Value must be less than or equal to {le}")
                continue
            return val
        except:
            print("Invalid, Please try again!")


def get_real(prompt="Please enter a decimal number: ", ge=None, le=None, gt=None, lt=None):
    """
    Function to prompt for and return a valid real number
    :param gt:
    :param le:
    :param errStr:
    :param lt:
    :param ge:
    :param prompt: string Optional string to use as prompt
    :return: num, float Valid real number
    """
    num = 0.0
    while True:
        try:
            num = float(input(prompt))
            if lt is not None and num >= lt:
                print(F"Value must be less than {lt}!")
                continue
            if ge is not None and num < ge:
                print(F"Value must be greater than or equal to {ge}!")
                continue
            if gt is not None and num <= gt:
                print(F"Value must be greater than {gt}!")
                continue
            if le is not None and num > le:
                print(F"Value must be less than or equal to {le}!")
                continue
            return num
        except:
            print("Invalid, please try again!")


def input_string(prompt="Enter a string:", error="Try again please, incorrect", valid=None):
    """
    Function to prompt for and return a string of characters.
    An empty string is invalid input.
    :param error:
    :param valid: valid function as param
    :param prompt: string Optional string to use as prompt
    :return: string Non-empty string of characters
    """

    while True:
        answer = input(prompt)
        if answer != " ":
            return answer
        else:
            print(error)


def y_or_n(prompt="Please enter 'y' or 'n':"):
    """
    Function to prompt for and return 'y' or 'n'.
    'Y', 'N', and all cases of 'yes' and 'no' are accepted.
    :param prompt: string Optional string to use as prompt
    :return: string Non-empty string of characters
    """
    answer = ""
    answer = input(prompt)
    answer = answer.lower()

    while answer != "n" and answer != "y" and answer != "no" and answer != "yes":
        print("Invalid response provided. Please try again!.")
        answer = input(prompt)
        answer = answer.lower()

    return answer


def select_item(prompt="Select desired item:", errStr="Error,Try again please!!", items="None", mapping=None):
    """
    Function to that allows user to select items from a list,
    or an optional dictionary if desired.
    :param items:
    :param mapping:
    :param errStr:
    :param prompt: string
    :return: string Non-empty string of characters
    """
    new_dictionary = {}
    if mapping is not None:
        for key in mapping:
            new_dictionary[key.lower()] = mapping[key]
            # print(mapping[key])
    for item in items:
        new_dictionary[item.lower()] = item
        # print(item)
    while True:
        user_input = input(prompt)
        user_input = user_input.lower()
        if user_input in new_dictionary:
            return new_dictionary[user_input]
        else:
            print(errStr)
