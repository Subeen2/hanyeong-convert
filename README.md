# hanyeong-convert

한/영 전환을 깜빡하고 친 글자를 드래그 + 단축키 한 번으로 되돌리는 Windows 도구.

| 친 글자 | 변환 결과 |
|---|---|
| `ㅗ디ㅣㅐ` | `hello` |
| `dkssudgktpdy` | `안녕하세요` |

- 선택한 글자에 한글이 있으면 한→영, 없으면 영→한 (두벌식 기준)
- 바꾼 뒤 입력기도 바뀐 언어로 전환
- 원래 클립보드 텍스트는 복원

## 다운로드 (Python 없이)
1. **파일 놓기**: [Releases](https://github.com/Subeen2/hanyeong-convert/releases/latest)에서 `hanyeong-convert.exe`를 받아 지우지 않을 폴더(예: 문서)로 옮기기
2. **처음 실행**: 더블클릭 — 창 없이 백그라운드에서 실행됨. "Windows의 PC 보호" 경고가 뜨면 [추가 정보] → [실행] (서명 안 된 개인 제작 exe라 뜨는 경고)
3. **부팅 때 자동 실행**
   1. exe 우클릭 → [더 많은 옵션 표시] → [바로 가기 만들기]
   2. `Win+R` → `shell:startup` → Enter (시작프로그램 폴더가 열림)
   3. 만든 바로 가기를 그 폴더로 옮기기 → 다음 부팅부터 자동 실행
4. **끄기**: 작업 관리자(`Ctrl+Shift+Esc`) → `hanyeong-convert.exe` → [작업 끝내기]
5. **자동 실행 해제**: `shell:startup` 폴더에서 바로 가기 삭제

실행 중에 또 실행하면 "단축키 등록 실패" 팝업이 뜸 — 이미 켜져 있다는 뜻이라 무시해도 됨.

## 소스로 실행
Python 3만 있으면 됨 (추가 패키지 없음).

`hanyeong-convert.bat` 더블클릭 (콘솔 창 없이 백그라운드 실행, 어느 폴더에서 실행해도 됨).
이미 실행 중이거나 단축키가 겹치면 오류 팝업이 뜸.

글자를 드래그하고 `Ctrl+Shift+Space`. 단축키는 `hanyeong_convert.py`의 `HOTKEY`에서 변경.
종료는 작업 관리자에서 `pythonw` 종료. 부팅 때 자동 실행하려면 `shell:startup` 폴더에 `.bat` 바로가기 추가.

## exe 빌드
```
pip install pyinstaller
pyinstaller --onefile --noconsole --name hanyeong-convert hanyeong_convert.py
```

## 테스트
```
python test_hanyeong_convert.py
```

## 한계
- Windows 전용
- 텍스트 클립보드만 복원 (이미지 등을 복사해둔 상태였다면 덮어씀)
- Ctrl+C / Ctrl+V가 다른 단축키인 앱(일부 터미널 등)에서는 동작 안 함
