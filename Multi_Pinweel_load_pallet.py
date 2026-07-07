import json
import math


def rotate_layout(layout, start_from):
    angle_map = {0: 270, 1: 180, 2: 0, 3: 90}
    angle = angle_map.get(start_from, 0)
    rad = math.radians(angle)

    rotated = []
    for x, y, d in layout:
        new_x = x * math.cos(rad) - y * math.sin(rad)
        new_y = x * math.sin(rad) + y * math.cos(rad)

        new_d = (d + start_from) % 2
        if start_from in (0, 1):
            new_d = 1 - new_d

        rotated.append([round(new_x, 1), round(new_y, 1), new_d])

    return rotated


def compute_d_e(limit, box_length, box_width):
    best = 0
    best_d, best_e = 0, 0

    for d in range(2, int(limit // box_length) + 1):
        e = int((limit - box_length * d) // box_width)
        if e < 1:
            continue

        value = d * e
        if value > best:
            best = value
            best_d, best_e = d, e

    return best_d, best_e


def generate_de_pinwheel(limit, box_length, box_width):
    d, e = compute_d_e(limit, box_length, box_width)

    if d == 0 or e == 0:
        raise ValueError("배치 가능한 double pinwheel 패턴이 없습니다.")

    half = (d * box_length + e * box_width) / 2
    base = []

    for row in range(e):
        for col in range(d):
            x = -half + box_length / 2 + col * box_length
            y = half - box_width / 2 - row * box_width
            base.append((x, y))

    layout = []

    for x, y in base:
        layout.append((x, y, 0))

    for x, y in base:
        layout.append((y, -x, 1))

    for x, y in base:
        layout.append((-x, -y, 0))

    for x, y in base:
        layout.append((-y, x, 1))

    odd = [[round(x, 1), round(y, 1), direction] for x, y, direction in layout]
    even = [[-y, -x, 1 - direction] for x, y, direction in layout]

    return odd, even, d, e


def predict(box_length, box_width, pallet_length, pallet_width, start_from=0):

    limit = min(pallet_length, pallet_width)

    odd, even, d, e = generate_de_pinwheel(limit, box_length, box_width)

    odd = rotate_layout(odd, start_from)
    even = rotate_layout(even, start_from)

    return {
        "input": [
            pallet_length,
            pallet_width,
            box_length,
            box_width,
            d * e * 4,
            start_from
        ],
        "output": [odd, even],
    }


if __name__ == "__main__":
    
    pallet_length = 1200
    pallet_width = 1000

    box_length = 250
    box_width = 400

    start_from = 0

    result = predict(
        box_length,
        box_width,
        pallet_length,
        pallet_width,
        start_from
    )

    print("{")
    print(f'  "input": {json.dumps(result["input"], separators=(",", ":"))},')
    print(f'  "output": {json.dumps(result["output"], separators=(",", ":"))}')
    print("}")