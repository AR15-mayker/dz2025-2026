using System;

class Program
{
    static void Main()
    {
        Console.Write("Введите шестизначное число: ");
        int number = int.Parse(Console.ReadLine());

        int d1 = number / 100000;
        int d2 = number / 10000 % 10;
        int d3 = number / 1000 % 10;

        int d4 = number / 100 % 10;
        int d5 = number / 10 % 10;
        int d6 = number % 10;

        int sum1 = d1 + d2 + d3;
        int sum2 = d4 + d5 + d6;

        if (sum1 == sum2)
        {
            Console.WriteLine("Билет счастливый");
        }
        else
        {
            Console.WriteLine("Билет не счастливый");
        }
    }
}