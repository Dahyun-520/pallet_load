import json
import math

EPS = 1e-6


def is_close(a, b, eps=EPS):
    return abs(a - b) < eps


def analyze_grid_basis(item):
    """
    박스 배치가
    - 짧은 변 기준 행렬인지
    - 긴 변 기준 행렬인지
    - 섞여있는지
    판별
    """

    box_l = item["input"][2]
    box_w = item["input"][3]

    short_side = min(box_l, box_w)
    long_side = max(box_l, box_w)

    odd_layer = item["output"][0]

    xs = sorted(set(round(x, 6) for x, _, _ in odd_layer))
    ys = sorted(set(round(y, 6) for _, y, _ in odd_layer))

    def get_steps(arr):
        return [round(abs(arr[i+1] - arr[i]), 6) for i in range(len(arr)-1)]

    x_steps = get_steps(xs)
    y_steps = get_steps(ys)

    def classify_steps(steps):
        if not steps:
            return "single"

        short_hits = sum(is_close(s, short_side) for s in steps)
        long_hits  = sum(is_close(s, long_side) for s in steps)

        if short_hits >= long_hits and short_hits > 0:
            return "short"
        if long_hits > short_hits:
            return "long"
        return "mixed"

    return {
        "x_basis": classify_steps(x_steps),
        "y_basis": classify_steps(y_steps),
        "short_side": short_side,
        "long_side": long_side,
        "x_steps": x_steps,
        "y_steps": y_steps
    }


def analyze_dataset(json_path):
    # 🔥 여기서 파일을 불러옴
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = {
        "short_based": 0,
        "long_based": 0,
        "mixed": 0
    }

    mixed_samples = []

    for idx, item in enumerate(data):
        result = analyze_grid_basis(item)

        if (
            result["x_basis"] == "short" and result["y_basis"] in ("long", "single")
        ) or (
            result["y_basis"] == "short" and result["x_basis"] in ("long", "single")
        ):
            stats["short_based"] += 1
        elif result["x_basis"] == "long" or result["y_basis"] == "long":
            stats["long_based"] += 1
        else:
            stats["mixed"] += 1
            mixed_samples.append({
                "index": idx,
                "input": item["input"],
                "analysis": result
            })

    return stats, mixed_samples


# ============================
# 실행부 (여기서 파일 지정)
# ============================

if __name__ == "__main__":
    json_file = "C:/Users/82106/OneDrive/바탕 화면/visualizer/윈도우1_박스 개수별 구분/box_count_24.json"

    stats, mixed = analyze_dataset(json_file)

    print("=== 행렬 기준 분석 결과 ===")
    print(f"짧은 변 기준 : {stats['short_based']}")
    print(f"긴 변 기준   : {stats['long_based']}")
    print(f"혼합 / 불명  : {stats['mixed']}")

    if mixed:
        print("\n=== 혼합 케이스 예시 (최대 3개) ===")
        for m in mixed[:3]:
            print(m)