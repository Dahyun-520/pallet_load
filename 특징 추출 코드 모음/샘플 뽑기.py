import json
import random


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def sample_by_box_count(file_path,
                        output_path,
                        min_count=1,
                        max_count=36,
                        sample_size=40):   # 🔥 기본 100개로 수정

    # 1️⃣ 파일 로드
    all_data = load_json(file_path)

    print(f"전체 데이터 개수: {len(all_data)}")

    # 2️⃣ 박스 개수별 분류
    grouped = {i: [] for i in range(min_count, max_count + 4)}

    for item in all_data:
        box_count = item["input"][4]
        if min_count <= box_count <= max_count:
            grouped[box_count].append(item)

    # 3️⃣ 박스 개수별 샘플링
    final_data = []

    for box_count in range(min_count, max_count + 4):
        items = grouped[box_count]
        print(f"{box_count}개짜리 데이터 개수: {len(items)}")

        if len(items) >= sample_size:
            sampled = random.sample(items, sample_size)
        else:
            print(f"⚠ {box_count}개짜리 데이터가 {sample_size}개 미만입니다. 전부 사용합니다.")
            sampled = items

        final_data.extend(sampled)

    # 4️⃣ 저장
    save_json(final_data, output_path)

    print(f"\n최종 저장 데이터 개수: {len(final_data)}")
    print(f"저장 완료 → {output_path}")


# =========================
# 사용 예시
# =========================

file_path = "C:/Users/82106/OneDrive/바탕 화면/visualizer/1/바람개비,윈도우 구분/바람개비,윈도우 구분 파일/바람개비형/pinwheel_1.json"
output_file = "Pinwheel_sampled_4_8_12_40each.json"

sample_by_box_count(file_path, output_file)