import os
import wave
import datetime
import pyaudio
import threading


class VoiceRecorder:
    def __init__(self):
        # 녹음 파일을 저장할 폴더 이름
        self.record_folder = 'course2/issue5/records'

        # 오디오 설정 값
        self.chunk = 1024              # 오디오 버퍼 크기
        self.format = pyaudio.paInt16  # 샘플 포맷 (16비트 PCM)
        self.channels = 1              # 모노 채널
        self.rate = 44100              # 샘플링 레이트 (Hz)

        self.audio = pyaudio.PyAudio()  # PyAudio 객체 생성
        self.is_recording = False       # 녹음 중 상태 여부
        self.frames = []                # 녹음한 오디오 프레임 저장 리스트

        # 폴더가 없다면 새로 생성
        if not os.path.exists(self.record_folder):
            os.makedirs(self.record_folder)

    def get_timestamp_filename(self):
        # 현재 시간을 기반으로 파일 이름 생성 (예: 20250608-211245.wav)
        now = datetime.datetime.now()
        return now.strftime('%Y%m%d-%H%M%S') + '.wav'

    def get_full_path(self, filename):
        # 파일 이름에 저장 경로를 붙여서 전체 경로 반환
        return os.path.join(self.record_folder, filename)

    def start_recording(self):
        # 녹음 시작 함수
        self.is_recording = True
        self.frames = []

        # 마이크 입력 스트림 열기
        stream = self.audio.open(format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        print('녹음을 시작합니다. 종료하려면 Enter 키를 누르세요.')

        # 사용자가 녹음을 중단할 때까지 계속 오디오 데이터를 수집
        while self.is_recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        # 스트림 종료
        stream.stop_stream()
        stream.close()

        # 파일로 저장
        filename = self.get_timestamp_filename()
        full_path = self.get_full_path(filename)

        with wave.open(full_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f'녹음이 완료되었습니다. 파일이 저장되었습니다: {full_path}')

    def stop_recording(self):
        # 외부 입력으로 녹음을 중단하는 함수
        self.is_recording = False

    def list_recordings_by_date_range(self, start_date, end_date):
        # 주어진 날짜 범위 내의 녹음 파일 목록 출력
        files = os.listdir(self.record_folder)
        selected_files = []

        for file in files:
            try:
                # 파일명에서 날짜 정보 파싱
                timestamp_str = file.replace('.wav', '')
                file_date = datetime.datetime.strptime(timestamp_str, '%Y%m%d-%H%M%S').date()
                if start_date <= file_date <= end_date:
                    selected_files.append(file)
            except ValueError:
                # 파일명이 날짜 형식이 아닐 경우 무시
                continue

        print('해당 범위의 녹음 파일 목록:')
        for file in selected_files:
            print(file)


def wait_for_enter(recorder):
    # 사용자의 Enter 키 입력을 대기하는 함수 (스레드용)
    input()
    recorder.stop_recording()


def main():
    # 프로그램 메인 루프
    recorder = VoiceRecorder()

    while True:
        print('\n[1] 녹음 시작 (Enter로 종료)')
        print('[2] 녹음 파일 조회 (날짜 범위)')
        print('[0] 종료')
        choice = input('메뉴를 선택하세요: ')

        if choice == '1':
            # 녹음 시작: stop을 위한 입력은 별도 스레드에서 기다림
            stopper = threading.Thread(target=wait_for_enter, args=(recorder,))
            stopper.start()

            # 메인 스레드에서는 녹음 실행
            recorder.start_recording()

            # 입력 스레드가 종료될 때까지 대기
            stopper.join()

        elif choice == '2':
            # 날짜 범위로 파일 조회
            start_input = input('시작 날짜 (예: 20250601): ')
            end_input = input('종료 날짜 (예: 20250608): ')
            try:
                start = datetime.datetime.strptime(start_input, '%Y%m%d').date()
                end = datetime.datetime.strptime(end_input, '%Y%m%d').date()
                recorder.list_recordings_by_date_range(start, end)
            except ValueError:
                print('잘못된 날짜 형식입니다. 다시 시도하세요.')

        elif choice == '0':
            # 프로그램 종료
            print('프로그램을 종료합니다.')
            break

        else:
            print('올바른 메뉴를 선택하세요.')


# 프로그램 실행 시작점
if __name__ == '__main__':
    main()
