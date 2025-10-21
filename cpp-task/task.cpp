#include <Servo.h>
#include <Arduino.h>

// Пин-конфигурация
const int TRIG_PIN = 2;
const int ECHO_PIN = 3;
const int SERVO_PIN = 9;

// Константы системы
const float MIN_DISTANCE = 2.0;    // Минимальное расстояние (см)
const float MAX_DISTANCE = 100.0;  // Максимальное расстояние (см)
const int DEFAULT_BUFFER_SIZE = 5; // Размер буфера по умолчанию

// Зоны регулирования с гистерезисом
const float NEAR_ZONE = 20.0;
const float MID_ZONE = 50.0;
const float HYSTERESIS = 2.0;      // Гистерезис для предотвращения дребезга

// Глобальные переменные
Servo servo;
float* measurementBuffer = nullptr;
int bufferSize = 0;
int bufferIndex = 0;
int measurementCount = 0;
float lastFilteredDistance = 0.0;
int lastZone = -1; // -1: не определено, 0: near, 1: mid, 2: far

// ==================== ДИНАМИЧЕСКИЕ МАССИВЫ И УКАЗАТЕЛИ ====================

// Создание динамического буфера
float* createBuffer(const int size) {
    if (size <= 0) return nullptr;
    return new float[size];
}

// Удаление буфера
void deleteBuffer(float*& buffer) {
    if (buffer != nullptr) {
        delete[] buffer;
        buffer = nullptr;
    }
}

// Добавление измерения в кольцевой буфер (работа через указатели)
void addMeasurement(float* const buffer, const float value, const int size, int& index, int& count) {
    if (buffer == nullptr || size <= 0) return;
    
    *(buffer + index) = value;  // Адресная арифметика
    index = (index + 1) % size;
    
    if (count < size) {
        count++;
    }
}

// ==================== ФИЛЬТРАЦИЯ ДАННЫХ ====================

// Быстрая сортировка для медианного фильтра
void quickSort(float* arr, const int left, const int right) {
    if (left >= right) return;
    
    float pivot = *(arr + (left + right) / 2);
    int i = left;
    int j = right;
    
    while (i <= j) {
        while (*(arr + i) < pivot) i++;
        while (*(arr + j) > pivot) j--;
        
        if (i <= j) {
            float temp = *(arr + i);
            *(arr + i) = *(arr + j);
            *(arr + j) = temp;
            i++;
            j--;
        }
    }
    
    quickSort(arr, left, j);
    quickSort(arr, i, right);
}

// Медианный фильтр
float calculateMedian(const float* const buffer, const int count) {
    if (buffer == nullptr || count <= 0) return 0.0;
    
    // Создаем временный массив для сортировки
    float* tempBuffer = new float[count];
    for (int i = 0; i < count; i++) {
        tempBuffer[i] = *(buffer + i);
    }
    
    quickSort(tempBuffer, 0, count - 1);
    
    float median;
    if (count % 2 == 0) {
        median = (tempBuffer[count / 2 - 1] + tempBuffer[count / 2]) / 2.0;
    } else {
        median = tempBuffer[count / 2];
    }
    
    delete[] tempBuffer;
    return median;
}

// Скользящее среднее
float calculateAverage(const float* const buffer, const int count) {
    if (buffer == nullptr || count <= 0) return 0.0;
    
    float sum = 0.0;
    for (int i = 0; i < count; i++) {
        sum += *(buffer + i);
    }
    
    return sum / count;
}

// Комбинированная фильтрация (медиана + скользящее среднее)
float applyFilters(const float* const buffer, const int count) {
    float median = calculateMedian(buffer, count);
    float average = calculateAverage(buffer, count);
    
    // Комбинируем фильтры для лучшего сглаживания
    return (median + average) / 2.0;
}

// ==================== ЛОГИКА УПРАВЛЕНИЯ ====================

// Определение зоны с гистерезисом
int determineZone(const float distance, const int lastZone) {
    int newZone;
    
    if (distance <= NEAR_ZONE) {
        newZone = 0; // Near
    } else if (distance <= MID_ZONE) {
        newZone = 1; // Mid
    } else {
        newZone = 2; // Far
    }
    
    // Применяем гистерезис
    if (lastZone != -1 && abs(newZone - lastZone) == 1) {
        float transitionPoint = (newZone > lastZone) ? 
            (lastZone == 0 ? NEAR_ZONE : MID_ZONE) : 
            (lastZone == 1 ? NEAR_ZONE + HYSTERESIS : MID_ZONE + HYSTERESIS);
            
        if ((newZone > lastZone && distance < transitionPoint + HYSTERESIS) ||
            (newZone < lastZone && distance > transitionPoint - HYSTERESIS)) {
            return lastZone; // Остаемся в предыдущей зоне
        }
    }
    
    return newZone;
}

// Преобразование расстояние → сигнал управления
float calculateOutput(const float distance) {
    float normalized;
    int currentZone = determineZone(distance, lastZone);
    
    switch (currentZone) {
        case 0: // Near zone (0-20 см)
            normalized = map(constrain(distance, MIN_DISTANCE, NEAR_ZONE), 
                           MIN_DISTANCE, NEAR_ZONE, 0, 85);
            break;
        case 1: // Mid zone (20-50 см)
            normalized = map(constrain(distance, NEAR_ZONE, MID_ZONE), 
                           NEAR_ZONE, MID_ZONE, 85, 170);
            break;
        case 2: // Far zone (50+ см)
            normalized = map(constrain(distance, MID_ZONE, MAX_DISTANCE), 
                           MID_ZONE, MAX_DISTANCE, 170, 255);
            break;
        default:
            normalized = 0;
    }
    
    lastZone = currentZone;
    return normalized;
}

// Обновление выхода (управление сервоприводом)
void updateOutput(const float signal) {
    int servoAngle = map(constrain(signal, 0, 255), 0, 255, 0, 180);
    servo.write(servoAngle);
}

// ==================== РАБОТА С ДАТЧИКОМ ====================

// Измерение расстояния HC-SR04
float readDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    long duration = pulseIn(ECHO_PIN, HIGH, 30000); // Таймаут 30ms
    float distance = duration * 0.034 / 2;
    
    // Проверка валидности данных
    if (distance < MIN_DISTANCE || distance > MAX_DISTANCE || duration == 0) {
        return -1.0; // Некорректное измерение
    }
    
    return distance;
}

// ==================== ПЕРЕГРУЖЕННЫЕ ФУНКЦИИ ====================

// Базовая инициализация
void initializeSystem() {
    initializeSystem(DEFAULT_BUFFER_SIZE);
}

// Инициализация с указанием размера буфера
void initializeSystem(const int size) {
    // Настройка пинов
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    
    // Инициализация сервопривода
    servo.attach(SERVO_PIN);
    
    // Создание буфера измерений
    if (measurementBuffer != nullptr) {
        deleteBuffer(measurementBuffer);
    }
    
    bufferSize = max(1, size); // Минимальный размер 1
    measurementBuffer = createBuffer(bufferSize);
    bufferIndex = 0;
    measurementCount = 0;
    
    // Инициализация начальных значений
    lastFilteredDistance = 0.0;
    lastZone = -1;
    
    Serial.begin(9600);
    Serial.println("System initialized with buffer size: " + String(bufferSize));
}

// ==================== ОСНОВНЫЕ ФУНКЦИИ ARDUINO ====================

void setup() {
    initializeSystem(7); // Инициализация с буфером размера 7
}

void loop() {
    // Измерение расстояния
    float rawDistance = readDistance();
    
    if (rawDistance > 0) { // Валидное измерение
        // Добавление в буфер
        addMeasurement(measurementBuffer, rawDistance, bufferSize, 
                      bufferIndex, measurementCount);
        
        // Применение фильтров
        float filteredDistance = applyFilters(measurementBuffer, measurementCount);
        lastFilteredDistance = filteredDistance;
        
        // Преобразование в сигнал управления
        float outputSignal = calculateOutput(filteredDistance);
        
        // Обновление выхода
        updateOutput(outputSignal);
        
        // Отладочная информация
        Serial.print("Raw: ");
        Serial.print(rawDistance);
        Serial.print("cm | Filtered: ");
        Serial.print(filteredDistance);
        Serial.print("cm | Signal: ");
        Serial.print(outputSignal);
        Serial.print(" | Zone: ");
        Serial.println(lastZone);
    } else {
        Serial.println("Invalid measurement detected");
    }
    
    delay(100); // Задержка между измерениями
}

// ==================== ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ====================

// Получение статистики буфера
void getBufferStats(const float* const buffer, const int count, 
                   float& minVal, float& maxVal, float& avgVal) {
    if (buffer == nullptr || count <= 0) {
        minVal = maxVal = avgVal = 0.0;
        return;
    }
    
    minVal = maxVal = *buffer;
    float sum = 0.0;
    
    for (int i = 0; i < count; i++) {
        float val = *(buffer + i);
        if (val < minVal) minVal = val;
        if (val > maxVal) maxVal = val;
        sum += val;
    }
    
    avgVal = sum / count;
}

// Сброс системы
void resetSystem() {
    bufferIndex = 0;
    measurementCount = 0;
    lastFilteredDistance = 0.0;
    lastZone = -1;
    
    if (measurementBuffer != nullptr) {
        for (int i = 0; i < bufferSize; i++) {
            *(measurementBuffer + i) = 0.0;
        }
    }
}