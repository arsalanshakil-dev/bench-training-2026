name = 'Alice'
age = 30
drink_coffee = True
salary = 50000.0

print(f"My name is {name}, I am {age} years old, {'I drink coffee' if drink_coffee else 'I do not drink coffee'}, and my salary is ${salary}.")

# Output:
# My name is Alice, I am 30 years old, I drink coffee, and my salary is $50000.0.

years_until_retirement = 60 - age
print(f"I have {years_until_retirement} years until retirement.")

# Output:
# I have 30 years until retirement. 

coffee_count = 3
weekly_coffee_budget = 150.0 * coffee_count
print(f"My weekly coffee budget is ${weekly_coffee_budget}.")

annual_coffee_budget = weekly_coffee_budget * 52
print(f"My annual coffee budget is ${annual_coffee_budget}.")

# Output:
# My weekly coffee budget is $450.0.
# My annual coffee budget is $23400.0.