import json

# ============================
# 1. odd 레이어 방향이 모두 같은지 체크
# ============================

def is_uniform_direction(layer):
    """
    layer: [[x, y, dir], ...]
    return:
        True  -> 전부 같은 방향 (윈도우형)
        False -> 방향이 섞여 있음 (바람개비형)
    """
    dirs = {d for _, _, d in layer}
    return len(dirs) == 1


# ============================
# 2. odd 기준 패턴 판별
# ============================

def classify_pattern_by_odd(output):
    """
    output: [odd_layer, even_layer]

    기준:
    - odd의 dir가 전부 같으면 → window
    - odd의 dir가 섞여 있으면 → pinwheel
    """
    odd_layer = output[0]

    if is_uniform_direction(odd_layer):
        return "window"

    return "pinwheel"


# ============================
# 3. JSON 분리 저장
# ============================

def split_and_save_dataset(
    input_json_path,
    window_output_path,
    pinwheel_output_path
):
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    window_data = []
    pinwheel_data = []

    for item in data:
        pattern = classify_pattern_by_odd(item["output"])

        if pattern == "window":
            window_data.append(item)
        else:
            pinwheel_data.append(item)

    # 저장 (원래 JSON 포맷 그대로)
    with open(window_output_path, "w", encoding="utf-8") as f:
        json.dump(window_data, f, ensure_ascii=False, indent=2)

    with open(pinwheel_output_path, "w", encoding="utf-8") as f:
        json.dump(pinwheel_data, f, ensure_ascii=False, indent=2)

    print("=== 분리 저장 완료 ===")
    print(f"윈도우형   : {len(window_data)} → {window_output_path}")
    print(f"바람개비형 : {len(pinwheel_data)} → {pinwheel_output_path}")


# ============================
# 4. 실행부
# ============================

if __name__ == "__main__":
    input_json = "C:/Users/82106/OneDrive/바탕 화면/1/6_part_006_of_006.json"

    window_json = "C:/Users/82106/OneDrive/바탕 화면/1/window_6.json"
    pinwheel_json = "C:/Users/82106/OneDrive/바탕 화면/1/pinwheel_6.json"

    split_and_save_dataset(
        input_json,
        window_json,
        pinwheel_json
    )