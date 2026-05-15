def main():
    fraction = percentage("Fraction: ")
    if str(fraction).isdigit():
        print(f"{fraction}%")
    else:
        print(fraction)


def percentage(prompt):
    while True:
        try:
            user = input(prompt)
            x , y = user.split("/")
            x = int(x)
            y = int(y)
            if x > y :
                continue
            elif y == 0:
                continue
            elif x < 0 or y < 0:
                continue
            else:
                 value = round(( x / y ) * 100)
                 if value < 2:
                    empty = "E"
                    return empty
                 elif value > 98:
                    full = "F"
                    return full
                 else:
                     return value
        except ValueError:
            pass
        except ZeroDivisionError:
            pass

main()
