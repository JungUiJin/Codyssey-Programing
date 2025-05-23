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
            with open('course1/issue3/sensor_log.txt', 'a') as log_file:
                log_file.write(log_entry + '\n')
        except IOError as e:
            print(f"파일 기록 중 오류 발생: {e}")
        
        return self.env_values
    
ds = DummySensor()
    
ds.set_env()
    
env_data = ds.get_env()
    
print(env_data)
