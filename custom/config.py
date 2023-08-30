import inspect
import os
from pathlib import Path
import imgaug.augmenters as iaa

from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    NormPerspectiveTransformCfg,
    GeneratorCfg,
    FixedTextColorCfg,
    FixedPerspectiveTransformCfg,
)
from text_renderer.layout.same_line import SameLineLayout
from text_renderer.layout.extra_text_line import ExtraTextLineLayout
from text_renderer.effect.curve import Curve
from text_renderer.layout import SameLineLayout, ExtraTextLineLayout


CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
OUT_DIR = CURRENT_DIR / "output"
DATA_DIR = CURRENT_DIR
BG_DIR = DATA_DIR / "bg"
FONT_DIR = DATA_DIR / "fonts"
FONT_LIST_FILE = DATA_DIR / "font_list.txt"
SYNTH_WORDS = DATA_DIR / "synthentic_words.txt"

font_cfg = dict(
    font_dir=FONT_DIR,
    font_list_file=FONT_LIST_FILE,
    font_size=(25, 31),
)

perspective_transform = NormPerspectiveTransformCfg(20, 20, 1.5)


def base_cfg(
    name: str,
    corpus: None,
    corpus_effects=None,
    layout_effects=None,
    layout=None,
    gray=False,
    num_image=5,
):
    return GeneratorCfg(
        num_image=num_image,
        save_dir=OUT_DIR / name,
        render_cfg=RenderCfg(
            bg_dir=BG_DIR,
            perspective_transform=perspective_transform,
            gray=gray,
            layout_effects=layout_effects,
            layout=layout,
            corpus=corpus,
            corpus_effects=corpus_effects,
            height=-1,
            pre_load_bg_img=True,
        ),
    )


def compact_char_spacing_small(num_image):
    cfg = base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                text_paths=[SYNTH_WORDS],
                separator="\n",
                num_word=(1, 1),
                **font_cfg,
            ),
        ),
        num_image=num_image,
    )
    cfg.render_cfg.corpus.cfg.char_spacing = -0.2
    return cfg


def compact_char_spacing_large(num_image):
    cfg = base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                text_paths=[SYNTH_WORDS],
                separator="\n",
                num_word=(1, 1),
                **font_cfg,
            ),
        ),
        num_image=num_image,
    )
    cfg.render_cfg.corpus.cfg.char_spacing = 0.3
    return cfg


def curve(num_image):
    cfg = base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                text_paths=[SYNTH_WORDS],
                filter_by_chars=False,
                separator="\n",
                num_word=(1, 1),
                **font_cfg,
            ),
        ),
        num_image=num_image,
    )
    cfg.render_cfg.corpus_effects = Effects(
        [
            Padding(p=1, w_ratio=[0.2, 0.21], h_ratio=[0.7, 0.71], center=True),
            Curve(p=1, period=180, amplitude=(4, 5)),
        ]
    )
    return cfg


def dropout_horizontal(num_image):
    cfg = base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                text_paths=[SYNTH_WORDS],
                filter_by_chars=False,
                separator="\n",
                num_word=(1, 1),
                **font_cfg,
            ),
        ),
        num_image=num_image,
    )
    cfg.render_cfg.corpus_effects = Effects(
        DropoutHorizontal(p=1, num_line=2, thickness=1)
    )
    return cfg


def dropout_vertical(num_image):
    cfg = base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                text_paths=[SYNTH_WORDS],
                filter_by_chars=False,
                separator="\n",
                num_word=(1, 1),
                **font_cfg,
            ),
        ),
        num_image=num_image,
    )
    cfg.render_cfg.corpus_effects = Effects(
        DropoutVertical(p=1, num_line=8, thickness=1)
    )
    return cfg


def line(num_image):
    poses = [
        "top",
        "bottom",
        "left",
        "right",
        "top_left",
        "top_right",
        "bottom_left",
        "bottom_right",
        "horizontal_middle",
        "vertical_middle",
    ]
    cfgs = []
    for i, pos in enumerate(poses):
        pos_p = [0] * len(poses)
        pos_p[i] = 1
        cfg = base_cfg(
            f"{inspect.currentframe().f_code.co_name}_{pos}",
            corpus=WordCorpus(
                WordCorpusCfg(
                    text_paths=[SYNTH_WORDS],
                    filter_by_chars=False,
                    separator="\n",
                    num_word=(1, 1),
                    **font_cfg,
                ),
            ),
            gray=True,
            num_image=num_image,
        )
        cfg.render_cfg.corpus_effects = Effects(
            Line(p=1, thickness=(3, 4), line_pos_p=pos_p)
        )
        cfgs.append(cfg)
    return cfgs


def extra_text_line_layout(num_image):
    cfg = base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=[
            WordCorpus(
                WordCorpusCfg(
                    text_paths=[SYNTH_WORDS],
                    filter_by_chars=False,
                    separator="\n",
                    num_word=(1, 1),
                    **font_cfg,
                ),
            ),
            WordCorpus(
                WordCorpusCfg(
                    text_paths=[SYNTH_WORDS],
                    filter_by_chars=False,
                    separator="\n",
                    num_word=(1, 1),
                    **font_cfg,
                ),
            ),
        ],
        gray=True,
        num_image=num_image,
    )
    cfg.render_cfg.layout = ExtraTextLineLayout(bottom_prob=1.0)
    return cfg


num_images = {
    "curve": 20000,
    "compact_char_spacing_small": 30000,
    "compact_char_spacing_large": 30000,
    "dropout_horizontal": 50000,
    "dropout_vertical": 50000,
    "extra_text_line_layout": 100000,
    "line": 20000,
}
# num_images = {
#     "curve": 2,
#     "compact_char_spacing_small": 2,
#     "compact_char_spacing_large": 2,
#     "dropout_horizontal": 2,
#     "dropout_vertical": 2,
#     "extra_text_line_layout": 2,
#     "line": 2,
# }


configs = [
    curve(num_images["curve"]),
    compact_char_spacing_small(num_images["compact_char_spacing_small"]),
    compact_char_spacing_large(num_images["compact_char_spacing_large"]),
    dropout_horizontal(num_images["dropout_horizontal"]),
    dropout_vertical(num_images["dropout_vertical"]),
    extra_text_line_layout(num_images["extra_text_line_layout"]),
    *line(num_images["line"]),
]
