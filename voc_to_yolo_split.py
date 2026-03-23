import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path("raw_labels")
CLASS_MAP = {"signboard": 0}

def convert_box(img_w, img_h, xmin, ymin, xmax, ymax):
    x_center = ((xmin + xmax) / 2.0) / img_w
    y_center = ((ymin + ymax) / 2.0) / img_h
    width = (xmax - xmin) / img_w
    height = (ymax - ymin) / img_h
    return x_center, y_center, width, height

def process_xml(xml_path: Path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    if size is None:
        print(f"[스킵] size 없음: {xml_path}")
        return

    img_w = int(size.find("width").text)
    img_h = int(size.find("height").text)

    lines = []

    for obj in root.findall("object"):
        name = obj.find("name").text.strip()

        if name not in CLASS_MAP:
            print(f"[스킵] 알 수 없는 클래스 '{name}' in {xml_path.name}")
            continue

        class_id = CLASS_MAP[name]
        bndbox = obj.find("bndbox")
        if bndbox is None:
            continue

        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)

        # 좌표 보정
        xmin = max(0, min(xmin, img_w))
        xmax = max(0, min(xmax, img_w))
        ymin = max(0, min(ymin, img_h))
        ymax = max(0, min(ymax, img_h))

        if xmax <= xmin or ymax <= ymin:
            print(f"[스킵] 잘못된 bbox in {xml_path.name}")
            continue

        x_center, y_center, width, height = convert_box(
            img_w, img_h, xmin, ymin, xmax, ymax
        )

        lines.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        )

    txt_path = xml_path.with_suffix(".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    xml_files = list(ROOT.rglob("*.xml"))

    if not xml_files:
        print("XML 파일이 없습니다.")
        return

    print(f"총 XML 파일 수: {len(xml_files)}")

    for xml_file in xml_files:
        process_xml(xml_file)

    print("변환 완료")

if __name__ == "__main__":
    main()