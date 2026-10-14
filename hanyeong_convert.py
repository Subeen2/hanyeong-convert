"""한/영 자판 복원기 (Windows)

한/영 전환을 깜빡하고 친 글자를 드래그한 뒤 Ctrl+Shift+Space를 누르면 바꿔준다.
  ㅗ디ㅣㅐ -> hello   (한글이 섞여 있으면 한->영)
  dkssud   -> 안녕    (한글이 없으면 영->한)
바꾼 뒤 입력기도 바뀐 언어로 전환한다. 종료는 트레이가 없으니 작업 관리자에서 pythonw 종료.
"""
import ctypes
import sys
import time
from ctypes import wintypes

CHO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
JUNG = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
JONG = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"  # 0번 = 받침 없음

# 두벌식 자판: 자모 -> 같은 자리 영문 키
KO2EN = dict(zip(
    "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ",
    "rRseEfaqQtTdwWczxvgkoiOjpuPhynbml",
))
VOWEL_PAIRS = {"ㅗㅏ": "ㅘ", "ㅗㅐ": "ㅙ", "ㅗㅣ": "ㅚ", "ㅜㅓ": "ㅝ", "ㅜㅔ": "ㅞ", "ㅜㅣ": "ㅟ", "ㅡㅣ": "ㅢ"}
JONG_PAIRS = {"ㄱㅅ": "ㄳ", "ㄴㅈ": "ㄵ", "ㄴㅎ": "ㄶ", "ㄹㄱ": "ㄺ", "ㄹㅁ": "ㄻ", "ㄹㅂ": "ㄼ",
              "ㄹㅅ": "ㄽ", "ㄹㅌ": "ㄾ", "ㄹㅍ": "ㄿ", "ㄹㅎ": "ㅀ", "ㅂㅅ": "ㅄ"}
for pairs in (VOWEL_PAIRS, JONG_PAIRS):
    for keys, combo in pairs.items():
        KO2EN[combo] = KO2EN[keys[0]] + KO2EN[keys[1]]
EN2KO = {v: k for k, v in KO2EN.items() if len(v) == 1}


def has_hangul(text):
    return any("가" <= ch <= "힣" or "ㄱ" <= ch <= "ㅣ" for ch in text)


def ko2en(text):
    out = []
    for ch in text:
        if "가" <= ch <= "힣":
            s = ord(ch) - 0xAC00
            jamos = CHO[s // 588] + JUNG[s % 588 // 28] + JONG[s % 28].strip()
            out.append("".join(KO2EN[j] for j in jamos))
        else:
            out.append(KO2EN.get(ch, ch))
    return "".join(out)


def en2ko(text):
    t = [EN2KO.get(ch) or EN2KO.get(ch.lower()) or ch for ch in text]
    is_vowel = lambda i: i < len(t) and t[i] in JUNG
    is_cons = lambda i: i < len(t) and t[i] in CHO
    out, i = [], 0
    while i < len(t):
        if is_vowel(i):  # 초성 없는 모음
            v = t[i]
            if is_vowel(i + 1) and v + t[i + 1] in VOWEL_PAIRS:
                v, i = VOWEL_PAIRS[v + t[i + 1]], i + 1
            out.append(v)
            i += 1
        elif is_cons(i) and is_vowel(i + 1):  # 초성 + 중성 (+ 종성)
            cho, jung, i = t[i], t[i + 1], i + 2
            if is_vowel(i) and jung + t[i] in VOWEL_PAIRS:
                jung, i = VOWEL_PAIRS[jung + t[i]], i + 1
            jong = ""
            if is_cons(i) and t[i] in JONG and not is_vowel(i + 1):  # 뒤에 모음 오면 다음 글자 초성
                pair = t[i] + t[i + 1] if is_cons(i + 1) else ""
                if pair in JONG_PAIRS and not is_vowel(i + 2):
                    jong, i = JONG_PAIRS[pair], i + 2
                else:
                    jong, i = t[i], i + 1
            out.append(chr(0xAC00 + (CHO.index(cho) * 21 + JUNG.index(jung)) * 28 + JONG.index(jong or " ")))
        else:  # 홀로 남은 자음, 숫자, 기호
            out.append(t[i])
            i += 1
    return "".join(out)


def convert(text):
    return ko2en(text) if has_hangul(text) else en2ko(text)


# ---- Windows: 단축키, 클립보드, 키 입력 ----
user32, kernel32, imm32 = ctypes.windll.user32, ctypes.windll.kernel32, ctypes.windll.imm32
user32.GetClipboardData.restype = kernel32.GlobalLock.restype = kernel32.GlobalAlloc.restype = ctypes.c_void_p
kernel32.GlobalLock.argtypes = kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]
imm32.ImmGetDefaultIMEWnd.restype = wintypes.HWND
user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]

CF_UNICODETEXT, VK_CONTROL, KEYUP = 13, 0x11, 2
MOD_CONTROL, MOD_SHIFT, MOD_NOREPEAT, VK_SPACE = 0x2, 0x4, 0x4000, 0x20
HOTKEY = (MOD_CONTROL | MOD_SHIFT | MOD_NOREPEAT, VK_SPACE)  # 바꾸려면 여기만


def open_clipboard():
    for _ in range(20):  # 다른 앱이 잡고 있으면 잠깐 기다림
        if user32.OpenClipboard(None):
            return True
        time.sleep(0.02)
    return False


def get_clipboard():
    if not open_clipboard():
        return None
    try:
        h = user32.GetClipboardData(CF_UNICODETEXT)
        if not h:
            return None
        text = ctypes.wstring_at(kernel32.GlobalLock(h))
        kernel32.GlobalUnlock(h)
        return text
    finally:
        user32.CloseClipboard()


def set_clipboard(text):
    if not open_clipboard():
        return
    try:
        user32.EmptyClipboard()
        if text is None:
            return
        buf = ctypes.create_unicode_buffer(text)
        h = kernel32.GlobalAlloc(0x2, ctypes.sizeof(buf))  # GMEM_MOVEABLE
        ctypes.memmove(kernel32.GlobalLock(h), buf, ctypes.sizeof(buf))
        kernel32.GlobalUnlock(h)
        user32.SetClipboardData(CF_UNICODETEXT, h)
    finally:
        user32.CloseClipboard()


def press_ctrl(key):
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(ord(key), 0, 0, 0)
    user32.keybd_event(ord(key), 0, KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYUP, 0)


def set_ime_korean(on):
    hwnd = imm32.ImmGetDefaultIMEWnd(user32.GetForegroundWindow())
    user32.SendMessageW(hwnd, 0x283, 2, 1 if on else 0)  # WM_IME_CONTROL, IMC_SETCONVERSIONMODE


def on_hotkey():
    # 단축키 누른 손가락이 떨어질 때까지 대기 (안 그러면 Ctrl+Shift+C가 됨)
    while any(user32.GetAsyncKeyState(vk) & 0x8000 for vk in (0x10, 0x11, 0x12, 0x20)):
        time.sleep(0.01)
    # ponytail: 텍스트 클립보드만 복원, 이미지 등은 덮어씀. 필요하면 모든 포맷 백업으로
    saved = get_clipboard()
    seq = user32.GetClipboardSequenceNumber()
    press_ctrl("C")
    for _ in range(50):
        if user32.GetClipboardSequenceNumber() != seq:
            break
        time.sleep(0.01)
    else:
        return  # 선택된 글자 없음
    selected = get_clipboard()
    if selected:
        set_clipboard(convert(selected))
        press_ctrl("V")
        # ponytail: 고정 대기. 앱이 붙여넣기 전에 복원하면 원래 내용이 붙음. 느린 앱에서 그러면 늘릴 것
        time.sleep(0.8)
        set_ime_korean(not has_hangul(selected))
    set_clipboard(saved)


def alert(text):
    user32.MessageBoxW(None, text, "hanyeong-convert", 0x10)  # pythonw는 콘솔이 없어 오류가 안 보임


def main():
    if not user32.RegisterHotKey(None, 1, *HOTKEY):
        alert("단축키 등록 실패: 이미 실행 중이거나 다른 프로그램이 Ctrl+Shift+Space를 쓰는 중")
        sys.exit(1)
    print("대기 중: 글자 드래그 후 Ctrl+Shift+Space")
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
        if msg.message == 0x0312:  # WM_HOTKEY
            try:
                on_hotkey()
            except Exception as e:  # 한 번 실패해도 상주는 유지
                alert(f"변환 실패: {e!r}")


if __name__ == "__main__":
    main()
