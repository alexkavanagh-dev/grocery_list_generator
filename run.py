import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('grocery_list_generator')

ingredients = SHEET.worksheet('INGREDIENT')
quantities = SHEET.worksheet('QUANTITY')


def generate_dinners_string():
    """Get the names of dinners from the first row of the ingredients
    worksheet. Use a for loop to create a string for listing out the options
    to the user with a corrosponding number next to each dinner name.

    Returns:
        string. The result of combining the dinner names in the for loop.
    """

    dinner_names = ingredients.row_values(1)

    dinners_string = ""

    # Combine each entry in dinner_names with corrosponding number into string
    for i in range(len(dinner_names)):
        dinners_string += f"{i + 1} - {dinner_names[i]}\n"

    return dinners_string


def get_dinner_picks(dinners_string):
    """Print out the dinner options to the user and ask for input to
    select from the options listed. User input must be in CSV format.

    Args:
        dinners_string: string: The list of dinner options for the user.

    Returns:
        list. The result of converting the users input to int.
    """
    while True:
        print("Please use the corresponding numbers to select your dinners for"
              " the next 7 days.")
        print("Your input must be seven numbers seperated by commas.\n")
        print("Example input: 1,2,3,4,5,6,7\n")
        print(dinners_string)

        dinners_input = input('Enter selections here:')

        dinners_split = dinners_input.split(',')

        # calls validate_csv() to check if input is valid. If false is returned
        # input is not valid and the user is asked for input again. While loop
        # breaks when True is returned and input is valid.
        if validate_csv(dinners_split):
            print("\nInput is valid!\n")
            break

    dinners_int = [int(dinner) for dinner in dinners_split]

    return dinners_int


def validate_csv(csv_input):
    """Check that input is exactly 7 values, input is only numbers and
    input is in the range of available options. Appropriate ValueError
    will be raised if input does not meet these requirements.

    Args:
        csv_input: string: The input taken in from the user.

    Returns:
        boolean. The result of checking if the input is the correct format.

    Raises:
        ValueError, if input is more or less than 7 values or
                    if input is not a number
                    if input is not in the range of available options
    """
    print("\nValidating input...\n")
    try:
        # Check if input is exactly 7 values
        if len(csv_input) != 7:
            raise ValueError(
                f"You must enter only 7 choices, you entered {len(csv_input)}"
            )

        # Check if input is number and in acceptable range
        for value in csv_input:
            if int(value) < 1 or int(value) > len(ingredients.row_values(1)):
                raise ValueError(
                    f"Input must correspond with options listed, {value} is "
                    "not an option"
                )

    # Return False if ValueError is raised
    except ValueError as e:
        print(f"Input was not valid: {e}.\n Please try again.\n")
        return False

    return True


def calculate_shopping_list(dinner_picks):
    """Using the input from the user, calculate the needed ingredients and
    quantities of each dinner selected and create a dictionary to be printed.

    Args:
        dinner_picks: list: The input taken in from the user as int.

    Returns:
        string. The result of calculating the shopping list from the
        users selections.
    """
    shopping_list = dict()

    print("Calculating Shopping list...\n")

    # Loop through values from the user to get the ingredient and quantity data
    for dinner in dinner_picks:

        ing_data = ingredients.col_values(dinner)
        quan_data = quantities.col_values(dinner)

        # Pop the first value off to remove the name of the selected dinner
        ing_data.pop(0)
        quan_data.pop(0)

        # Zip the ingredient and quantity data into a dictionary
        recipe_dict = dict(zip(ing_data, quan_data))

        # Check if the ingredient is already in the shopping list and either
        # Add to the quantity value if already present or add as new ingredient
        for ing, quan in recipe_dict.items():
            if ing in shopping_list:
                shopping_list[ing] = shopping_list.get(ing) + int(quan)
            else:
                shopping_list[ing] = int(quan)

    return shopping_list


def print_shopping_list(shopping_list):
    """Prints out the calculated list of ingredients and quantities.

    Args:
        shopping_list: list: The caclulated ingredients and quantities
        for the dinners selected by the user.
    """
    print("Your shopping list will be printed below:\n")
    for x, y in shopping_list.items():
        print(x + " : " + str(y))


def main():
    """Run all program fuctions
    """
    print("Welcome to my shopping list generator!\n")
    dinners_string = generate_dinners_string()
    dinner_picks = get_dinner_picks(dinners_string)
    shopping_list = calculate_shopping_list(dinner_picks)
    print_shopping_list(shopping_list)


main()
