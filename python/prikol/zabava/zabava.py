import time
import random
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.layout import Layout
from rich import print as rprint

console = Console()

def imperial_factory_activation():
    # Создаем макет для интерфейса
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    
    # Стилизованный заголовок
    title = Text("⚙️ АКТИВАЦИЯ ИМПЕРСКОГО ЗАВОДА ⚙️", style="bold bright_yellow")
    title_panel = Panel(Align.center(title), style="bright_red")
    layout["header"].update(title_panel)
    
    # Основная область с прогресс-баром
    progress_table = Progress(
        SpinnerColumn("dots", style="cyan"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=50),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        expand=True
    )
    
    # Список систем для активации
    systems = [
        {"name": "Инициализация систем управления...", "weight": 1.0},
        {"name": "Загрузка энергетических контуров...", "weight": 0.8},
        {"name": "Калибровка производственных линий...", "weight": 0.7},
        {"name": "Запуск имперских протоколов...", "weight": 0.6},
        {"name": "Диагностика защитных систем...", "weight": 0.9},
        {"name": "Оптимизация рабочих процессов...", "weight": 0.5}
    ]
    
    # Случайный выбор систем, которые будут активированы (от 3 до 6)
    selected_systems = random.sample(systems, random.randint(3, 6))
    
    # Шанс сбоя (20%)
    failure_chance = 0.5
    will_fail = random.random() < failure_chance
    failure_system = None
    failure_point = 0
    
    if will_fail:
        failure_system = random.randint(0, len(selected_systems) - 1)
        failure_point = random.randint(30, 90)
    
    with progress_table as progress:
        tasks = []
        for system in selected_systems:
            task = progress.add_task(f"[cyan]{system['name']}", total=100)
            tasks.append(task)
        
        console.print(layout)
        console.print("\n")
        
        # Имитация загрузки с разной скоростью
        completed = [False] * len(tasks)
        current_progress = [0] * len(tasks)
        
        while not all(completed):
            for i, task in enumerate(tasks):
                if not completed[i]:
                    # Случайная скорость прогресса для каждой системы
                    speed = random.uniform(0.3, 1.5) * selected_systems[i]["weight"]
                    current_progress[i] += speed
                    
                    # Проверка на сбой
                    if (will_fail and i == failure_system and 
                        current_progress[i] >= failure_point and 
                        current_progress[i] < 100):
                        
                        # СБОЙ СИСТЕМЫ!
                        progress.update(task, completed=100, description=f"[bold red]СБОЙ: {selected_systems[i]['name']}")
                        console.print("\n")
                        error_panel = Panel.fit(
                            Align.center(f"🚨 [bold red]КРИТИЧЕСКИЙ СБОЙ СИСТЕМЫ!\\n"
                                        f"Система: {selected_systems[i]['name']}\\n"
                                        f"Код ошибки: 0x{random.randint(0x1000, 0xFFFF):04X}"), 
                            style="red",
                            border_style="bright_red"
                        )
                        console.print(error_panel)
                        
                        # Аварийное завершение других систем
                        for j, other_task in enumerate(tasks):
                            if j != i and not completed[j]:
                                progress.update(other_task, completed=current_progress[j], 
                                              description=f"[yellow]ПРЕРВАНО: {selected_systems[j]['name']}")
                        
                        console.print("\n")
                        shutdown_panel = Panel.fit(
                            Align.center("🔴 [bold red]АВАРИЙНОЕ ОТКЛЮЧЕНИЕ ЗАВОДА\\n"
                                        "ИНИЦИИРОВАНА ПРОЦЕДУРА ДИАГНОСТИКИ"), 
                            style="red"
                        )
                        console.print(shutdown_panel)
                        return
                    
                    if current_progress[i] >= 100:
                        current_progress[i] = 100
                        completed[i] = True
                        progress.update(task, completed=100, description=f"[green]✓ {selected_systems[i]['name']}")
                    else:
                        progress.update(task, completed=current_progress[i])
            
            time.sleep(0.1)
    
    # УСПЕШНАЯ АКТИВАЦИЯ
    console.print("\n")
    
    # Случайные показатели эффективности
    efficiency = random.randint(85, 99)
    power_level = random.randint(90, 100)
    production_capacity = random.randint(80, 95)
    
    success_messages = [
        "✅ [bold green]Все системы инициализированы!",
        f"⚡ [bold green]Эффективность: {efficiency}%",
        f"🔋 [bold green]Энергетический уровень: {power_level}%",
        f"🏭 [bold green]Производственная мощность: {production_capacity}%",
        "👑 [bold bright_yellow]ИМПЕРСКИЙ ЗАВОД ПОЛНОСТЬЮ АКТИВИРОВАН!"
    ]
    
    for message in success_messages:
        console.print(Panel.fit(Align.center(message), style="green"))
        time.sleep(0.5)
    
    # Финальная заставка
    final_display = Panel.fit(
        Align.center(f"🚀 [bold bright_yellow]ЗАВОД ГОТОВ К ПРОИЗВОДСТВУ!\\n\\n"
                    f"⚙️  Эффективность: {efficiency}%\\n"
                    f"🔋  Энергетический уровень: {power_level}%\\n"
                    f"🏭  Производственная мощность: {production_capacity}%\\n"
                    f"👑  Имперские протоколы: АКТИВИРОВАНЫ"), 
        style="bright_yellow",
        border_style="red"
    )
    console.print("\n")
    console.print(final_display)

if __name__ == "__main__":
    imperial_factory_activation()