import json
import math

def rotate_90(layout):
    return [[round(-y, 2), round(x, 2), 1 - d] for x, y, d in layout]

def apply_start_from(layout, start_from):

    if start_from == 0:
        return layout

    elif start_from == 1:
        return [[x, round(-y, 2), d] for x, y, d in layout]

    elif start_from == 2:
        return [[round(-x, 2), y, d] for x, y, d in layout]

    elif start_from == 3:
        return [[round(-x, 2), round(-y, 2), d] for x, y, d in layout]

    else:
        return layout


def solve_pattern(L, W, P_L, P_W):

    n1 = (P_L - L) // W
    m1 = P_W // W
    l1 = P_W // L
    count_A1 = int(m1 + n1 * l1)

    n2 = (P_L - W) // L
    m2 = P_W // L
    l2 = P_W // W
    count_A2 = int(m2 + n2 * l2)

    n3 = (P_W - L) // W
    m3 = P_L // W
    l3 = P_L // L
    count_B1 = int(m3 + n3 * l3)

    n4 = (P_W - W) // L
    m4 = P_L // L
    l4 = P_L // W
    count_B2 = int(m4 + n4 * l4)

    best = max([
        ("A1", count_A1, n1, m1, l1),
        ("A2", count_A2, n2, m2, l2),
        ("B1", count_B1, n3, m3, l3),
        ("B2", count_B2, n4, m4, l4),
    ], key=lambda x: x[1])

    pattern, _, n, m, l = best

    if pattern == "A1":
        base = build_A1(L, W, n, m, l, P_L, P_W)
        result = [[x, -y, d] for x, y, d in base]

    elif pattern == "A2":
        base = build_A2(L, W, n, m, l, P_L, P_W)
        result = [[x, -y, d] for x, y, d in base]

    elif pattern == "B1":
        base = build_B1(L, W, n, m, l, P_L, P_W)
        result = rotate_90(base)

    else:
        base = build_B2(L, W, n, m, l, P_L, P_W)
        result = rotate_90(base)

    return pattern, result


def build_A1(L, W, n, m, l, P_L, P_W):

    coords = []

    total_width = L + W * n
    xmin = -total_width / 2

    left_h = W * m
    window_h = L * l

    target_h = max(left_h, window_h)
    y_start = target_h / 2

    if window_h > left_h and m > 1:
        gap = (window_h - left_h) / (m - 1)
    else:
        gap = 0

    x_left = xmin + L / 2
    y = y_start - W / 2

    for i in range(int(m)):
        coords.append([round(x_left, 2), round(y, 2), 0])
        y -= (W + gap)

    start_x = xmin + L + W / 2
    start_y = (L * l) / 2 - L / 2

    for r in range(int(l)):
        for c in range(int(n)):
            x = start_x + c * W
            y = start_y - r * L
            coords.append([round(x, 2), round(y, 2), 1])

    return coords


def build_A2(L, W, n, m, l, P_L, P_W):

    coords = []

    total_width = W + L * n
    xmin = -total_width / 2

    left_h = L * m
    window_h = W * l

    target_h = max(left_h, window_h)
    y_start = target_h / 2

    if window_h > left_h and m > 1:
        gap = (window_h - left_h) / (m - 1)
    else:
        gap = 0

    x_left = xmin + W / 2
    y = y_start - L / 2

    for i in range(int(m)):
        coords.append([round(x_left, 2), round(y, 2), 1])
        y -= (L + gap)

    start_x = xmin + W + L / 2
    start_y = (W * l) / 2 - W / 2

    for r in range(int(l)):
        for c in range(int(n)):
            x = start_x + c * L
            y = start_y - r * W
            coords.append([round(x, 2), round(y, 2), 0])

    return coords


def build_B1(L, W, n, m, l, P_L, P_W):

    coords = []

    total_width = L + W * n
    xmin = -total_width / 2

    left_h = W * m
    window_h = L * l

    target_h = max(left_h, window_h)
    y_start = target_h / 2

    if window_h > left_h and m > 1:
        gap = (window_h - left_h) / (m - 1)
    else:
        gap = 0

    x_left = xmin + L / 2
    y = y_start - W / 2

    for i in range(int(m)):
        coords.append([round(x_left, 2), round(y, 2), 0])
        y -= (W + gap)

    start_x = xmin + L + W / 2
    start_y = (L * l) / 2 - L / 2

    for r in range(int(l)):
        for c in range(int(n)):
            x = start_x + c * W
            y = start_y - r * L
            coords.append([round(x, 2), round(y, 2), 1])

    return coords


def build_B2(L, W, n, m, l, P_L, P_W):

    coords = []

    total_width = W + L * n
    xmin = -total_width / 2

    left_h = L * m
    window_h = W * l

    target_h = max(left_h, window_h)
    y_start = target_h / 2

    if window_h > left_h and m > 1:
        gap = (window_h - left_h) / (m - 1)
    else:
        gap = 0

    x_left = xmin + W / 2
    y = y_start - L / 2

    for i in range(int(m)):
        coords.append([round(x_left, 2), round(y, 2), 1])
        y -= (L + gap)

    start_x = xmin + W + L / 2
    start_y = (W * l) / 2 - W / 2

    for r in range(int(l)):
        for c in range(int(n)):
            x = start_x + c * L
            y = start_y - r * W
            coords.append([round(x, 2), round(y, 2), 0])

    return coords


def predict(box_length, box_width, pallet_length, pallet_width, start_from=0):

    pattern, base = solve_pattern(
        box_length,
        box_width,
        pallet_length,
        pallet_width
    )

    rotated = apply_start_from(base, start_from)

    odd = [[round(-x, 2), round(-y, 2), d] for x, y, d in rotated]
    even = list(reversed(rotated))

    box_per_level = max(len(odd), len(even))

    return {
        "pattern": pattern,
        "input": [
            pallet_length,
            pallet_width,
            box_length,
            box_width,
            box_per_level,
            start_from
        ],
        "output": [odd, even]
    }



if __name__ == "__main__":

    pallet_x = 1100
    pallet_y = 1100

    box_l = 270
    box_w = 230

    start_from = 0

    result = predict(box_l, box_w, pallet_x, pallet_y, start_from)

    print("{")
    print(f'  "pattern": "{result.get("pattern", "UNKNOWN")}",')  # 🔥 추가
    print(f'  "input": {json.dumps(result["input"], separators=(",", ": "))},')
    print(f'  "output": {json.dumps(result["output"], separators=(",", ": "))}')
    print("}")