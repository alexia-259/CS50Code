def main():
    text = input("Text: ")
    word = word_count(text)
    letter = letter_count(text)
    sentence = sentence_count(text)
    l = (letter/ word) * 100
    s = (sentence/ word) * 100
    index = round(0.0588 * l - 0.296 * s - 15.8)

    if index < 1:
        print("Before Grade 1")
    elif index < 16:
        print(f"Grade {index}")
    else:
        print("Grade 16+")


def word_count(t):
    space = len(t.split())
    return space

def letter_count(t):
    count = 0
    for c in t:
        if c.isalpha():
            count += 1
    return count

def sentence_count(t):
    d = t.count(".")
    q = t.count("?")
    e = t.count("!")
    s = d + q + e
    return s

if __name__ == "__main__":
    main()
