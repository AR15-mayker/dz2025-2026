import socket
import struct
import os
import time
import json
from collections import defaultdict
from datetime import datetime

class PacketAnalyzer:
    def __init__(self):
        self.stats = defaultdict(int)
        self.start_time = time.time()
        self.packet_count = 0
        
    def parse_ip_header(self, raw_data):
        """
        Функция для парсинга IP-заголовка
        """
        # Проверяем минимальную длину пакета
        if len(raw_data) < 20:
            print("❌ Слишком короткий пакет для IP-заголовка")
            return None
            
        try:
            # Распаковываем первые 20 байт с помощью struct
            ip_header = struct.unpack('!BBHHHBBH4s4s', raw_data[:20])
            
            # Извлекаем поля согласно формату IP-заголовка
            version_ihl = ip_header[0]
            version = version_ihl >> 4
            ihl = (version_ihl & 0xF) * 4
            
            # Проверяем длину заголовка
            if ihl < 20 or ihl > len(raw_data):
                print("❌ Некорректная длина IP-заголовка")
                return None
                
            tos = ip_header[1]
            total_length = ip_header[2]
            identification = ip_header[3]
            flags_fragment = ip_header[4]
            ttl = ip_header[5]
            protocol = ip_header[6]
            checksum = ip_header[7]
            src_ip = socket.inet_ntoa(ip_header[8])
            dst_ip = socket.inet_ntoa(ip_header[9])
            
            # Обновляем статистику
            self.stats['total_packets'] += 1
            self.stats[f'protocol_{protocol}'] += 1
            self.stats[f'src_{src_ip}'] += 1
            self.stats[f'dst_{dst_ip}'] += 1
            
            # Определяем протокол верхнего уровня
            protocol_map = {
                1: 'ICMP',
                2: 'IGMP',
                6: 'TCP', 
                17: 'UDP',
                41: 'IPv6',
                89: 'OSPF'
            }
            protocol_name = protocol_map.get(protocol, f'Unknown ({protocol})')
            
            # Анализ флагов фрагментации
            flags = flags_fragment >> 13
            fragment_offset = flags_fragment & 0x1FFF
            
            mf_flag = flags & 1
            df_flag = (flags >> 1) & 1
            reserved_flag = (flags >> 2) & 1
            
            # Выводим информацию о пакете
            print("\n" + "="*60)
            print(f"📦 ОБНАРУЖЕН IP-ПАКЕТ #{self.packet_count + 1}")
            print("="*60)
            print(f"🕒 Время: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
            print(f"🌐 Версия IP: {version}")
            print(f"📏 Длина заголовка: {ihl} байт")
            print(f"🎯 Тип услуги (TOS): {tos} (0x{tos:02x})")
            print(f"📊 Общая длина пакета: {total_length} байт")
            print(f"🆔 Идентификатор: {identification} (0x{identification:04x})")
            print(f"⏳ TTL: {ttl}")
            print(f"📡 Протокол: {protocol_name}")
            print(f"✅ Контрольная сумма: 0x{checksum:04x}")
            print(f"📤 IP-адрес отправителя: {src_ip}")
            print(f"📥 IP-адрес получателя: {dst_ip}")
            print(f"🚩 Флаги: MF={mf_flag}, DF={df_flag}, Reserved={reserved_flag}")
            print(f"📍 Смещение фрагмента: {fragment_offset}")
            
            if mf_flag or fragment_offset > 0:
                print("⚠️  Пакет фрагментирован!")
            
            # Возвращаем данные для возможного дальнейшего анализа
            return {
                'protocol': protocol,
                'protocol_name': protocol_name,
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'total_length': total_length,
                'header_length': ihl,
                'ttl': ttl,
                'data': raw_data[ihl:total_length],
                'timestamp': time.time()
            }
            
        except struct.error as e:
            print(f"❌ Ошибка распаковки IP-заголовка: {e}")
            return None
        except Exception as e:
            print(f"❌ Неожиданная ошибка при парсинге IP-заголовка: {e}")
            return None

    def analyze_upper_layer(self, packet_info):
        """
        Функция для анализа протоколов верхнего уровня
        """
        if not packet_info:
            return
            
        protocol = packet_info['protocol']
        data = packet_info['data']
        
        print(f"🔍 Анализ {packet_info['protocol_name']}...")
        
        if protocol == 6 and len(data) >= 20:  # TCP
            try:
                tcp_header = struct.unpack('!HHLLBBHHH', data[:20])
                src_port = tcp_header[0]
                dst_port = tcp_header[1]
                sequence = tcp_header[2]
                acknowledgment = tcp_header[3]
                data_offset = (tcp_header[4] >> 4) * 4
                flags = tcp_header[5]
                
                # Анализ TCP флагов
                flag_names = []
                if flags & 0x01: flag_names.append("FIN")
                if flags & 0x02: flag_names.append("SYN")  
                if flags & 0x04: flag_names.append("RST")
                if flags & 0x08: flag_names.append("PSH")
                if flags & 0x10: flag_names.append("ACK")
                if flags & 0x20: flag_names.append("URG")
                
                print(f"🔗 TCP: {src_port} → {dst_port}")
                print(f"   Seq: {sequence}, Ack: {acknowledgment}")
                print(f"   Флаги: {', '.join(flag_names) if flag_names else 'None'}")
                print(f"   Длина данных: {len(data) - data_offset} байт")
                
                # Определяем известные порты
                port_info = self.get_port_info(src_port, dst_port)
                if port_info:
                    print(f"   💡 {port_info}")
                    
            except Exception as e:
                print(f"🔗 TCP: ошибка анализа - {e}")
        
        elif protocol == 17 and len(data) >= 8:  # UDP
            try:
                udp_header = struct.unpack('!HHHH', data[:8])
                src_port = udp_header[0]
                dst_port = udp_header[1]
                length = udp_header[2]
                checksum = udp_header[3]
                
                print(f"🔗 UDP: {src_port} → {dst_port}")
                print(f"   Длина: {length} байт, Контрольная сумма: 0x{checksum:04x}")
                print(f"   Данные: {len(data) - 8} байт")
                
                port_info = self.get_port_info(src_port, dst_port)
                if port_info:
                    print(f"   💡 {port_info}")
                    
            except Exception as e:
                print(f"🔗 UDP: ошибка анализа - {e}")
        
        elif protocol == 1 and len(data) >= 4:  # ICMP
            try:
                icmp_header = struct.unpack('!BBH', data[:4])
                icmp_type = icmp_header[0]
                icmp_code = icmp_header[1]
                icmp_checksum = icmp_header[2]
                
                icmp_types = {
                    0: "Echo Reply", 8: "Echo Request",
                    3: "Destination Unreachable", 11: "Time Exceeded"
                }
                
                type_name = icmp_types.get(icmp_type, "Unknown")
                print(f"🔗 ICMP: {type_name} (type={icmp_type}, code={icmp_code})")
                print(f"   Контрольная сумма: 0x{icmp_checksum:04x}")
                
            except Exception as e:
                print(f"🔗 ICMP: ошибка анализа - {e}")

    def get_port_info(self, src_port, dst_port):
        """Определяет сервисы по портам"""
        common_ports = {
            80: "HTTP", 443: "HTTPS", 53: "DNS", 25: "SMTP",
            110: "POP3", 143: "IMAP", 22: "SSH", 23: "Telnet",
            21: "FTP", 67: "DHCP Server", 68: "DHCP Client",
            161: "SNMP", 123: "NTP", 993: "IMAPS", 995: "POP3S"
        }
        
        src_service = common_ports.get(src_port)
        dst_service = common_ports.get(dst_port)
        
        if src_service and dst_service:
            return f"{src_service} → {dst_service}"
        elif src_service:
            return f"Источник: {src_service}"
        elif dst_service:
            return f"Назначение: {dst_service}"
        
        return None

    def show_statistics(self):
        """Показывает статистику захвата"""
        duration = time.time() - self.start_time
        print("\n" + "="*50)
        print("📊 СТАТИСТИКА ЗАХВАТА")
        print("="*50)
        print(f"Общее время: {duration:.2f} секунд")
        print(f"Всего пакетов: {self.stats['total_packets']}")
        print(f"Скорость: {self.stats['total_packets'] / duration:.2f} пакетов/сек")
        
        # Статистика по протоколам
        protocol_stats = {k: v for k, v in self.stats.items() if k.startswith('protocol_')}
        if protocol_stats:
            print("\n📡 По протоколам:")
            for proto_key, count in protocol_stats.items():
                proto_id = proto_key.replace('protocol_', '')
                proto_map = {'6': 'TCP', '17': 'UDP', '1': 'ICMP'}
                proto_name = proto_map.get(proto_id, f'Proto {proto_id}')
                print(f"  {proto_name}: {count} пакетов")

    def save_packet_to_file(self, raw_data, filename=None):
        """Сохраняет пакет в файл"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"packet_{timestamp}.bin"
            
        try:
            with open(filename, 'wb') as f:
                f.write(raw_data)
            print(f"💾 Пакет сохранен в файл: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Ошибка сохранения пакета: {e}")
            return None

    def start_sniffing(self, packet_limit=0, filter_protocol=None):
        """
        Основная функция для захвата пакетов
        """
        sniffer = None
        try:
            # Создаем RAW socket для захвата IP-пакетов
            sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            
            # Получаем имя текущего интерфейса
            hostname = socket.gethostname()
            host = socket.gethostbyname(hostname)
            
            # Привязываем сокет к интерфейсу
            sniffer.bind((host, 0))
            
            # Включаем режим promiscuous для захвата всех пакетов
            sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Для Windows нужно дополнительно включить promiscuous mode
            if os.name == 'nt':
                sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            
            print(f"🚀 Захват пакетов запущен на интерфейсе {host}")
            if filter_protocol:
                print(f"🔧 Фильтр: {filter_protocol}")
            if packet_limit > 0:
                print(f"🎯 Ограничение: {packet_limit} пакетов")
            print("📡 Ожидание пакетов... (Ctrl+C для остановки)")
            print("-" * 60)
            
            while True:
                if packet_limit > 0 and self.packet_count >= packet_limit:
                    print(f"\n🎯 Достигнут лимит в {packet_limit} пакетов")
                    break
                    
                # Читаем пакет
                raw_data, addr = sniffer.recvfrom(65565)
                self.packet_count += 1
                
                # Парсим IP-заголовок
                packet_info = self.parse_ip_header(raw_data)
                
                # Применяем фильтр по протоколу
                if packet_info and filter_protocol:
                    if packet_info['protocol_name'].upper() != filter_protocol.upper():
                        continue
                
                # Анализ протоколов верхнего уровня
                if packet_info:
                    self.analyze_upper_layer(packet_info)
                    
                    # Предлагаем сохранить интересные пакеты
                    if packet_info['protocol'] in [6, 17, 1]:  # TCP, UDP, ICMP
                        if input("💾 Сохранить пакет в файл? (y/N): ").lower() == 'y':
                            self.save_packet_to_file(raw_data)
                
                # Показываем статистику каждые 10 пакетов
                if self.packet_count % 10 == 0:
                    self.show_statistics()
                    
        except KeyboardInterrupt:
            print("\n\n⏹️ Захват пакетов остановлен пользователем")
        except PermissionError:
            print("❌ ОШИБКА: Для захвата пакетов требуются права администратора!")
            print("   Запустите скрипт от имени администратора/root")
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")
        finally:
            # Выключаем promiscuous mode для Windows
            if sniffer:
                if os.name == 'nt':
                    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                sniffer.close()
            
            # Финальная статистика
            self.show_statistics()

def analyze_packet_from_file(filename):
    """
    Функция для анализа заранее сохраненного пакета
    """
    analyzer = PacketAnalyzer()
    try:
        with open(filename, 'rb') as f:
            raw_data = f.read()
        print(f"📁 Анализ пакета из файла: {filename}")
        print(f"📏 Размер файла: {len(raw_data)} байт")
        
        packet_info = analyzer.parse_ip_header(raw_data)
        if packet_info:
            analyzer.analyze_upper_layer(packet_info)
            
    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден")
    except Exception as e:
        print(f"❌ Ошибка при анализе файла: {e}")

def main():
    print("🛠️ АНАЛИЗАТОР IP-ПАКЕТОВ v2.0")
    print("="*50)
    
    analyzer = PacketAnalyzer()
    
    while True:
        print("\nВыберите режим работы:")
        print("1 - Захват пакетов в реальном времени")
        print("2 - Анализ пакета из файла") 
        print("3 - Захват с фильтром по протоколу")
        print("4 - Захват с ограничением по количеству пакетов")
        print("5 - Выход")
        
        choice = input("Ваш выбор (1-5): ").strip()
        
        if choice == "1":
            analyzer.start_sniffing()
            break
        elif choice == "2":
            filename = input("Введите имя файла с пакетом: ").strip()
            analyze_packet_from_file(filename)
            break
        elif choice == "3":
            protocol = input("Введите протокол для фильтра (TCP/UDP/ICMP): ").strip().upper()
            if protocol in ['TCP', 'UDP', 'ICMP']:
                analyzer.start_sniffing(filter_protocol=protocol)
                break
            else:
                print("❌ Неверный протокол. Используйте TCP, UDP или ICMP")
        elif choice == "4":
            try:
                limit = int(input("Введите количество пакетов для захвата: ").strip())
                analyzer.start_sniffing(packet_limit=limit)
                break
            except ValueError:
                print("❌ Введите корректное число")
        elif choice == "5":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    # Проверяем права администратора
    if os.name != 'nt' and os.geteuid() != 0:
        print("⚠️  Внимание: Для полной функциональности запустите скрипт с правами root!")
        print("   Используйте: sudo python3 packet_analyzer.py")
        print("   Продолжить без прав администратора? (y/N): ", end="")
        if input().lower() != 'y':
            exit()
    
    main()