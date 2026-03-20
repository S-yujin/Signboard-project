import os
import random
import shutil
from pathlib import Path

# 원본 폴더
RAW_IMAGES = Path("raw_images")
RAW_LABELS = Path("raw_labels")

# 출력 폴더
OUT_ROOT = Path("dataset")

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def make_dirs():
    for split in ["train", "val", "test"]:
        (OUT_ROOT / "images" / split).mkdir(parents=True, exist_ok=True)
        (OUT_ROOT / "labels" / split).mkdir(parents=True, exist_ok=True)

def collect_image_files():
    files = []
    for p in RAW_IMAGES.iterdir():
        if p.suffix.lower() in IMAGE_EXTS:
            files.append(p)
    return sorted(files)

def copy_pair(img_path: Path, split: str):
    label_path = RAW_LABELS / f"{img_path.stem}.txt"

    dst_img = OUT_ROOT / "images" / split / img_path.name
    shutil.copy2(img_path, dst_img)

    # 라벨 없으면 빈 파일 생성
    dst_label = OUT_ROOT / "labels" / split / f"{img_path.stem}.txt"
    if label_path.exists():
        shutil.copy2(label_path, dst_label)
    else:
        dst_label.touch()

def main():
    random.seed(42)
    make_dirs()

    image_files = collect_image_files()
    random.shuffle(image_files)

    total = len(image_files)
    n_train = int(total * TRAIN_RATIO)
    n_val = int(total * VAL_RATIO)
    n_test = total - n_train - n_val

    train_files = image_files[:n_train]
    val_files = image_files[n_train:n_train + n_val]
    test_files = image_files[n_train + n_val:]

    for f in train_files:
        copy_pair(f, "train")
    for f in val_files:
        copy_pair(f, "val")
    for f in test_files:
        copy_pair(f, "test")

    print(f"전체: {total}")
    print(f"train: {len(train_files)}")
    print(f"val:   {len(val_files)}")
    print(f"test:  {len(test_files)}")

if __name__ == "__main__":
    main()