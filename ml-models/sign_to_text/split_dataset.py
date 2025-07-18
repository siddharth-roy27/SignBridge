import os
import shutil
import random

# Source directory (original)
src_dir = 'data'  # current folder is ~/s/m/s/

# Destination
dst_dir = 'data_split'
train_dir = os.path.join(dst_dir, 'train')
val_dir = os.path.join(dst_dir, 'val')

# Create folders
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Get class folders A-Z, 1–9
classes = sorted([d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))])

split_ratio = 0.8  # 80% for training

for cls in classes:
    cls_path = os.path.join(src_dir, cls)
    files = [f for f in os.listdir(cls_path) if os.path.isfile(os.path.join(cls_path, f))]
    random.shuffle(files)

    split_index = int(len(files) * split_ratio)
    train_files = files[:split_index]
    val_files = files[split_index:]

    os.makedirs(os.path.join(train_dir, cls), exist_ok=True)
    os.makedirs(os.path.join(val_dir, cls), exist_ok=True)

    for f in train_files:
        shutil.copy(os.path.join(cls_path, f), os.path.join(train_dir, cls, f))

    for f in val_files:
        shutil.copy(os.path.join(cls_path, f), os.path.join(val_dir, cls, f))

print("✅ Done: Data split into 'data_split/train' and 'data_split/val'")
