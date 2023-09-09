import json
import os
from glob import glob

json_paths = glob('output/**/*.json')
annotations = []
for json_path in json_paths:
    with open(json_path) as f:
        data = json.load(f)
    augment_type = os.path.basename(os.path.dirname(json_path))
    for img_name, label in data['labels'].items():
        img_path = os.path.join('output', augment_type, img_name + '.jpg')
        annotations.append((img_path, label))

with open('synthentic_annotations.txt', 'w') as f:
    for img_path, label in annotations:
        f.write(f'{img_path}\t{label}\n')

