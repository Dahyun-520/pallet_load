import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATASET_PATH = BASE_DIR / "pattern_results.json"
DEFAULT_PNG_OUTPUT_DIR = BASE_DIR / "visualize_png"
VISUAL_RANGE = 650
KOREAN_FONT_CANDIDATES = [
    "Malgun Gothic",
    "AppleGothic",
    "NanumGothic",
    "Noto Sans CJK KR",
    "Noto Sans KR",
    "DejaVu Sans",
]


def configure_matplotlib_fonts():
    available_fonts = {font.name for font in font_manager.fontManager.ttflist}
    selected_fonts = [
        font_name for font_name in KOREAN_FONT_CANDIDATES if font_name in available_fonts
    ]
    if not selected_fonts:
        selected_fonts = ["DejaVu Sans"]

    plt.rcParams["font.family"] = selected_fonts
    plt.rcParams["axes.unicode_minus"] = False


configure_matplotlib_fonts()


def parse_input(sample):
    values = sample["input"]

    if isinstance(values, dict):
        pallet_length = float(values["pallet_length"])
        pallet_width = float(values["pallet_width"])
        box_length = float(values["box_length"])
        box_width = float(values["box_width"])
        start_from = int(values.get("start_from", 0))
    else:
        pallet_length, pallet_width, box_length, box_width = map(float, values[:4])
        start_from = int(values[5]) if len(values) >= 6 else 0

    return pallet_length, pallet_width, box_length, box_width, start_from


def extract_layers(sample):
    output = sample["output"]
    if isinstance(output, dict):
        return output.get("odd", []), output.get("even", [])
    return output[0], output[1]


def extract_box_per_level(sample, odd_count, even_count):
    counts = sample.get("output_count", {})
    total_count = counts.get("total")
    if total_count is None:
        total_count = odd_count + even_count

    return int(total_count) // 2


def make_title(sample, index, total):
    pallet_length, pallet_width, box_length, box_width, start_from = parse_input(sample)
    counts = sample.get("output_count", {})
    odd_layer, even_layer = extract_layers(sample)
    odd_count = int(counts.get("odd", len(odd_layer)))
    even_count = int(counts.get("even", len(even_layer)))
    box_per_level = extract_box_per_level(sample, odd_count, even_count)

    return "\n".join(
        [
            f"샘플 {index + 1}/{total} | 요청 {sample.get('request_index', index + 1)}",
            (
                f"패턴: {sample.get('selected_pattern_label', sample.get('selected_pattern', 'unknown'))} | "
                f"팔레트: {pallet_length} x {pallet_width} | "
                f"박스: {box_length} x {box_width} | "
                f"시작 방향: {start_from} | 층당 박스 수: {box_per_level} | "
            ),
        ]
    )


def ensure_output_dir(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)


def clear_existing_pngs(output_dir):
    for png_file in output_dir.glob("*.png"):
        png_file.unlink()


def build_sample_filename(sample, index):
    request_index = sample.get("request_index", index + 1)
    pattern_name = sample.get("selected_pattern", "pattern")
    _, _, _, _, start_from = parse_input(sample)
    return f"request_{request_index:03d}_{pattern_name}_start_{start_from}.png"


def setup_axes(fig, axes, sample, index, total):
    pallet_length, pallet_width, _, _, _ = parse_input(sample)
    fig.suptitle(make_title(sample, index, total), size=14)

    for ax, layer_name in zip(axes, ["ODD", "EVEN"]):
        ax.clear()

        if not ax.xaxis_inverted():
            ax.invert_xaxis()

        ax.plot([-VISUAL_RANGE, VISUAL_RANGE], [-VISUAL_RANGE, VISUAL_RANGE], lw=0)
        ax.grid(True, "major", ls="-.")
        ax.set_aspect(1)
        ax.set_box_aspect(1)
        ax.set_title(f"{layer_name} LAYER")

        ax.add_patch(
            Rectangle(
                (-pallet_width / 2, -pallet_length / 2),
                pallet_width,
                pallet_length,
                ec="#ee2222aa",
                fc="none",
                lw=3,
                zorder=10,
            )
        )


def draw_layer(ax, placements, box_length, box_width):
    for item_index, (x, y, orientation) in enumerate(placements, start=1):
        draw_width = box_width
        draw_length = box_length
        if int(orientation) == 1:
            draw_width = box_length
            draw_length = box_width

        ax.text(
            y,
            x,
            s=item_index,
            family="monospace",
            size=10,
            ha="center",
            va="center",
            zorder=7,
        )

        rect = Rectangle(
            (y - draw_width / 2, x - draw_length / 2),
            draw_width,
            draw_length,
            ec="#622c0f",
            fc="#e4a250",
            lw=1,
            zorder=5,
        )
        ax.add_patch(rect)


def render_sample(fig, axes, sample, index, total):
    _, _, box_length, box_width, _ = parse_input(sample)
    odd_layer, even_layer = extract_layers(sample)
    setup_axes(fig, axes, sample, index, total)
    draw_layer(axes[0], odd_layer, box_length, box_width)
    draw_layer(axes[1], even_layer, box_length, box_width)


def save_dataset_pngs(dataset, output_dir=DEFAULT_PNG_OUTPUT_DIR):
    if not isinstance(dataset, list) or not dataset:
        raise ValueError("PNG 저장용 데이터는 비어 있지 않은 리스트여야 합니다.")

    output_dir = Path(output_dir)
    ensure_output_dir(output_dir)
    clear_existing_pngs(output_dir)

    fig, axes = plt.subplots(1, 2, figsize=(12, 8))
    saved_paths = []

    for index, sample in enumerate(dataset):
        render_sample(fig, axes, sample, index, len(dataset))
        fig.tight_layout(rect=[0, 0.03, 1, 0.92])
        output_path = output_dir / build_sample_filename(sample, index)
        fig.savefig(output_path, dpi=150)
        saved_paths.append(output_path)

    plt.close(fig)
    return saved_paths


def load_dataset(path=DEFAULT_DATASET_PATH):
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    save_dataset_pngs(load_dataset())
