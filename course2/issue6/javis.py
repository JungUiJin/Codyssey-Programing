import os
import wave
import datetime
import pyaudio
import threading
import csv
import speech_recognition as sr  # STT를 위한 외부 라이브러리

class VoiceRecorder:
    def __init__(self):
        # 녹음 파일을 저장할 폴더 이름
        self.record_folder = 'course2/issue6/records'
        self.csv_folder = 'course2/issue6/csv'

        # 오디오 설정 값
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

        self.audio = pyaudio.PyAudio()
        self.is_recording = False
        self.frames = []

        if not os.path.exists(self.record_folder):
            os.makedirs(self.record_folder)
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)

    def get_timestamp_filename(self):
        # 현재 시간을 기반으로 파일 이름 생성
        now = datetime.datetime.now()
        return now.strftime('%Y%m%d-%H%M%S') + '.wav'

    def get_recoders_full_path(self, filename):
        # 저장 경로를 포함한 전체 파일 경로 반환
        return os.path.join(self.record_folder, filename)
    
    def get_csv_full_path(self, filename):
        # 저장 경로를 포함한 전체 파일 경로 반환
        return os.path.join(self.csv_folder, filename)

    def start_recording(self):
        # 음성 녹음을 시작하는 함수
        self.is_recording = True
        self.frames = []

        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        print('녹음을 시작합니다. 종료하려면 Enter 키를 누르세요.')

        while self.is_recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

        filename = self.get_timestamp_filename()
        full_path = self.get_recoders_full_path(filename)

        with wave.open(full_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f'녹음이 완료되었습니다. 파일이 저장되었습니다: {full_path}')

    def stop_recording(self):
        # 외부 입력으로 녹음을 중단
        self.is_recording = False

    def list_recordings_by_date_range(self, start_date, end_date):
        # 날짜 범위로 녹음 파일 목록 출력
        files = os.listdir(self.record_folder)
        selected_files = []

        for file in files:
            try:
                timestamp_str = file.replace('.wav', '')
                file_date = datetime.datetime.strptime(timestamp_str, '%Y%m%d-%H%M%S').date()
                if start_date <= file_date <= end_date:
                    selected_files.append(file)
            except ValueError:
                continue

        print('해당 범위의 녹음 파일 목록:')
        for file in selected_files:
            print(file)

    def convert_audio_to_text(self, filename):
        # STT 기능: 녹음된 파일에서 텍스트를 추출하고 CSV로 저장
        recognizer = sr.Recognizer()
        recoders_full_path = self.get_recoders_full_path(filename)

        try:
            with sr.AudioFile(recoders_full_path) as source:
                audio_data = recognizer.record(source)

            # Google STT API 사용 (인터넷 연결 필요)
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print('인식된 텍스트:', text)

            # CSV 파일로 저장
            csv_filename = filename.replace('.wav', '.csv')
            csv_path = self.get_csv_full_path(csv_filename)

            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Time', 'Text'])  # 헤더
                writer.writerow(['00:00:00', text])  # 단일 블록 저장

            print(f'CSV 파일이 저장되었습니다: {csv_path}')

        except sr.UnknownValueError:
            print('음성을 인식할 수 없습니다.')
        except sr.RequestError as e:
            print(f'Google STT 요청 실패: {e}')

    def search_keyword_in_csv_file(self, filename, keyword):
        # 단일 CSV 파일 내에서 키워드 검색
        full_path = self.get_csv_full_path(filename)
        print(f'"{keyword}" 키워드 검색 결과 in {filename}:')
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 헤더 건너뜀
                for row in reader:
                    if keyword in row[1]:
                        print(f'{filename} [{row[0]}] : {row[1]}')
        except FileNotFoundError:
            print(f'파일을 찾을 수 없습니다: {filename}')


def wait_for_enter(recorder):
    # 녹음을 종료하기 위해 Enter 키를 기다리는 스레드용 함수
    input()
    recorder.stop_recording()


def main():
    recorder = VoiceRecorder()

    while True:
        print('\n[1] 녹음 시작 (Enter로 종료)')
        print('[2] 녹음 파일 조회 (날짜 범위)')
        print('[3] 음성 파일 텍스트로 변환 (STT)')
        print('[4] 키워드로 CSV 검색 (파일 선택 후)')
        print('[0] 종료')
        choice = input('메뉴를 선택하세요: ')

        if choice == '1':
            stopper = threading.Thread(target=wait_for_enter, args=(recorder,))
            stopper.start()
            recorder.start_recording()
            stopper.join()

        elif choice == '2':
            start_input = input('시작 날짜 (예: 20250601): ')
            end_input = input('종료 날짜 (예: 20250608): ')
            try:
                start = datetime.datetime.strptime(start_input, '%Y%m%d').date()
                end = datetime.datetime.strptime(end_input, '%Y%m%d').date()
                recorder.list_recordings_by_date_range(start, end)
            except ValueError:
                print('잘못된 날짜 형식입니다. 다시 시도하세요.')

        elif choice == '3':
            filename = input('변환할 녹음 파일명을 입력하세요 (예: 20250608-211245.wav): ')
            recorder.convert_audio_to_text(filename)

        elif choice == '4':
            files = os.listdir(recorder.csv_folder)
            csv_files = [f for f in files if f.endswith('.csv')]
            if not csv_files:
                print('CSV 파일이 없습니다.')
            else:
                page = 0
                page_size = 10
                total_pages = (len(csv_files) - 1) // page_size + 1
                while True:
                    start = page * page_size
                    end = start + page_size
                    page_items = csv_files[start:end]
                    print(f'\nCSV 파일 목록 (페이지 {page+1}/{total_pages}):')
                    for idx, f in enumerate(page_items, start=1):
                        print(f'{idx}. {f}')
                    nav = input("번호 선택, n(다음), p(이전), q(취소): ")
                    if nav.lower() == 'n':
                        if page < total_pages - 1:
                            page += 1
                        else:
                            print('마지막 페이지입니다.')
                    elif nav.lower() == 'p':
                        if page > 0:
                            page -= 1
                        else:
                            print('첫 페이지입니다.')
                    elif nav.lower() == 'q':
                        break
                    else:
                        try:
                            sel = int(nav)
                            if 1 <= sel <= len(page_items):
                                filename = page_items[sel-1]
                                keyword = input('검색할 키워드를 입력하세요: ')
                                recorder.search_keyword_in_csv_file(filename, keyword)
                                break
                            else:
                                print('올바른 번호를 입력하세요.')
                        except ValueError:
                            print('올바른 입력이 아닙니다.')

        elif choice == '0':
            print('프로그램을 종료합니다.')
            break

        else:
            print('올바른 메뉴를 선택하세요.')


if __name__ == '__main__':
    main()
