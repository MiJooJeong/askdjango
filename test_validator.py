import re

val = "01012341234abc"  # 11
# pattern = "^01[016789][1-9]\\d{6,7}$"
pattern = r"^01[016789][1-9]\d{6,7}$"   # raw

if re.match(pattern, val):
    print("matched")
else:
    print("invalid")
