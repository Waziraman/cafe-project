# Import the json module.
# A module is a file containing reusable Python code and functions.
# The json module lets Python read data from JSON files and write data to JSON files.
import json

# A variable stores a value that we can use later.
# These are constants by convention: their names are written in uppercase.
EXPENSES_FILE = "week-01/expenses.json"
APPROVAL_LIMIT = 25000


# A function is a reusable block of code that performs a specific task.
# load_expenses is the function name.
# path is a parameter: it receives the file path when the function is called.
def load_expenses(path):

    # open() opens a file so Python can read or write its contents.
    # path tells Python which file to open.
    # "r" means read mode: we only want to read the file.
    # It automatically closes the file after the indented block finishes,
    # even if an error occurs.
    with open(path, "r") as file:
        # json.load() reads JSON data from the opened file
        # and converts it into Python data.
        # A JSON array becomes a Python list.
        # JSON objects inside the array become Python dictionaries.
        expenses = json.load(file)

    # return sends the result back to the code that called this function.
    # The function returns the list of expense dictionaries.
    return expenses


# This function receives the list of expenses.
# It calculates how much was spent in each category.
def category_totals(expenses):

    # Create an empty dictionary.
    # A dictionary stores data as key-value pairs.
    # Here, the category name will be the key and its total will be the value.
    totals = {}

    # A for loop repeats a block of code for each item in a collection.
    # This loop visits every expense dictionary in the expenses list.
    for expense in expenses:
        # Access dictionary values using their keys.
        # expense["category"] gets the category name.
        # expense["amount"] gets the expense amount.
        category = expense["category"]
        amount = expense["amount"]

        # if checks whether a condition is true.
        # "not in" checks whether a key does not exist in the dictionary.
        #
        # If this category has not appeared before,
        # create it in the dictionary and set its starting total to zero.
        if category not in totals:
            totals[category] = 0

        # Add this expense amount to the category's existing total.
        # The += operator means:
        # totals[category] = totals[category] + amount
        totals[category] += amount

    # Return the completed dictionary of category totals.
    return totals


# This function receives a number and returns it as formatted text.
def format_rupees(amount):

    # An f-string is a formatted string.
    # The expression inside { } is evaluated and inserted into the string.
    #
    # :, is a format specifier that adds commas to a number.
    # Example: 184200 becomes "184,200".
    #
    # This function returns a string, not a numeric value.
    return f"{amount:,}"


# This function finds and returns the expense with the highest amount.
def largest_expense(expenses):

    # Start by assuming the first expense is the largest.
    # List indexing starts at zero, so expenses[0] means the first item.
    largest = expenses[0]

    # Visit each expense in the list.
    for expense in expenses:
        # Compare the current expense amount with the largest amount found so far.
        # > means "greater than".
        if expense["amount"] > largest["amount"]:
            # If the current expense is larger, update largest.
            largest = expense

    # Return the dictionary containing the largest expense.
    return largest


# This function returns a list of expenses above the approval limit.
def approval_expenses(expenses):

    # Start with an empty list.
    # We will add expenses that exceed the limit to this list.
    needs_approval = []

    # Check every expense.
    for expense in expenses:
        # > means strictly greater than.
        # An expense equal to Rs 25,000 is NOT included.
        if expense["amount"] > APPROVAL_LIMIT:
            # append() adds an item to the end of a list.
            needs_approval.append(expense)

    # Return the list of expenses that need approval.
    return needs_approval


# This function prepares and saves the summary report.
# It receives the original expenses list and category totals dictionary.
def save_summary(expenses, totals):

    # Create a dictionary containing the summary information.
    # These keys are required by the assignment.
    summary = {
        # len() returns the number of items in a list.
        "expense_count": len(expenses),
        # sum() adds the amounts from all expense dictionaries.
        # The expression inside sum() gets the amount from each expense.
        "total": sum(expense["amount"] for expense in expenses),
        # Store the category totals dictionary.
        "by_category": totals,
    }

    # Open the summary file in write mode.
    # "w" creates the file if it does not exist.
    # If it already exists, its previous contents are replaced.
    with open("week-01/summary.json", "w", encoding="utf-8") as file:
        # json.dump() converts Python data into JSON
        # and writes it directly into the opened file.
        #
        # indent=4 makes the JSON file easier for humans to read.
        json.dump(summary, file, indent=4)


# main() brings the steps together in the correct order.
def main():

    # Call load_expenses() and store its returned list in expenses.
    # The data comes from expenses.json, not from a list typed here.
    expenses = load_expenses(EXPENSES_FILE)

    # Call category_totals() to calculate totals for each category.
    totals = category_totals(expenses)

    # Calculate the total spent across all expenses.
    total = sum(expense["amount"] for expense in expenses)

    # Find the largest expense dictionary.
    largest = largest_expense(expenses)

    # Get the list of expenses that exceed the approval limit.
    approvals = approval_expenses(expenses)

    # print() displays text or values in the terminal.
    print("Cafe expense report")

    # len(expenses) counts the number of recorded expenses.
    print(f"Expenses recorded: {len(expenses)}")

    # Display the total using the formatting function.
    print(f"Total spent: Rs {format_rupees(total)}")

    # \n inserts a blank line before the category heading.
    print("\nBy category:")

    # .items() returns the key-value pairs from a dictionary.
    # Here, category is the key and amount is its value.
    for category, amount in totals.items():
        # <10 aligns the category text within a 10-character space.
        # >8 aligns the formatted amount to the right within 8 characters.
        # These formatting options make the report easier to read.
        print(f"  {category:<10} Rs {format_rupees(amount):>8}")

    # Display the name and amount of the largest expense.
    # largest["item"] accesses the expense name.
    # largest["amount"] accesses its amount.
    print(
        f"\nLargest expense: {largest['item']} (Rs {format_rupees(largest['amount'])})"
    )

    # Display the approval limit and the number of expenses above it.
    print(
        f"\nNeeds approval (over Rs {format_rupees(APPROVAL_LIMIT)}): {len(approvals)}"
    )

    # Display each expense that needs approval.
    for expense in approvals:
        print(f"  - {expense['item']}: Rs {format_rupees(expense['amount'])}")

    # Save the calculated summary to week-01/summary.json.
    save_summary(expenses, totals)


# __name__ is a special Python variable.
# When this file is run directly, Python sets __name__ to "__main__".
# This condition ensures main() runs when we execute this file.
# It prevents main() from running automatically if this file
# is imported into another Python program.
if __name__ == "__main__":
    main()
