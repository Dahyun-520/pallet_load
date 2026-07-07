import json

def check_odd_first_direction_all_zero(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("❌ JSON 최상위가 리스트가 아닙니다.")
            return

        all_zero = True
        errors = []

        # 🔥 JSON 전체 순회
        for data_idx, item in enumerate(data):

            if "output" not in item:
                print(f"❌ {data_idx}번째 데이터에 output 없음")
                continue

            output = item["output"]

            # 🔥 output의 odd index만 검사
            for i in range(len(output)):
                if i % 2 == 1:  # odd index

                    try:
                        first_direction = output[i][0][2]

                        if first_direction != 0:
                            all_zero = False
                            errors.append((data_idx, i, first_direction))

                    except Exception as e:
                        print(f"구조 에러 → data[{data_idx}] output[{i}] : {e}")

        print("===================================")

        if all_zero:
            print("✅ 모든 데이터의 output odd 첫 방향이 0입니다.")
        else:
            print("❌ 0이 아닌 값이 존재합니다.")
            print("총 개수:", len(errors))
            for d_idx, out_idx, direction in errors:
                print(f"data[{d_idx}] → output[{out_idx}] 시작 방향: {direction}")

    except Exception as e:
        print("파일 읽기 에러:", e)


file_path = r"C:/Users/82106/OneDrive/바탕 화면/visualizer/1/바람개비,윈도우 구분/바람개비,윈도우 구분 파일/윈도우형/window_1.json"

check_odd_first_direction_all_zero(file_path)