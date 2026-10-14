from hanyeong_convert import convert, en2ko, ko2en

cases = {
    "dkssudgktpdy": "안녕하세요",
    "dhkswjs": "완전",       # 겹모음 + 받침이 다음 초성으로
    "ekfr": "닭",            # 겹받침
    "ekfrdl": "닭이",
    "Rkr": "깍",             # 쌍자음
    "DKS": "안",             # Caps Lock
    "akE": "마ㄸ",           # ㄸ은 받침 불가
    "dml": "의",
    "hk": "ㅘ",
    "hello 123!": "ㅗ디ㅣㅐ 123!",
}
for en, ko in cases.items():
    assert en2ko(en) == ko, (en, en2ko(en), ko)

assert ko2en("ㅗ디ㅣㅐ") == "hello"
assert ko2en("안녕하세요") == "dkssudgktpdy"
assert ko2en("닭이 완전 깍") == "ekfrdl dhkswjs Rkr"
assert convert("ㅗ디ㅣㅐ wㅐ깅") == "hello world"   # 한글 섞이면 한->영
assert convert("dkssud") == "안녕"
for word in ["안녕하세요", "닭볶음탕", "꿇어앉았다", "의사결정", "뷁"]:
    assert en2ko(ko2en(word)) == word, word
print("ok")
