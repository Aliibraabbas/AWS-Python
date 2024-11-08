# Take ina list ofnumbers from the useran run FizzBuzz on that list
#when you loop through the listeremember the rules:
# 1 if the number is divisible by both 3 and 5 print "FizzBuzz"
# 2 if the number is divisible by 3 print "Fizz"
# 3 if the number is divisible by 5 print "Buzz"
# 4 Otherwise just print the number

# def fizz_buzz(numbers):
#     for number in numbers:
#         if number % 3 == 0 and number % 5 == 0:
#             print("FizzBuzz")
#         elif number % 3 == 0:
#             print("Fizz")
#         elif number % 5 == 0:
#             print("Buzz")
#         else:
#             print(number)


def FizzBuzz(n):
     if n%3 and n%5:
        return "FizzBuzz"
     elif n%3:
        return "Fizz"
     elif n%5:
        return "Buzz"
     else:
        return n
     
def sort_custom ():
    pass

def main () -> str:
    list_numbers = [33, 6, 9, 34, 12, 90, 56]

    res = filter(lambda x: x < 12, list_numbers)
    print(list(res))
    
    result = []
    for elm in list_numbers:
        if elm < 12:
            result.append(elm)

    print(result)



    # list_numbers = [
    #     {"value": 33, }, {"value": 15, }, {"value": 5, }, {"value": 3, }, {"value": 2, }, {"value": 1, }
    # ]








# def main () -> str:
#     list_numbers = [33, 15, 5, 3, 2, 1]
#     for elm in list_numbers:
#         res = FizzBuzz(elm)
#         print(res)

#         print(list_numbers)

# def main () -> str:
#     try:
#         n: int = int(input())
#     except ValueError:
#         print('Please enter a number')
#         raise ValueError ('Please enter a number')
        
#     print(type(n))


if __name__ == '__main__':
    main()