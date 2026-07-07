import json
import math

def compute_box_per_level(pallet_length, pallet_width, box_length, box_width):
    L = box_length
    W = box_width

    x = int(pallet_length // L)
    y = int(pallet_width // W)

    return x * y


def rotate(x, y, angle):
    if angle == 0:
        return x, y
    elif angle == 90:
        return y, -x
    elif angle == -90:
        return -y, x
    elif angle == 180:
        return -x, -y
    else:
        raise ValueError("invalid angle")


def round5(v):
    if v == 0:
        return 0.0
    return round(v, 5)


def generate_window_coordinates(
    pallet_length,
    pallet_width,
    box_length,
    box_width,
    box_per_level,
    start_from
):

    L = box_length
    W = box_width

    xA = int(pallet_length // L)
    yA = int(pallet_width // W)
    areaA = xA * yA

    xB = int(pallet_length // W)
    yB = int(pallet_width // L)
    areaB = xB * yB

    use_B = areaB > areaA

    if not use_B:
        x = xA
        y = yA
        step_x = L
        step_y = W

        start_x = -L * x / 2 + L / 2
        start_y =  W * y / 2 - W / 2

        base_coords = []
        for r in range(y):
            for c in range(x):
                cx = start_x + c * step_x
                cy = start_y - r * step_y
                base_coords.append([cx, cy, 0])

    else:
        x = xB
        y = yB
        step_x = W
        step_y = L

        start_x = -W * x / 2 + W / 2
        start_y =  L * y / 2 - L / 2

        base_coords = []
        for r in range(y):
            for c in range(x):
                cx = start_x + c * step_x
                cy = start_y - r * step_y
                base_coords.append([cx, cy, 0])

    angle_map = {
        0: 90,
        1: 0,
        2: 180,
        3: -90
    }

    angle = angle_map.get(start_from, 0)

    rotated_coords = []

    for x, y, _ in base_coords:

        if use_B:
            x, y = rotate(y, x, 90)

        if start_from == 0:
            rx, ry = x, -y
        elif start_from == 3:
            rx, ry = -x, y
        else:
            rx, ry = rotate(x, y, angle)

        direction = 1 if use_B else 0
        if use_B:
            rotated_coords.append([round5(-rx), round5(ry), direction])
        else:
            rotated_coords.append([round5(-rx), round5(-ry), direction])

    return [rotated_coords, rotated_coords]


def predict(box_length, box_width, pallet_length, pallet_width, start_from=0):

    box_per_level = compute_box_per_level(
        pallet_length,
        pallet_width,
        box_length,
        box_width
    )

    full_input = [
        pallet_length,
        pallet_width,
        box_length,
        box_width,
        box_per_level,
        start_from
    ]

    output = generate_window_coordinates(
        pallet_length,
        pallet_width,
        box_length,
        box_width,
        box_per_level,
        start_from
    )

    return {
        "input": full_input,
        "output": output
    }


if __name__ == "__main__":

    box_length = 400
    box_width = 250

    pallet_length = 1200
    pallet_width = 1000
    start_from = 3

    result = predict(
        box_length,
        box_width,
        pallet_length,
        pallet_width,
        start_from
    )

    print("{")
    print(f'  "input": {json.dumps(result["input"], separators=(",",":"))},')
    print(f'  "output": {json.dumps(result["output"], separators=(",",":"))}')
    print("}")