import os
from b_main import find_seasons
from print_tricks import pt

def mark_videos(series, possible_conflicting_sequences):
    pass

def test_marking_of_videos():
    test_full_vids = False
    if test_full_vids:
        series_path = fr'C:\Users\user\Downloads\_Tor\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\_vids_for_python_automatic_editing'
        db_path = 'hashes_full_vids.db'
    else:
        main_folder = 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\'
        # series_path = os.path.join(main_folder, 'compiled_tiny_videos_for_testing', 'compiled')
        series_path = os.path.join(main_folder, 'tiny_vids','3_complete_vids_to_test')

        db_path = 'hashes_tiny_vids.db'
        
    series = find_seasons(series_path)
    
    possible_conflicting_sequences = {
    'sequence 0': {
        '_s01e01_40.mp4': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        '_s01e02_40.mp4': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        '_s01e03_40.mp4': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        '_s01e04_40.mp4': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    },
    'sequence 1': {'_s01e01_40.mp4': [34, 35, 36, 37, 38, 39], '_s01e02_40.mp4': [21, 22, 23], '_s01e03_40.mp4': [22, 23, 24], '_s01e04_40.mp4': [23, 24]},
    'sequence 2': {'_s01e01_40.mp4': [25, 26, 27, 28, 29], '_s01e02_40.mp4': [35, 36, 37, 38, 39], '_s01e03_40.mp4': [36, 37, 38, 39, 40], '_s01e04_40.mp4': [37, 38, 39, 40, 41]},
    'sequence 3': {'_s01e01_40.mp4': [43, 44, 45, 46, 47], '_s01e02_40.mp4': [26, 27, 28, 29, 30], '_s01e03_40.mp4': [27, 28, 29, 30, 31], '_s01e04_40.mp4': [28, 29, 30, 31, 32]},
    'sequence 4': {'_s01e01_40.mp4': [52, 53, 54, 55, 56], '_s01e02_40.mp4': [43, 44, 45, 46, 47, 48], '_s01e03_40.mp4': [44, 45, 46, 47, 48], '_s01e04_40.mp4': [45, 46, 47, 48, 49]},
    'sequence 5': {'_s01e01_40.mp4': [65, 66, 67, 68, 69], '_s01e02_40.mp4': [53, 54, 55, 56, 57], '_s01e03_40.mp4': [53, 54, 55, 56, 57], '_s01e04_40.mp4': [54, 55, 56, 57, 58]},
    'sequence 6': {'_s01e01_40.mp4': [74, 75, 76, 77, 78], '_s01e02_40.mp4': [66, 67, 68, 69, 70], '_s01e03_40.mp4': [66, 67, 68, 69, 70], '_s01e04_40.mp4': [67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86]},
    'sequence 7': {'_s01e01_40.mp4': [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94], '_s01e02_40.mp4': [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91], '_s01e03_40.mp4': [90, 91, 92, 93, 94], '_s01e04_40.mp4': [90, 91, 92, 93, 94]},
    'sequence 8': {'_s01e03_40.mp4': [73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87]}
    }
    
    mark_videos(series, possible_conflicting_sequences)

if __name__ == "__main__":

    test_marking_of_videos()


'''
I would like to take the incoming dict, and use a library to create chapters that start and end at each one of these sequences in each one of these video. We flag the chapters as disabled. 

'''