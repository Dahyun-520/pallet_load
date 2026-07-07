import json
from collections import Counter

# =========================
# 설정: JSON 파일 경로
# =========================
JSON_FILE_PATH = "C:/Users/82106/OneDrive/바탕 화면/1/바람,윈도우 나눈거/window_1.json"   # ← 여기에 네 파일 경로 넣기


def analyze_box_count_distribution(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # input 구조:
    # [팔렛트 길이, 팔렛트 너비, 박스 길이, 박스 너비, 박스 개수, 시작 위치]
    box_counts = [item["input"][4] for item in data]

    counter = Counter(box_counts)

    total = len(box_counts)
    multiple_of_4 = sum(count for box, count in counter.items() if box % 4 == 0)
    not_multiple_of_4 = total - multiple_of_4

    print("================================")
    print("📦 박스 개수 분포 분석 결과")
    print("================================")
    print(f"전체 데이터 수            : {total}")
    print(f"4의 배수 박스 개수 데이터 : {multiple_of_4}")
    print(f"❌ 4의 배수 아님          : {not_multiple_of_4}")
    print("\n박스 개수별 분포:")

    for box_count in sorted(counter.keys()):
        count = counter[box_count]
        flag = "" if box_count % 4 == 0 else " ❌"
        print(f" - 박스 개수 {box_count:>3}개 : {count}개{flag}")

    print("\n요약:")
    summary = ", ".join(
        f"{box}개 {count}건"
        for box, count in sorted(counter.items())
    )
    print(summary)


# =========================
# 실행
# =========================
if __name__ == "__main__":
    analyze_box_count_distribution(JSON_FILE_PATH)