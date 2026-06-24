private void button1_Click(object sender, EventArgs e)
{
    try
    {
        int number = int.Parse("abc");
        MessageBox.Show(number.ToString());
    }
    catch (FormatException)
    {
        MessageBox.Show("Ошибка преобразования!");
    }
}