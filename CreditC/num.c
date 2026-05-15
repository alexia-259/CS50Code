#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long number = 12345678911224 ;
    int position = 0;
//    int dig = number % 100 ;
//    printf("%i\n", dig) ;


   while (number > 0)
    {
        string dig = number  ;
        number /= 100 ;
        position++ ;

        printf("(%i) %d ", position , dig) ;
    }
}
