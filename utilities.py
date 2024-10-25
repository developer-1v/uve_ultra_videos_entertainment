import cv2
import matplotlib.pyplot as plt
import sqlite3
from rich import print as rprint
import json


def extract_frame(video_path, frame_number, output_image_path=None, display=False):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    # Check if the video was opened successfully
    if not video_capture.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    # Set the frame position
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read the frame
    success, frame = video_capture.read()
    
    if success:
        if display:
            # Convert BGR to RGB for matplotlib
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Display the frame using matplotlib
            plt.imshow(frame_rgb)
            plt.title(f"Frame {frame_number}")
            plt.axis('off')  # Hide axes
            plt.show()
        elif output_image_path:
            # Save the frame as an image
            cv2.imwrite(output_image_path, frame)
            print(f"Frame {frame_number} saved as {output_image_path}")
    else:
        print(f"Error: Could not read frame {frame_number}")
    
    # Release the video capture object
    video_capture.release()


import sqlite3
import json

def add_to_hashes_db(possible_conflicting_sequences, hashes_db_path):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(hashes_db_path)
    cursor = conn.cursor()
    
    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS possible_conflicting_sequences (
            sequence_id TEXT NOT NULL,
            file_name TEXT NOT NULL,
            numbers TEXT NOT NULL
        )
    ''')
    
    # Insert each sequence into the database
    for sequence_id, files in possible_conflicting_sequences.items():
        for file_name, numbers in files.items():
            # Convert the list of numbers to a JSON string
            numbers_str = json.dumps(numbers)
            cursor.execute('INSERT INTO possible_conflicting_sequences (sequence_id, file_name, numbers) VALUES (?, ?, ?)', 
                           (sequence_id, file_name, numbers_str))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()



def test_add_to_hashes_db():
    possible_conflicting_sequences = {
        'sequence 0': {'tiny_compiled_15a_normal.mkv': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], 
                    'tiny_compiled_15b_reverse.mkv': [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43]},
        'sequence 1': {'tiny_compiled_15a_normal.mkv': [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40], 
                    'tiny_compiled_15b_reverse.mkv': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]}
    }

    add_to_hashes_db(possible_conflicting_sequences, 'hashes.db')


def test_extract_frame():
    video_path = ''
    video_path = "C:\\Users\\user\\Downloads\\_Tor\\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\\_vids_for_python_automatic_editing\\[Sokudo] Boku no Hero Academia S01E01 [1080p BD][AV1][dual audio].mkv"
    video_path = "C:\\Users\\user\\Downloads\\_Tor\\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\\_vids_for_python_automatic_editing\\[Sokudo] Boku no Hero Academia S01E02 [1080p BD][AV1][dual audio].mkv"
    # video_path = "C:\\Users\\user\\Downloads\\_Tor\\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\\_vids_for_python_automatic_editing\\[Sokudo] Boku no Hero Academia S01E03 [1080p BD][AV1][dual audio].mkv"
    frame_number = 19051  # Change this to the frame number you want to extract
    output_image_path = f'{frame_number}.jpg'
    display = True
    # Set display to True to show the frame in a window
    extract_frame(video_path, frame_number, output_image_path, display=display)


def get_video_properties(video_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    # Check if the video was opened successfully
    if not video_capture.isOpened():
        print(f"Error: Could not open video {video_path}")
        return None
    
    # Retrieve properties
    num_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    framerate = video_capture.get(cv2.CAP_PROP_FPS)
    length_of_video = num_frames / framerate
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Release the video capture object
    video_capture.release()
    
    # Return the properties as a dictionary
    return {
        'Number of Frames': num_frames,
        'Framerate': framerate,
        'Length of Video (seconds)': length_of_video,
        'Resolution': f"{width}x{height}"
    }


if __name__ == "__main__":
    import os
    
    # List of directories to check for video files
    video_directories = [
        'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\0_simple_vids',
        # 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\1_clips_to_build_vids',
        'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\2_desired_output_vids',
        'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\3_complete_vids_to_test',
        # 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\4_clips_to_remove',
        # 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\5_clips_to_keep',
        'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\6_final_uve_edited_vids',
        # Add more directories as needed
    ]
    video_extensions = ('.mkv', '.mp4', '.avi')  # Add or remove extensions as needed
    
    # Iterate over each directory in the list
    for video_directory in video_directories:
        # List all files in the directory and filter for video files
        videos_to_check = [os.path.join(video_directory, f) for f in os.listdir(video_directory) if f.endswith(video_extensions)]
        
        for vid in videos_to_check:
            # Extract just the file name from the full path
            file_name = os.path.basename(vid)
            print(file_name, ' ', get_video_properties(vid))