#include <cs50.h>
#include <stdio.h>

int main(void)
{

    int counter = 0;
    long holder; // holds the value of the card

    do
    {
        holder = get_long("Number: "); // user input
    }
    while (holder < 0);

    long card = holder;

    while (holder > 0)
    {
        holder = holder / 10;
        counter++;
    }
    //printf("%i\n", counter);

    if (counter < 13 || counter > 16)
    {
        printf("INVALID\n");
    }

    // to do the check_sum
    // get second to last digit, then devide by 100
    // times those numbers by 2
    // add each integer from those numbers
    else
    {



        long check_card = card; // holds the value of the card
        long card_type = card;  // holds the value of the card, i dont know how to do it any other way
                            // for the last check
        int number1 = 0;        // numbers for the first check
        int check1 = 0;         // adding integers after diving them
        card = card / 10;

        while (card > 0)
        {
            // first, times by 2 all the numbers and add them as single int
            
            number1 = card % 10;
            number1 = number1 * 2;

            int reminder = number1 % 10;
            number1 = number1 / 10;
            check1 = check1 + number1 + reminder;
            card = card / 100;



        }

        // the numbers for the second part of the check
        int number2 = 0;
        int check2 = 0;

        while (check_card > 0)
        {
            // then, add the rest of the integers
            number2 = check_card % 10;
            check_card = check_card / 100;
            check2 = check2 + number2;
            //printf("%i\n", check2) ;
        }


        // adding both of the checks
        int check_sum = check1 + check2;

        // this will check if the number ends in a 0, which is the sum



        if (check_sum % 10 != 0)
        {
        printf("INVALID\n");
        }
        else
        {
            // gives you the first two digits of the credit card number
            // this can be used to check what type of card it is
            while (card_type > 100)
            {
                card_type = card_type / 10;
            }

            // checks which card it actually is
            // do if, else if, else statements so it is all continous rather than just if statements
            if ((card_type == 34 || card_type == 37) && counter == 15)
            {
                printf("AMEX\n");
            }
             else if ((card_type >= 51 && card_type <= 55) && counter == 16)
             {
                printf("MASTERCARD\n");
             }
            else if (card_type / 10 == 4 && (counter == 13 || counter == 16))
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
    }

}
