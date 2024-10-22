import xxhash
from imagehash import average_hash, phash, phash_simple, dhash, dhash_vertical, whash, colorhash
from vishash.vishash import ImageSignature
from perception import hashers
import cv2
from PIL import Image
from cv2 import img_hash

POSSIBLE_CLIP_FOLDER_NAMES = ['clips', 'cuts', 'images', 'frames']
SUPPORTED_IMAGE_TYPES = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
SUPPORTED_VIDEO_TYPES = ['.mp4', '.avi', '.mov', '.mkv']

XXHASH = xxhash.xxh64
XXHASH_BYTES = XXHASH().digest_size

print(f"Bytes used by xxhash: {XXHASH_BYTES}")


tiny_clip_vars = {
    'minimal_opening_scene_seconds': 0.5,
    'minimal_closing_scene_seconds': 0.5,
    'repeated_episodes': 3,
    'last_video': None,
}


# HASH_METHODS = {
#     # 'imagehash_average_hash': lambda frame: str(average_hash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
#     'imagehash_phash': lambda frame: str(phash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
#     # 'imagehash_phash_simple': lambda frame: str(phash_simple(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
#     # 'imagehash_dhash': lambda frame: str(dhash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
#     # 'imagehash_dhash_vertical': lambda frame: str(dhash_vertical(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
#     # 'imagehash_whash': lambda frame: str(whash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
#     # 'imagehash_colorhash': lambda frame: str(colorhash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
#     # 'perception_phash': lambda frame: hashers.PHash().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
#     # 'perception_dhash': lambda frame: hashers.DHash().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
#     # 'perception_ahash': lambda frame: hashers.AverageHash().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
#     # 'perception_whash': lambda frame: hashers.WaveletHash().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
#     # 'perception_color_moment': lambda frame: hashers.ColorMoment().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
#     # 'perception_block_mean': lambda frame: hashers.BlockMean().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
#     # 'cv2_average_hash': lambda frame: img_hash.AverageHash_create().compute(frame).tostring(),
#     # 'cv2_block_mean_hash': lambda frame: img_hash.BlockMeanHash_create().compute(frame).tostring(),
#     # 'cv2_color_moment_hash': lambda frame: img_hash.ColorMomentHash_create().compute(frame).tostring(),
#     # 'cv2_marr_hildreth_hash': lambda frame: img_hash.MarrHildrethHash_create().compute(frame).tostring(),
#     # 'cv2_phash': lambda frame: img_hash.PHash_create().compute(frame).tostring(),
#     # 'cv2_radial_variance_hash': lambda frame: img_hash.RadialVarianceHash_create().compute(frame).tostring(),
#     # 'vishash': lambda frame: str(ImageSignature().generate_signature(frame).tostring()),  # Updated line
#     # 'xxhash': lambda frame: XXHASH(frame).hexdigest(),
# }