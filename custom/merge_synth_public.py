from glob import glob
import os
import shutil

public_img_dir = "../../new_train"
public_img_dir = os.path.abspath(public_img_dir)

public_train_annotation_file = "../../train.txt"
public_synthentic_folder_dir = "output/new_train"
shutil.rmtree(public_synthentic_folder_dir, ignore_errors=True)
os.makedirs(public_synthentic_folder_dir, exist_ok=True)

# symlink the public images to the synthetic folder
for img_path in glob(public_img_dir + "/*"):
    img_name = img_path.split("/")[-1]
    os.symlink(img_path, public_synthentic_folder_dir + "/" + img_name)

# read the public train annotation file
with open(public_train_annotation_file, "r") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
with open("new_train_annotation.txt", "w") as f:
    for line in lines:
        line = line.replace(" ", "\t")
        img_name, label = line.split("\t")
        f.write(public_synthentic_folder_dir + "/" + img_name + "\t" + label + "\n")
open("synth_public_train.txt", "w").close()
os.system("cat new_train_annotation.txt >> synth_public_train.txt")
os.system("cat synthentic_annotations.txt >> synth_public_train.txt")
