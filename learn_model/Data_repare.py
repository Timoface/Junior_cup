import os
import pandas as pd
import shutil

DATASET_PATH = "data"
OUTPUT_PATH = "yolo_dataset"
LABELS = {"signboard": 0}

def convert_annotations(csv_path, out_labels_folder):
    df = pd.read_csv(csv_path)
    os.makedirs(out_labels_folder, exist_ok=True)

    for filename in df['filename'].unique():
        img_w, img_h = df[df['filename'] == filename][['width', 'height']].values[0]
        objects = df[df['filename'] == filename][['class', 'xmin', 'ymin', 'xmax', 'ymax']]

        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(out_labels_folder, txt_filename)

        with open(txt_path, "w") as f:
            for _, row in objects.iterrows():
                cls, xmin, ymin, xmax, ymax = row['class'], row['xmin'], row['ymin'], row['xmax'], row['ymax']
                x_center = (xmin + xmax) / 2 / img_w
                y_center = (ymin + ymax) / 2 / img_h
                width = (xmax - xmin) / img_w
                height = (ymax - ymin) / img_h
                f.write(f"{LABELS[cls]} {x_center} {y_center} {width} {height}\n")

for split in ["train", "val", "test"]:
    csv_file = os.path.join(DATASET_PATH, split, f"{split}.csv")
    img_dir = os.path.join(DATASET_PATH, split)
    labels_dir = os.path.join(OUTPUT_PATH, "labels", split)
    images_dir = os.path.join(OUTPUT_PATH, "images", split)

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    convert_annotations(csv_file, labels_dir)

    for img_file in os.listdir(img_dir):
        if img_file.endswith((".jpg", ".png")):
            shutil.copy(os.path.join(img_dir, img_file), os.path.join(images_dir, img_file))

print("✅ Данные подготовлены!")