import json
import math


def rotate_layout(layout, start_from):
    angle_map = {
        0: 270,
        1: 180,
        2: 0,
        3: 90
    }

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


def compute_box_per_level(limit, box_length, box_width):
    L = box_length
    W = box_width

    long_side = max(L, W)
    short_side = min(L, W)

    a = int((limit - long_side) // short_side) if limit >= long_side else 0

    return 4 * a


def generate_ring_coordinates(pallet_length, pallet_width,
                               box_length, box_width,
                               box_per_level):

    if box_per_level % 4 != 0:
        raise ValueError("박스 개수는 4의 배수여야 합니다.")

    if box_per_level == 0:
        raise ValueError("박스를 배치할 수 없습니다.")

    per_side = box_per_level // 4

    if box_length > box_width:
        side_total = box_length + box_width * per_side
    else:
        side_total = box_width + box_length * per_side

    half_side = side_total / 2

    if half_side > pallet_length / 2 or half_side > pallet_width / 2:
        raise ValueError("박스들이 팔렛트 범위를 초과합니다.")

    layout = []

    if box_length > box_width:

        x = -half_side + box_width / 2
        y = half_side - box_length / 2
        layout.append([round(x, 1), round(y, 1), 0])

        for _ in range(per_side - 1):
            x += box_width
            layout.append([round(x, 1), round(y, 1), 0])

        x = half_side - box_length / 2
        y = half_side - box_width / 2
        layout.append([round(x, 1), round(y, 1), 1])

        for _ in range(per_side - 1):
            y -= box_width
            layout.append([round(x, 1), round(y, 1), 1])

        x = -half_side + box_length / 2
        y = -half_side + box_width / 2 + box_width * (per_side - 1)
        layout.append([round(x, 1), round(y, 1), 1])

        for _ in range(per_side - 1):
            y -= box_width
            layout.append([round(x, 1), round(y, 1), 1])

        x = half_side - box_width / 2 - box_width * (per_side - 1)
        y = -half_side + box_length / 2
        layout.append([round(x, 1), round(y, 1), 0])

        for _ in range(per_side - 1):
            x += box_width
            layout.append([round(x, 1), round(y, 1), 0])

    else:

        x = -half_side + box_width / 2
        y = half_side - box_length / 2
        layout.append([round(x, 1), round(y, 1), 0])

        for _ in range(per_side - 1):
            y -= box_length
            layout.append([round(x, 1), round(y, 1), 0])

        x = -half_side + box_length / 2
        y = -half_side + box_width / 2
        layout.append([round(x, 1), round(y, 1), 1])

        for _ in range(per_side - 1):
            x += box_length
            layout.append([round(x, 1), round(y, 1), 1])

        x = half_side - box_length / 2 - box_length * (per_side - 1)
        y = half_side - box_width / 2
        layout.append([round(x, 1), round(y, 1), 1])

        for _ in range(per_side - 1):
            x += box_length
            layout.append([round(x, 1), round(y, 1), 1])

        x = half_side - box_width / 2
        y = -half_side + box_length / 2 + box_length * (per_side - 1)
        layout.append([round(x, 1), round(y, 1), 0])

        for _ in range(per_side - 1):
            y -= box_length
            layout.append([round(x, 1), round(y, 1), 0])

    odd = [[-y, -x, d] for x, y, d in layout]
    even = [[-y, -x, 1 - d] for x, y, d in odd]

    return [odd, even]


def predict(box_length, box_width, pallet_length=1100, pallet_width=1100, start_from=0):

    limit = min(pallet_length, pallet_width)

    box_per_level = compute_box_per_level(limit, box_length, box_width)

    full_input = [
        pallet_length,
        pallet_width,
        box_length,
        box_width,
        box_per_level,
        start_from
    ]

    odd, even = generate_ring_coordinates(
        pallet_length,
        pallet_width,
        box_length,
        box_width,
        box_per_level
    )

    odd = rotate_layout(odd, start_from)
    even = rotate_layout(even, start_from)

    return {
        "input": full_input,
        "output": [odd, even]
    }


if __name__ == "__main__":

    result = predict(
        box_length=605,
        box_width=395,
        pallet_length=1000,
        pallet_width=1200,
        start_from=0
    )

    print("{")
    print(f'  "input": {json.dumps(result["input"], separators=(",",":"))},')
    print(f'  "output": {json.dumps(result["output"], separators=(",",":"))}')
    print("}")