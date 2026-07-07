
import json

# =========================
# 설정
# =========================
INPUT_JSON_PATH = "C:/Users/82106/OneDrive/바탕 화면/visualizer/윈도우1_박스 개수별 구분/box_count_4.json"


with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

total_count = len(data)
line_data_count = 0   # odd에서 x=0 또는 y=0 인 데이터 수

for item in data:
    output = item.get("output", [])

    if not output or len(output) < 1:
        continue

    odd_boxes = output[0]

    xs = [box[0] for box in odd_boxes]
    ys = [box[1] for box in odd_boxes]

    all_x_zero = all(x == 0.0 for x in xs)
    all_y_zero = all(y == 0.0 for y in ys)

    # x=0 이거나 y=0 인 경우 → 일직선 데이터
    if all_x_zero or all_y_zero:
        line_data_count += 1


normal_data_count = total_count - line_data_count

print(f"전체 데이터 수                  : {total_count}")
print(f"x 또는 y 좌표가 전부 0.0 인 데이터 : {line_data_count}")
print(f"x,y 좌표가 모두 0.0이 아닌 데이터 : {normal_data_count}")






'''
import json

# =========================
# 설정
# =========================
INPUT_JSON_PATH = "C:/Users/82106/OneDrive/바탕 화면/visualizer/윈도우1_박스 개수별 구분/box_count_4.json"


with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

longer_count = 0   # 긴변*2 > 팔렛트 길이
shorter_count = 0  # 긴변*2 <= 팔렛트 길이

for item in data:
    inp = item["input"]

    pallet_length = inp[0]
    box_length = inp[2]
    box_width = inp[3]

    # 박스의 긴 변 선택
    long_side = max(box_length, box_width)

    # 긴 변 * 2 와 팔렛트 길이 비교
    if long_side * 2 > pallet_length:
        longer_count += 1
    else:
        shorter_count += 1


print(f"긴변*2가 팔렛트 길이보다 긴 데이터   : {longer_count}개")
print(f"긴변*2가 팔렛트 길이보다 짧은 데이터 : {shorter_count}개")



import json

# =========================
# 설정
# =========================
INPUT_JSON_PATH = "C:/Users/82106/OneDrive/바탕 화면/visualizer/윈도우1_박스 개수별 구분/box_count_4.json"


with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 카운터
long_gap_shorter = 0    # pallet - long*2 가 더 짧음
short_gap_shorter = 0   # pallet - short*4 가 더 짧음
gap_equal = 0           # 둘이 같은 경우
line_data_total = 0     # x or y = 0 인 데이터 총합


for item in data:
    output = item.get("output", [])
    if not output:
        continue

    # --------
    # odd 좌표 기준 일직선 판별
    # --------
    odd_boxes = output[0]
    xs = [box[0] for box in odd_boxes]
    ys = [box[1] for box in odd_boxes]

    all_x_zero = all(x == 0.0 for x in xs)
    all_y_zero = all(y == 0.0 for y in ys)

    if not (all_x_zero or all_y_zero):
        continue  # 분석 대상 아님

    line_data_total += 1

    # --------
    # INPUT 기반 계산
    # --------
    inp = item["input"]
    pallet_L = inp[0]
    box_L = inp[2]
    box_W = inp[3]

    long_side = max(box_L, box_W)
    short_side = min(box_L, box_W)

    gap_long = pallet_L - (long_side * 2)
    gap_short = pallet_L - (short_side * 4)

    # --------
    # 비교
    # --------
    if gap_long < gap_short:
        long_gap_shorter += 1
    elif gap_short < gap_long:
        short_gap_shorter += 1
    else:
        gap_equal += 1


print(f"x 또는 y 좌표가 전부 0.0 인 데이터 수 : {line_data_total}")
print()
print(f"팔렛트 - 긴변*2 가 더 짧은 데이터   : {long_gap_shorter}")
print(f"팔렛트 - 짧은변*4 가 더 짧은 데이터 : {short_gap_shorter}")
print(f"두 값이 같은 데이터                : {gap_equal}")
'''
import json

# =========================
# 설정
# =========================
INPUT_JSON_PATH = "C:/Users/82106/OneDrive/바탕 화면/visualizer/윈도우1_박스 개수별 구분/box_count_4.json"


with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

short2_less_long = 0   # 짧은변*2 < 긴변
others = 0             # 나머지 (>=)

for item in data:
    inp = item["input"]

    box_L = inp[2]
    box_W = inp[3]

    long_side = max(box_L, box_W)
    short_side = min(box_L, box_W)

    if short_side * 2 < long_side:
        short2_less_long += 1
    else:
        others += 1


print(f"짧은 변 * 2 < 긴 변 인 데이터 : {short2_less_long}개")
print(f"그 외 데이터 (>=)            : {others}개")