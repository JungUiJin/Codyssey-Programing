def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: '{filename}' 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f'Error: 파일을 읽는 중 문제가 발생했습니다 - {e}')
        return None

if __name__ == '__main__':
    print('Hello Mars')

    log_filename = 'mission_computer_main.log'
    log_content = read_log_file(log_filename)

    if log_content:
        print('\n[ 로그 파일 내용 ]')
        print(log_content)