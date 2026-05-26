using System;

class Program
{
    static void PrintMultiplicationTable(int n)
    {
        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                Console.Write((i * j).ToString().PadLeft(4));
            }

            Console.WriteLine();
        }
    }

    static void Main()
    {
        Console.Write("Введите n: ");
        int n = int.Parse(Console.ReadLine());

        PrintMultiplicationTable(n);
    }
}