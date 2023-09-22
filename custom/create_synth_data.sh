rm -rf output
python3 create_simple_words.py
cd ..
python3 main.py --config custom/config.py \
    --dataset img \
    --num_processes 16 \
    --log_period 10
cd custom
python3 create_annotation.py
python3 merge_synth_public.py