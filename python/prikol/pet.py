import time
import random

moods = ["😀", "😐", "😴", "😡", "🤢"]
hunger = 0
boredom = 0

def show_status():
    mood = moods[min((hunger + boredom) // 3, len(moods) - 1)]
    print(f"\nПитомец: {mood}")
    print(f"Голод: {hunger}/10")
    print(f"Скука: {boredom}/10")

def tick():
    global hunger, boredom
    hunger = min(10, hunger + 1)
    boredom = min(10, boredom + 1)

def feed():
    global hunger
    hunger = max(0, hunger - 3)
    print("Ты покормил питомца! 🍕")

def play():
    global boredom
    boredom = max(0, boredom - 3)
    print("Вы поиграли! 🎮")

def main():
    print("Твой консольный питомец запущен!")
    print("Команды: feed – покормить, play – поиграть, exit – выйти")

    while True:
        show_status()
        cmd = input("\nЧто сделать? ").strip().lower()
        
        if cmd == "feed":
            feed()
        elif cmd == "play":
            play()
        elif cmd == "exit":
            print("Питомец машет тебе лапкой и уходит спать... 😴")
            break
        else:
            print("Не понял команду :(")

        tick()
        time.sleep(0.5)

if __name__ == "__main__":
    main()
