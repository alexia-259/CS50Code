#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <math.h>

int word_count(string text);
int letter_count(string text);
int sentence_count(string text);
float average(int ls, int word);

int main(void)
{
    string text = get_string("Text: ");
    int word = word_count(text);
    int letter = letter_count(text);
    int sentence = sentence_count(text);
    float l = average(letter, word);
    float s = average(sentence, word);
    int index = round(0.0588 * l - 0.296 * s - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 1 && index <= 16)
    {
        printf("Grade %i\n", index);
    }
    else
    {
        printf("Grade 16+\n");
    }
}

int word_count(string text)
{
    int count = 1;
    for(int i = 0; text[i] != '\0'; i ++)
    {
        if (isblank(text[i]))
        {
            count ++;
        }
    }
    return count;
}

int letter_count(string text)
{
    int count = 0;
    for(int i = 0;text[i] != '\0'; i ++)
    {
        if (isalpha(text[i]))
        {
            count ++;
        }
    }
    return count;
}

int sentence_count(string text)
{
    int count = 0;
    for(int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count ++;
        }
    }
    return count;
}

float average(int ls, int word)
{
    float avg = (float) ls / word;
    float result = (float) avg * 100;
    return result;
}
