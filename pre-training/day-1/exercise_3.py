def printTable(number):
    print(f"Multiplication Table for {number}:")
    for i in range(1, 11):
        print(f"{number} x {i} = {number * i}")

start_number = 1
end_number = 12

while True:
    print(f"Enter number between {start_number} and {end_number} or enter 0 to view all tables or -1 to exit:")
    number = int(input())

    if number == -1:
        print("Exiting...")
        break
    elif number == 0:
        for i in range(start_number, end_number + 1):
            printTable(i)
    elif number >= start_number and number <= end_number:
        printTable(number)
    else:
        print("Invalid input. Please enter a number between 1 and 12.")