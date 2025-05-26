import zipfile
import itertools
import string
import time
from multiprocessing import Process, Value, Queue, cpu_count
import os

ZIP_PATH = "course2\issue3\emergency_storage_key.zip"
CHARSET = string.digits + string.ascii_lowercase  # '0123456789abcdefghijklmnopqrstuvwxyz'
PASSWORD_LENGTH = 6

def try_passwords(start_index, step, found_flag, queue):
    total_attempts = 0
    start_time = time.time()
    zf = zipfile.ZipFile(ZIP_PATH)

    for i, pwd_tuple in enumerate(itertools.product(CHARSET, repeat=PASSWORD_LENGTH)):
        if found_flag.value:
            return  # 다른 프로세스에서 성공하면 종료

        if i % step != start_index:
            continue

        password = ''.join(pwd_tuple)
        total_attempts += 1

        try:
            zf.extractall(pwd=bytes(password, 'utf-8'))
            elapsed = time.time() - start_time
            found_flag.value = 1
            print(f"[+] 프로세스 {start_index} 성공: '{password}'")
            queue.put(password)
            return
        except:
            if total_attempts % 1000000 == 0:
                elapsed = time.time() - start_time

def unlock_zip():
    if not os.path.exists(ZIP_PATH):
        print(f"[!] zip 파일이 존재하지 않습니다: {ZIP_PATH}")
        return

    print("[*] 멀티프로세싱을 이용한 zip 크래킹을 시작합니다.")
    start_time = time.time()

    manager_flag = Value('i', 0)  # 성공 여부 공유 변수
    password_queue = Queue()

    cpu_cores = cpu_count()
    print(f"[*] 사용 가능한 CPU 코어 수: {cpu_cores}")

    processes = []
    for i in range(cpu_cores):
        p = Process(target=try_passwords, args=(i, cpu_cores, manager_flag, password_queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    elapsed = time.time() - start_time
    if not password_queue.empty():
        password = password_queue.get()
        print(f"[+] 최종 성공! 비밀번호는: {password}")
        with open("password.txt", "w") as f:
            f.write(password)
    else:
        print("[-] 비밀번호를 찾지 못했습니다.")
    print(f"[*] 총 소요 시간: {elapsed:.2f}초")

if __name__ == '__main__':
    unlock_zip()
