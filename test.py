def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total

def divide_numbers(a, b):
    return a / b  # No error handling!

# Using print for debugging
print("Testing the functions")
result = calculate_sum([1, 2, 3, 4, 5])
print(result)