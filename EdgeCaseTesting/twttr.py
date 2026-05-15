def main():
    user = input("Input: ")
    output = shorten(user)
    print("Output: ", output)

def shorten(user):
    vowel = ''
    for v in user:
        if v in ["a","i","u","e","o","A","I","U","E","O"]:
            v = v.replace(v , "")
            vowel += v
        else:
            vowel += v
    return vowel

if __name__ == "__main__":
    main()

