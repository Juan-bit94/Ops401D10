# Script:          
# Purpose: 
# Why

# Done: Create a function, calling a function, and passing a variable to the function.

def my_function(my_list = {5, 4, 3, 2, 1,}):
    for number in my_list:
        print(number)

if __name__ == "__main__":
    my_variable = [1, 2, 3, 4, 5]
    my_function(my_variable)
    my_function()