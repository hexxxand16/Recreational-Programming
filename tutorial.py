# This is a comment

# Python runs up to down, running each command one by one (except functions)

# This is a variable. You do NOT need to declare a type
a = 5

# This is a string. You can also use single quotes ''
b = "Hello World"

# This is the print function. This will output variables or text
print(b)  # Outputs "Hello World"
print("Who")  # Outputs "Who"

# This is a list. Unlike arrays, you can put anything in lists
c = ["Hi", 666, 3.141, 'a']

# This is the append function. It will add an item to the end of the list
c.append("Who's there")
print(c)

# This is the len function. It returns the length of an array
print(len(c))  # Outputs 5

# This is a for loop. The end of line must be a colon :
for i in range(3):
    """
    This is a comment block
    The range function will create values to iterate. The arguement is what value to iterate to.
    It will start from 0. range(10) will iterate through 0, 1, 2, ..., 9.
    This is the same as for (int i = 0; i < 10; i++)
    """
    print("This is inside for loop")

print("This is not in for loop")  # Unindent to end for loop

# This is a if statement. It must also be indented with a colon
if a == 5:
    print("a is 5")
elif a == 6:  # This is an else if statement. It must be indented
    print("This will never happen")
else:  # This is an else statement. It must be indented
    print("This also")


# This is a function. It must be indented
def myFunction():
    print("This is my function")


myFunction()  # The function won't run unless you call it

# Iterating though an array
d = [1, 1, 2, 3, 5, 8, 11]
for i in d:  # This will iterate though the array d
    print(i)  # Prints values in d one by one