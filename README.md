# hanyeong-convert

한/영 전환을 깜빡하고 친 글자를 드래그 + 단축키 한 번으로 되돌리는 Windows 도구.

| 친 글자 | 변환 결과 |
|---|---|
| `ㅗ디ㅣㅐ` | `hello` |
| `dkssudgktpdy` | `안녕하세요` |

- 선택한 글자에 한글이 있으면 한→영, 없으면 영→한 (두벌식 기준)
- 바꾼 뒤 입력기도 바뀐 언어로 전환
- 원래 클립보드 텍스트는 복원

## 실행
Python 3만 있으면 됨 (추가 패키지 없음).

`hanyeong-convert.bat` 더블클릭 (콘솔 창 없이 백그라운드 실행, 어느 폴더에서 실행해도 됨).
이미 실행 중이거나 단축키가 겹치면 오류 팝업이 뜸.

글자를 드래그하고 `Ctrl+Shift+Space`. 단축키는 `hanyeong_convert.py`의 `HOTKEY`에서 변경.
종료는 작업 관리자에서 `pythonw` 종료. 부팅 때 자동 실행하려면 `shell:startup` 폴더에 `.bat` 바로가기 추가.

## 테스트
```
python test_hanyeong_convert.py
```

## 한계
- Windows 전용
- 텍스트 클립보드만 복원 (이미지 등을 복사해둔 상태였다면 덮어씀)
- Ctrl+C / Ctrl+V가 다른 단축키인 앱(일부 터미널 등)에서는 동작 안 함
