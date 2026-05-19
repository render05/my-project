# Assignment 1

# -------------------------------
# Question 1 and 5
# Student Result and Grade System
# -------------------------------

name = input("Enter student name: ")
student_class = input("Enter class: ")

sub1 = float(input("Enter marks of Subject 1: "))
sub2 = float(input("Enter marks of Subject 2: "))
sub3 = float(input("Enter marks of Subject 3: "))
sub4 = float(input("Enter marks of Subject 4: "))
sub5 = float(input("Enter marks of Subject 5: "))

total = sub1 + sub2 + sub3 + sub4 + sub5
percentage = total / 5

# Grade Calculation
if percentage >= 60:
    grade = 'A'
elif percentage >= 50:
    grade = 'B'
elif percentage >= 40:
    grade = 'C'
elif percentage >= 33:
    grade = 'D'
else:
    grade = 'Fail'

print("\n----- Student Result -----")
print("Name:", name)
print("Class:", student_class)
print("Total Marks:", total)
print("Percentage:", percentage)
print("Grade:", grade)


# -------------------------------
# Question 2
# String Methods
# -------------------------------

str1 = input("\nEnter first string: ")
str2 = input("Enter second string: ")

new_string = str1 + " " + str2

print("\nConcatenated String:", new_string)

print("lower():", new_string.lower())
print("upper():", new_string.upper())
print("title():", new_string.title())
print("swapcase():", new_string.swapcase())
print("capitalize():", new_string.capitalize())
print("casefold():", new_string.casefold())
print("center():", new_string.center(50))
print("count('a'):", new_string.count('a'))
print("endswith('a'):", new_string.endswith('a'))
print("find('a'):", new_string.find('a'))
print("isalnum():", new_string.isalnum())
print("isdigit():", new_string.isdigit())
print("isnumeric():", new_string.isnumeric())
print("isspace():", new_string.isspace())
print("replace():", new_string.replace('a', '@'))


# -------------------------------
# Question 4
# Assignment Operators Practice
# -------------------------------

print("\nAssignment Operators Practice")

x = 10

print("Initial value:", x)

x += 5
print("After += 5:", x)

x -= 3
print("After -= 3:", x)

x *= 2
print("After *= 2:", x)

x /= 4
print("After /= 4:", x)

x %= 3
print("After %= 3:", x)