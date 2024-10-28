import os
import unittest

import cv2
from cv2 import img_hash
from PIL import Image
from rich import print as rprint

from print_tricks import pt
pt.easy_imports('main.py')

from globals import SUPPORTED_IMAGE_TYPES, SUPPORTED_VIDEO_TYPES, XXHASH#, #HASH_METHODS
import b_find_seasons

from imagehash import average_hash, phash, phash_simple, dhash, dhash_vertical, whash, colorhash
from vishash.vishash import ImageSignature
from perception import hashers



def get_hash_function(method=None):
    """Return the hash function based on the specified method, or all methods if no method is specified."""
    HASH_METHODS = {
        # 'imagehash_average_hash': lambda frame: str(average_hash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
        # 'imagehash_phash': lambda frame: str(phash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
        # 'imagehash_phash_simple': lambda frame: str(phash_simple(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
        # 'imagehash_dhash': lambda frame: str(dhash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
        # 'imagehash_dhash_vertical': lambda frame: str(dhash_vertical(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
        # 'imagehash_whash': lambda frame: str(whash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
        # 'imagehash_colorhash': lambda frame: str(colorhash(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))),
        # 'perception_phash': lambda frame: hashers.PHash().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
        # 'perception_dhash': lambda frame: hashers.DHash().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
        # 'perception_ahash': lambda frame: hashers.AverageHash().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
        # 'perception_whash': lambda frame: hashers.WaveletHash().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
        # 'perception_color_moment': lambda frame: hashers.ColorMoment().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
        # 'perception_block_mean': lambda frame: hashers.BlockMean().compute(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))),
        # 'cv2_average_hash': lambda frame: img_hash.AverageHash_create().compute(frame).tostring(),
        # 'cv2_block_mean_hash': lambda frame: img_hash.BlockMeanHash_create().compute(frame).tostring(),
        # 'cv2_color_moment_hash': lambda frame: img_hash.ColorMomentHash_create().compute(frame).tostring(),
        # 'cv2_marr_hildreth_hash': lambda frame: img_hash.MarrHildrethHash_create().compute(frame).tostring(),
        # 'cv2_phash': lambda frame: img_hash.PHash_create().compute(frame).tostring(),
        # 'cv2_radial_variance_hash': lambda frame: img_hash.RadialVarianceHash_create().compute(frame).tostring(),
        # 'vishash': lambda frame: str(ImageSignature().generate_signature(frame).tostring()),  # Updated line
        'xxhash': lambda frame: XXHASH(frame).hexdigest(),
    }
    
    if method == 'any':
        ## Use the first method in the dictionary
        first_method = next(iter(HASH_METHODS))
        return HASH_METHODS[first_method]

    if method is None:
        return HASH_METHODS
    
    if method not in HASH_METHODS:
        raise ValueError(f"Unsupported hashing method: {method}")
    
    return HASH_METHODS[method]


def hash_frame(frame, hash_function):
    """Generate a hash for a single frame/image using the specified hash function."""
    return hash_function(frame)




def hash_video(video_path, frame_hashes=None, conflicting_frame_hashes=None, method='any'):
    """Generate hashes for each frame in a video using the specified method."""
    cap = cv2.VideoCapture(video_path)
    if conflicting_frame_hashes is None:
        conflicting_frame_hashes = {}
    if frame_hashes is None:
        frame_hashes = {}

    frame_number = 0
    hash_function = get_hash_function(method)
    movie_name = os.path.basename(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"End of video or frame {frame_number} could not be read.")
            break  # Exit the loop if the video ends or a frame cannot be read

        frame_hash = hash_frame(frame, hash_function)
        frame_hashes, conflicting_frame_hashes = process_frame_hash(
            frame_hash, frame_number, movie_name, frame_hashes, conflicting_frame_hashes)
        # if pt.r(51):
        #     rprint('frame_hashes:\n', frame_hashes)
        #     rprint('conflicting_frame_hashes:\n', conflicting_frame_hashes)
        #     pt.ex()
        
        frame_number += 1

    cap.release()
    
    sorted_conflicting_hashes = sort_conflicting_hashes(frame_hashes, conflicting_frame_hashes)
    
    return frame_hashes, sorted_conflicting_hashes

def sort_conflicting_hashes(frame_hashes, conflicting_frame_hashes):
    """Sort conflicting_frame_hashes to match the order of frame_hashes."""
    sorted_conflicting_hashes = {}
    
    for frame_hash in frame_hashes:
        if frame_hash in conflicting_frame_hashes:
            sorted_conflicting_hashes[frame_hash] = conflicting_frame_hashes[frame_hash]
    
    return sorted_conflicting_hashes


def process_frame_hash(frame_hash, frame_number, movie_name, frame_hashes, conflicting_frame_hashes):
    """Process the frame hash and update frame_hashes and conflicting_frame_hashes."""
    if frame_hash in frame_hashes:
        # Ensure the movie_name list is initialized
        if not isinstance(frame_hashes[frame_hash], dict):
            frame_hashes[frame_hash] = {}
        
        if movie_name not in frame_hashes[frame_hash]:
            frame_hashes[frame_hash][movie_name] = []
        
        # Add the current frame number to frame_hashes
        frame_hashes[frame_hash][movie_name].append(frame_number)

        # Check if there are multiple movies for this frame hash
        if len(frame_hashes[frame_hash]) > 1:
            # Directly copy the entry to conflicting_frame_hashes if a conflict is detected
            conflicting_frame_hashes[frame_hash] = frame_hashes[frame_hash].copy()
    else:
        frame_hashes[frame_hash] = {movie_name: [frame_number]}
    
    return frame_hashes, conflicting_frame_hashes

def hash_image(image_path, method='xxhash'):
    """Generate a hash for a single image using the specified method."""
    image = cv2.imread(image_path)
    return hash_frame(image, method)




class TestHashVideo(unittest.TestCase):
    def setUp(self):
        # Set up the test folder and files
        self.test_folder = os.path.join(os.getcwd(), "videos_for_testing", "compiled_tiny_videos_for_testing", "compiled")
        self.test_files = b_find_seasons.find_videos_in_folder(self.test_folder)
        self.video_path = self.test_files[1]

    def test_hash_methods(self):
        frame_hashes = {}
        conflicting_frame_hashes = {}
        
        ## get length of video
        cap = cv2.VideoCapture(self.video_path)
        video_frames_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        # Retrieve the hash methods dynamically
        hashed_detections = {}
        HASH_METHODS = get_hash_function().keys()
        pt(HASH_METHODS)
        

        for i, method in enumerate(HASH_METHODS):
            with self.subTest(method=method):
                pt(method)
                pt.t()
                frame_hashes, conflicting_frame_hashes = hash_video(self.video_path, frame_hashes, conflicting_frame_hashes, method=method)
                pt.t()
                hashed_detections[method] = video_frames_length - len(frame_hashes)
                # pt(hashed_detections[method], video_frames_length), len(frame_hashes)
                # rprint(frame_hashes)
                self.assertIsInstance(frame_hashes, dict)

        # pt(hashed_detections) ## organize this by the lowest number of hashed frames
        # pt(sorted(hashed_detections.items(), key=lambda x: x[1]))

        rprint('frame_hashes:\n', frame_hashes)
        rprint('conflicting_frame_hashes:\n', conflicting_frame_hashes)

if __name__ == '__main__':
    unittest.main()
