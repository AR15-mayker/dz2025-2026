using System;

class Program
{
    static void CompressArray(int[] arr)
    {
        int index = 0;

        for (int i = 0; i < arr.Length; i++)
        {
            if (arr[i] != 0)
            {
                arr[index] = arr[i];
                index++;
            }
        }

        while (index < arr.Length)
        {
            arr[index] = 0;
            index++;
        }
    }

    static void Main()
    {
        int[] arr = new int[10];
        Random random = new Random();

        Console.WriteLine("Исходный массив:");

        for (int i = 0; i < arr.Length; i++)
        {
            arr[i] = random.Next(0, 10);
            Console.Write(arr[i] + " ");
        }

        Console.WriteLine();

        CompressArray(arr);

        Console.WriteLine("Сжатый массив:");

        for (int i = 0; i < arr.Length; i++)
        {
            Console.Write(arr[i] + " ");
        }
    }
}