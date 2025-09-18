<#
.SYNOPSIS
    Собирает информацию об аппаратном обеспечении Windows и сохраняет в `hardware_report.md`.

.DESCRIPTION
    Скрипт выполняет несколько WMI/PowerShell команд для сбора сведений о CPU, памяти, GPU, накопителях,
    материнской плате, сетевых адаптерах и ОС. Результат записывается в markdown-файл рядом со скриптом.

    Запуск: Откройте PowerShell и выполните:
        cd <путь к папке проекта>
        .\collect-hardware-info.ps1

    Для некоторых команд (dmidecode в Linux эквивалент, здесь не нужен) не требуется админ. Однако
    команды могут вернуть более подробную информацию при запуске от имени администратора.
#>

param(
    [string]$OutFile = "hardware_report.md"
)

function Write-SectionHeading { param($title) "## $title`n" }

# Collect data
$cpu = wmic cpu get name,numberofcores,numberoflogicalprocessors,maxclockspeed /format:list 2>$null
$memChips = wmic memorychip get devicelocator,capacity,speed,memorytype /format:list 2>$null
$totalMem = (systeminfo | Select-String "Total Physical Memory") -replace '.*?:\s*','' 2>$null
$gpu = wmic path win32_videocontroller get name,adapterram /format:list 2>$null
$disks = wmic diskdrive get model,size,interfacetype /format:list 2>$null
$logical = wmic logicaldisk get name,size,freespace /format:list 2>$null
$baseboard = wmic baseboard get product,manufacturer,version /format:list 2>$null
$systemModel = wmic computersystem get model,manufacturer /format:list 2>$null
$nics = wmic nic get name,macaddress,speed /format:list 2>$null
$os = wmic os get caption,version,buildnumber /format:list 2>$null

# Build markdown
$md = @()
$md += "# Отчёт: Информация об аппаратном обеспечении"
$md += "Создан: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
$md += Write-SectionHeading -title "Общая информация о системе"
$md += "**OS / Version / Build:**`n"
$md += "```
" + $os + "
```
$md += "**System model / Manufacturer:**`n"
$md += "```
" + $systemModel + "
```

$md += Write-SectionHeading -title "Центральный процессор"
$md += "```
" + $cpu + "
```

$md += Write-SectionHeading -title "Оперативная память (слоты)"
$md += "```
" + $memChips + "
```
$md += "**Total Physical Memory (systeminfo):** $totalMem`n"

$md += Write-SectionHeading -title "Графический процессор"
$md += "```
" + $gpu + "
```

$md += Write-SectionHeading -title "Накопители"
$md += "**Physical drives:**`n```
" + $disks + "
```
$md += "**Logical disks:**`n```
" + $logical + "
```

$md += Write-SectionHeading -title "Материнская плата"
$md += "```
" + $baseboard + "
```

$md += Write-SectionHeading -title "Сетевые адаптеры"
$md += "```
" + $nics + "
```

$md += Write-SectionHeading -title "Полезные команды (для ручного запуска)"
$md += "- `wmic cpu get name,numberofcores,numberoflogicalprocessors,maxclockspeed`
- `wmic memorychip get devicelocator, capacity, speed, memorytype`
- `systeminfo | findstr /R /C:\"Total Physical Memory\"`
- `wmic path win32_videocontroller get name, adapterram`
- `wmic diskdrive get model, size, interfacetype`
- `wmic baseboard get product, manufacturer, version`
- `ipconfig /all`"

$md += "`n---`n"
$md += "_Сгенерировано скриптом `collect-hardware-info.ps1`._"

# Write to file
$md -join "`n" | Out-File -FilePath $OutFile -Encoding UTF8

Write-Host "Created file:`t$OutFile"
