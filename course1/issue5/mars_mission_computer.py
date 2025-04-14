import time
import random
import os
import platform
import json
import subprocess

# 설정 파일 읽기 함수
def read_settings(file_path='course1/issue5/setting.txt'):
    settings = {'info': set(), 'load': set()}
    current_section = None

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('[') and line.endswith(']'):
                    section = line[1:-1].lower()
                    if section in settings:
                        current_section = section
                elif current_section:
                    settings[current_section].add(line)
    except FileNotFoundError:
        print(f'설정 파일 {file_path}이 존재하지 않습니다. 모든 정보를 출력합니다.')
        settings = None
    return settings

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        log_entry = ' | '.join(f"{key}: {value}" for key, value in self.env_values.items())

        try:
            with open('course1/issue/sensor_log.txt', 'a') as log_file:
                log_file.write(log_entry + '\n')
        except IOError as e:
            print(f"파일 기록 중 오류 발생: {e}")

        return self.env_values

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.ds = DummySensor()
        self.history = []
        self.settings = read_settings()

    def get_sensor_data(self):
        while True:
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            items = self.env_values.items()
            print('{')
            for i, (key, value) in enumerate(items):
                comma = ',' if i < len(items) - 1 else ''
                print(f"  '{key}': {value}{comma}")
            print('}')

            self.history.append(self.env_values.copy())

            if len(self.history) >= 60:
                avg_values = {}
                for key in self.env_values:
                    total = sum(entry[key] for entry in self.history[-60:])
                    avg = round(total / 60, 3)
                    avg_values[key] = avg

                print('\n--- 5분 평균 환경 값 ---')
                print('{')
                for i, (key, value) in enumerate(avg_values.items()):
                    comma = ',' if i < len(avg_values) - 1 else ''
                    print(f"  '{key}': {value}{comma}")
                print('}\n')

            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print('System stopped...')
                break

    def get_mission_computer_info(self):
        try:
            total_mem = self.get_total_memory_windows()

            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu': platform.processor(),
                'cpu_cores': os.cpu_count(),
                'memory_size_mb': total_mem
            }

            if self.settings and self.settings['info']:
                info = {k: v for k, v in info.items() if k in self.settings['info']}

            print('\n--- 미션 컴퓨터 시스템 정보 ---')
            print(json.dumps(info, indent=2))

        except Exception as e:
            print(f'시스템 정보 수집 중 오류 발생: {e}')

    def get_mission_computer_load(self):
        try:
            cpu = self.get_cpu_load_windows()
            mem = self.get_mem_load_windows()

            load = {
                'cpu_usage_percent': cpu,
                'memory_usage_percent': mem
            }

            if self.settings and self.settings['load']:
                load = {k: v for k, v in load.items() if k in self.settings['load']}

            print('\n--- 미션 컴퓨터 부하 정보 ---')
            print(json.dumps(load, indent=2))

        except Exception as e:
            print(f'부하 정보 수집 중 오류 발생: {e}')

    def get_cpu_load_windows(self):
        try:
            result = subprocess.check_output(
                'wmic cpu get loadpercentage', shell=True
            ).decode()
            for line in result.splitlines():
                if line.strip().isdigit():
                    return int(line.strip())
        except Exception:
            return -1
        return -1

    def get_total_memory_windows(self):
        try:
            result = subprocess.check_output(
                'wmic computersystem get TotalPhysicalMemory', shell=True
            ).decode()
            for line in result.splitlines():
                if line.strip().isdigit():
                    bytes_size = int(line.strip())
                    return bytes_size // (1024 * 1024)  # MB로 변환
        except Exception:
            return -1
        return -1

    def get_mem_load_windows(self):
        try:
            result = subprocess.check_output(
                'wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value', shell=True
            ).decode()
            lines = result.strip().splitlines()
            mem_info = {}
            for line in lines:
                if '=' in line:
                    key, value = line.split('=')
                    mem_info[key.strip()] = int(value.strip())
            free_kb = mem_info['FreePhysicalMemory']
            total_kb = mem_info['TotalVisibleMemorySize']
            used_kb = total_kb - free_kb
            percent = (used_kb / total_kb) * 100
            return round(percent, 2)
        except Exception:
            return -1

# 실행부
if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
