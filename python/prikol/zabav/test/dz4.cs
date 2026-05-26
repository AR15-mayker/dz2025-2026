using System;

class BankAccount
{
    private double _balance;

    public double Balance
    {
        get { return _balance; }
    }

    public BankAccount(double balance)
    {
        if (balance < 0)
        {
            _balance = 0;
        }
        else
        {
            _balance = balance;
        }
    }

    public void Deposit(double amount)
    {
        if (amount > 0)
        {
            _balance += amount;
        }
    }

    public bool Withdraw(double amount)
    {
        if (amount > 0 && amount <= _balance)
        {
            _balance -= amount;
            return true;
        }

        return false;
    }

    public override string ToString()
    {
        return "Счет: " + _balance + " руб.";
    }
}

class Program
{
    static void Main()
    {
        BankAccount account = new BankAccount(1000);

        Console.WriteLine(account);

        account.Deposit(500);
        Console.WriteLine(account);

        bool result = account.Withdraw(300);

        Console.WriteLine("Снятие прошло: " + result);
        Console.WriteLine(account);
    }
}