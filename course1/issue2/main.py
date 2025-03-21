def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()  # 모든 줄을 읽어서 리스트로 저장
    except FileNotFoundError:
        print(f"Error: '{filename}' 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f'Error: 파일을 읽는 중 문제가 발생했습니다 - {e}')
        return None

def write_csv_file(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for row in data:
                file.write(','.join(row) + '\n')
        print(f'정렬된 데이터가 {filename}에 저장되었습니다.')
    except Exception as e:
        print(f'Error: 파일을 저장하는 중 문제가 발생했습니다 - {e}')

def write_binary_file(filename, data):
    try:
        with open(filename, 'wb') as file:
            for row in data:
                file.write("|".join(row).encode('utf-8') + b"\n")
        print(f"이진 파일로 저장되었습니다: {filename}")
    except Exception as e:
        print(f'Error: 이진 파일 저장 중 문제가 발생했습니다 - {e}')

def read_binary_file(filename):
    try:
        with open(filename, 'rb') as file:
            data = [line.decode('utf-8').strip().split('|') for line in file]
        print(f"이진 파일에서 읽어온 데이터:")
        for row in data:
            print(row) 
    except Exception as e:
        print(f'Error: 이진 파일을 읽는 중 문제가 발생했습니다 - {e}')

if __name__ == '__main__':

    filename = 'course1/issue2/Mars_Base_Inventory_List.csv'
    outfilename = 'course1/issue2/Mars_Base_Inventory_danger.csv'
    binfilename = 'course1/issue2/Mars_Base_Inventory_List.bin'
    contents = read_log_file(filename)
    
    if contents :
        data = [line.strip().split(",") for line in contents]
        
        result = list()
        result.append(data[0])
        
        for type in data[0]: 
            if type == 'Flammability':
                index = data[0].index('Flammability')
                print(index)
        
        for tuple in data[1:]:
            if float(tuple[index]) >= 0.7:
                result.append(tuple)
        
        # 인화성이 높은 순으로 정렬
        result[1:] = sorted(result[1:], key=lambda x: float(x[index]), reverse=True)
        
        # CSV 파일로 저장
        write_csv_file(outfilename, result)
        
        # 이진 파일로 저장
        write_binary_file(binfilename, result)
            
        # 이진 파일에서 읽고 출력
        read_binary_file(binfilename)