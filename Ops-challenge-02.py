# Script:          
# Purpose: 
# Why

import datetime
import os

def my_function(my_list = {5, 4, 3, 2, 1,}):
    for number in my_list:
        print(number)

now  = datetime.datetime.now()
print(now)

new_date = datetime.date(1996, 12, 11)
print(new_date)

time_now = time.time()
print(time_now)

result = os.system('ping -c 2')
if __name__ == "__main__":
    my_variable = [1, 2, 3, 4, 5]
    my_function(my_variable)
    my_function()