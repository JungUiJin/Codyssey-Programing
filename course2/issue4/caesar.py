import string

# 보너스 과제용 간단한 사전 단어 세트
simple_dictionary = {"I love Mars", "I", "that", "love", "for", "Mars", "with", "you", "this", "but", "his", "from", "they", "say", "her"}

def caesar_cipher_decode(target_text, shift):
    decoded = []
    for char in target_text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base - shift) % 26 + base)
            decoded.append(new_char)
        else:
            decoded.append(char)
    return ''.join(decoded)

def contains_dictionary_word(text, dictionary):
    words = text.lower().split()
    for word in words:
        if word.strip(string.punctuation) in dictionary:
            return True
    return False

def main():
    # 1. 파일 읽기
    try:
        with open("password.txt", "r", encoding="utf-8") as f:
            password = f.read().strip()
    except FileNotFoundError:
        print("password.txt 파일을 찾을 수 없습니다.")
        return

    print("모든 Caesar Cipher 해독 결과 (Shift 1~25):\n")

    shift_results = {}

    # 2. 모든 시프트 결과 출력
    for shift in range(1, 26):
        decoded = caesar_cipher_decode(password, shift)
        shift_results[shift] = decoded
        if contains_dictionary_word(decoded, simple_dictionary):
            print(f"[Shift {shift:2}] (사전 단어 감지됨): {decoded}")
            save = input("해당 Shift를 result.txt에 저장하시겠습니까? (y/n) : ")
            if save == 'y' :
                with open("result.txt", "w", encoding="utf-8") as f:
                    f.write(decoded)
                print(f"[Shift {shift}] 결과가 result.txt에 저장되었습니다.")
                return
            else : continue
        else:
            print(f"[Shift {shift:2}]: {decoded}")

    # 3. 사용자에게 선택 요청
    try:
        user_shift = int(input("\n저장하고 싶은 시프트 번호를 입력하세요 (1~25), 또는 0을 입력해 종료: "))
        if user_shift in shift_results:
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write(shift_results[user_shift])
            print(f"[Shift {user_shift}] 결과가 result.txt에 저장되었습니다.")
        elif user_shift == 0:
            print("저장하지 않고 종료합니다.")
        else:
            print("유효하지 않은 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

if __name__ == "__main__":
    main()
