import json

EPS = 1e-6  # 부동소수 오차 허용 범위


# ============================
# 박스 길이/너비 vs 첫 박스 좌표 검증
# ============================

def is_zero(val, eps=EPS):
    return abs(val) < eps


def check_first_box_position(item):
    """
    규칙:
    - box_l > box_w → first_box.x == 0
    - box_w > box_l → first_box.y == 0

    return:
        "OK", "MISMATCH", "EQUAL"
    """

    pallet_l, pallet_w, box_l, box_w, box_cnt, start = item["input"]

    first_box = item["output"][0][0]
    x, y = first_box[0], first_box[1]

    if box_l > box_w:
        # x 좌표가 0이어야 함
        if is_zero(x):
            return "OK"
        else:
            return "MISMATCH"

    elif box_w > box_l:
        # y 좌표가 0이어야 함
        if is_zero(y):
            return "OK"
        else:
            return "MISMATCH"

    else:
        return "EQUAL"


# ============================
# JSON 전체 검사
# ============================

def analyze_dataset(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = {
        "OK": 0,
        "MISMATCH": 0,
        "EQUAL": 0
    }

    mismatches = []

    for idx, item in enumerate(data):
        result = check_first_box_position(item)
        stats[result] += 1

        if result == "MISMATCH":
            first_box = item["output"][0][0]
            mismatches.append({
                "index": idx,
                "input": item["input"],
                "box_l": item["input"][2],
                "box_w": item["input"][3],
                "first_box_xy": first_box[:2]
            })

    return stats, mismatches


# ============================
# 실행부
# ============================

if __name__ == "__main__":
    json_file = "C:/Users/82106/OneDrive/바탕 화면/visualizer/윈도우1_박스 개수별 구분/box_count_4.json"

    stats, mismatches = analyze_dataset(json_file)

    print("=== 첫 박스 좌표 검증 결과 ===")
    print(f"조건 일치 (OK)        : {stats['OK']}")
    print(f"조건 불일치 (MISMATCH): {stats['MISMATCH']}")
    print(f"길이 == 너비 (EQUAL)  : {stats['EQUAL']}")

    if mismatches:
        print("\n=== 불일치 샘플 (최대 5개) ===")
        for m in mismatches[:5]:
            print(m)