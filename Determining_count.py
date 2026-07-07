import math


###########################################
# 180도 회전
###########################################

def rotate_180(layout):
    return [[round(-x, 2), round(-y, 2), 1 - d] for x, y, d in layout]


###########################################
# 패턴 선택
###########################################

def get_max_pattern(box_length, box_width, pallet_L, pallet_W, return_debug=False):
    L = box_length
    W = box_width

    long_side = max(L, W)
    short_side = min(L, W)

    pallet_short = min(pallet_L, pallet_W)
    pallet_long = max(pallet_L, pallet_W)

    # -------------------------
    # 1. 바람개비형 (LIMIT → 짧은 pallet 기준)
    a = int((pallet_short - long_side) // short_side) if pallet_short >= long_side else 0
    pinwheel = 4 * a

    # -------------------------
    # 2. 윈도우형 (두 방향 비교)
    x1 = int(pallet_L // L)
    y1 = int(pallet_W // W)
    window_1 = x1 * y1

    x2 = int(pallet_W // L)
    y2 = int(pallet_L // W)
    window_2 = x2 * y2

    if window_1 >= window_2:
        max_window = window_1
        x, y = x1, y1
        window_type = "A"
    else:
        max_window = window_2
        x, y = x2, y2
        window_type = "B"

    # =========================
    # 3. 스플릿형 (4방향 비교로 수정)
    # =========================

    # -------------------------
    # A1 방향
    # -------------------------
    n1 = (pallet_L - L) // W if pallet_L >= L else 0
    m1 = pallet_W // W
    l1 = pallet_W // L
    split_a1 = m1 + l1 * n1

    # -------------------------
    # A2 방향
    # -------------------------
    n2 = (pallet_L - W) // L if pallet_L >= W else 0
    m2 = pallet_W // L
    l2 = pallet_W // W
    split_a2 = m2 + l2 * n2

    # -------------------------
    # B1 방향
    # -------------------------
    n3 = (pallet_W - L) // W if pallet_W >= L else 0
    m3 = pallet_L // W
    l3 = pallet_L // L
    split_b1 = m3 + l3 * n3

    # -------------------------
    # B2 방향
    # -------------------------
    n4 = (pallet_W - W) // L if pallet_W >= W else 0
    m4 = pallet_L // L
    l4 = pallet_L // W
    split_b2 = m4 + l4 * n4

    # -------------------------
    # 최적 선택
    # -------------------------
    splits = {
        "A1": split_a1,
        "A2": split_a2,
        "B1": split_b1,
        "B2": split_b2,
    }

    # split별 값 저장 (핵심 추가)
    split_data = {
        "A1": (n1, m1, l1),
        "A2": (n2, m2, l2),
        "B1": (n3, m3, l3),
        "B2": (n4, m4, l4),
    }

    split_type = max(splits, key=splits.get)
    split = splits[split_type]

    # -------------------------
    # 4. 다중 바람개비형 (pallet_L, pallet_W 기준 최적화)
    max_double = 0
    best_d, best_e = 0, 0

    pallet_short = min(pallet_L, pallet_W)

    max_d = int(pallet_short // L)

    for d in range(1, max_d + 1):
        remaining = pallet_short - L * d
        if remaining < 0:
            continue

        e = remaining // W
        if e < 1:
            continue

        val = d * e

        if val > max_double:
            max_double = val
            best_d, best_e = d, e

    double_pinwheel = int(max_double * 4)

    # -------------------------
    # 결과
    results = {
        "pinwheel": pinwheel,
        "window": max_window,
        "split": split,
        "double_pinwheel": double_pinwheel
    }

    max_count = max(results.values())
    candidates = [k for k, v in results.items() if v == max_count]

    # -------------------------
    # fail 조건들

    def fail_center_pinwheel():
        return a * short_side - long_side >= long_side

    def fail_center_double():
        return abs(best_d * L - best_e * W) >= long_side

    def fail_extra_window():
        if window_type == "A":
            return (pallet_L - x * L >= L and pallet_W - y * W >= W) or \
                   (pallet_L - x * L >= W and pallet_W - y * W >= L)
        else:
            return (pallet_W - x * L >= L and pallet_L - y * W >= W) or \
                   (pallet_W - x * L >= W and pallet_L - y * W >= L)

    def fail_extra_split():
        n, m, l = split_data[split_type]

        if split_type in ["A1", "A2"]:
            return (
                (pallet_L - (L + W * n) >= L and pallet_W - L * l >= W) or
                (pallet_L - (L + W * n) >= W and pallet_W - L * l >= L)
            )
        else:
            return (
                (pallet_W - (L + W * n) >= L and pallet_L - L * l >= W) or
                (pallet_W - (L + W * n) >= W and pallet_L - L * l >= L)
            )

    def fail_extra_pinwheel():
        remain = pallet_short - 4 * a
        return remain >= L or remain >= W

    def fail_extra_double():
        remain_L = pallet_L - L * best_d
        remain_W = pallet_W - W * best_e
        return remain_L >= L or remain_W >= W

    # -------------------------
    # 1순위 필터
    filtered = []
    for p in candidates:
        if p == "pinwheel" and fail_center_pinwheel():
            continue
        if p == "double_pinwheel" and fail_center_double():
            continue
        filtered.append(p)

    candidates = filtered if filtered else candidates

    # -------------------------
    # 2순위 필터
    filtered = []
    for p in candidates:
        if p == "window" and fail_extra_window():
            continue
        if p == "split" and fail_extra_split():
            continue
        if p == "pinwheel" and fail_extra_pinwheel():
            continue
        if p == "double_pinwheel" and fail_extra_double():
            continue
        filtered.append(p)

    if filtered:
        candidates = filtered

    # -------------------------
    # 점수 계산

    def ratio(p):
        if p == "window":
            w = x * L
            h = y * W

        elif p == "split":
            n, m, l = split_data[split_type]

            if split_type in ["A1", "A2"]:
                w = L + W * n
                h = L * l
            else:
                w = W + L * n
                h = W * l

        else:
            return 0

        return abs(w - h) / (max(w, h) + 1e-6)

    def area_loss(p):
        total = pallet_L * pallet_W

        if p == "window":
            loss = total - x * L * y * W

        elif p == "pinwheel":
            side = short_side * a + long_side
            loss = total - side * side

        elif p == "double_pinwheel":
            side = L * best_d + W * best_e
            loss = total - side * side

        elif p == "split":
            n, m, l = split_data[split_type]

            if split_type in ["A1", "A2"]:
                loss = total - W * n * L * l - max(W * m * L, L * L * l)
            else:
                loss = total - L * n * W * l - max(L * m * W, W * W * l)

        return loss / total

    def rot_rank(p):
        if p in ["pinwheel", "double_pinwheel"]:
            return 0
        elif p == "split":
            return 1
        else:
            return 2

    # -------------------------
    # debug
    debug = {}
    for name, count in results.items():
        debug[name] = {
            "count": count,
            "area_loss": area_loss(name),
            "ratio": ratio(name),
        }

    # -------------------------
    if len(candidates) == 1:
        if return_debug:
            return candidates[0], results, debug
        return candidates[0], results

    # -------------------------
    best_score = float("inf")
    best_list = []

    for p in candidates:
        score = 4.0 * ratio(p) + 1.5 * area_loss(p)

        if score < best_score:
            best_score = score
            best_list = [p]
        elif abs(score - best_score) < 1e-9:
            best_list.append(p)

    if len(best_list) > 1:
        best = min(best_list, key=rot_rank)
    else:
        best = best_list[0]

    if return_debug:
        return best, results, debug
    return best, results


# ==========================
# 실행
# ==========================

if __name__ == "__main__":
    box_length = float(input("박스 길이 입력: "))
    box_width = float(input("박스 너비 입력: "))
    pallet_L = float(input("팔렛트 길이 입력: "))
    pallet_W = float(input("팔렛트 너비 입력: "))

    best, values = get_max_pattern(box_length, box_width, pallet_L, pallet_W)

    print("\n📦 입력:")
    print(f"박스: {box_length} x {box_width}")
    print(f"팔렛트: {pallet_L} x {pallet_W}\n")

    print("📊 결과:")
    for k, v in values.items():
        print(f"{k}: {v}")

    print("\n🏆 최적 패턴:", best)