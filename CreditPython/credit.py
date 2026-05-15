import re

def main():
    while True:
        try:
            card = int(input("Number: "))
            if card > 0:
                break
        except ValueError:
            continue

    h = str(card)

    matches = re.search(r"^[0-9]{13,16}$", h)

    if not matches:
        print("INVALID")
        return

    if not checker(card):
        print("INVALID")
        return

    two_digits = int(h[:2])
    first_digit = int(h[0])

    if two_digits == 34 or two_digits == 37:
        print("AMEX")
    elif 51 <= two_digits <= 55:
        print("MASTERCARD")
    elif first_digit == 4:
        print("VISA")
    else:
        print("INVALID")



def checker(c):
    check1 = check_1(c)
    check2 = check_2(c)
    sumof = check1 + check2
    if sumof % 10 == 0:
        return True
    else:
        return False

def check_1(c):
    check1 = 0
    c = c // 10
    while c > 0:
        no = c % 10  # gets first number from the back
        no = no * 2    # times it by 2
        remainder = no % 10  # separates the numbers
        no = no // 10  #separates the numbers
        check1 = check1 + no + remainder  # adds them up
        c = c // 100
    return check1

def check_2(c):
    check2 = 0
    while c > 0:
        check2 += c % 10
        c = c // 100
    return check2




if __name__ == "__main__":
    main()
