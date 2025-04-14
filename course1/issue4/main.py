import time
import random 

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
            with open('course1/issue5/sensor_log.txt', 'a') as log_file:
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

    def get_sensor_data(self):
        start_time = time.time()
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

            # 5분(300초)마다 평균 출력
            if len(self.history) >= 60:
                avg_values = {}
                for key in self.env_values:
                    total = sum(entry[key] for entry in self.history[-60:])
                    avg = round(total / 60, 3)
                    avg_values[key] = avg

                items = list(avg_values.items())
                
                print('\n--- 5분 평균 환경 값 ---')
                print('{')
                for i, (key, value) in enumerate(items):
                    comma = ',' if i < len(items) - 1 else ''
                    print(f"  '{key}': {value}{comma}")
                print('}\n')

            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print('System stopped...')
                break


if __name__ == '__main__':
    
    # 인스턴스 생성 및 실행
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
