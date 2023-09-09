rm -rf output
cd ..
python3 main.py --config custom/config.py \
    --dataset img \
    --num_processes 2 \
    --log_period 10
cd custom
python create_annotation.py
python merge_synth_public.py