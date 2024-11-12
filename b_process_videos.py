import os
import sqlite3
from collections import defaultdict
from rich import print as rprint 
from rich.pretty import pprint
from print_tricks import pt
from tqdm import tqdm

from globals import SUPPORTED_VIDEO_TYPES
import b_find_seasons
from b_data_hashing import hash_video
import b_calculate_sequences

def save_hashes_to_db(frame_hashes, conflicting_frame_hashes, db_path='hashes.db'):
    """Save frame hashes and conflicting frame hashes to an SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS frame_hashes (
                        hash TEXT PRIMARY KEY,
                        data TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS conflicting_frame_hashes (
                        hash TEXT PRIMARY KEY,
                        data TEXT)''')
    
    # Insert or replace data
    for hash_key, data in frame_hashes.items():
        cursor.execute('REPLACE INTO frame_hashes (hash, data) VALUES (?, ?)', (hash_key, str(data)))
    
    for hash_key, data in conflicting_frame_hashes.items():
        cursor.execute('REPLACE INTO conflicting_frame_hashes (hash, data) VALUES (?, ?)', (hash_key, str(data)))
    
    conn.commit()
    conn.close()

def load_hashes_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ensure the table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS frame_hashes (
            hash TEXT PRIMARY KEY,
            data BLOB
        )
    ''')
    
    cursor.execute('SELECT hash, data FROM frame_hashes')
    rows = cursor.fetchall()
    
    frame_hashes = {row[0]: row[1] for row in rows}
    conflicting_frame_hashes = {}  # Adjust this based on your actual schema and needs
    
    conn.close()
    return frame_hashes, conflicting_frame_hashes

def process_videos(video_paths, use_disk=False, db_path='hashes.db'):
    frame_hashes = {}
    conflicting_frame_hashes = {}
    
    if use_disk:
        frame_hashes, conflicting_frame_hashes = load_hashes_from_db(db_path)
    
    # Process videos only if not using disk or if there are new videos to process
    if not use_disk or video_paths:
        for video in tqdm(video_paths, desc="Processing videos"):
            frame_hashes, conflicting_frame_hashes = hash_video(video, frame_hashes, conflicting_frame_hashes)
        
        if use_disk:
            save_hashes_to_db(frame_hashes, conflicting_frame_hashes, db_path)
    
    return frame_hashes, conflicting_frame_hashes

if __name__ == "__main__":
    frame_hashes = {}
    conflicting_frame_hashes = {}
    
    # Example data structure
    test_data_structure = {
        "category1": ["video1.mp4", "video2.mp4"],
        "category2": {
            "subcategory1": ["video3.mp4"],
            "subcategory2": ["video4.mp4", "video5.mp4"]
        }
    }
    
    # Process the data structure
    frame_hashes, conflicting_frame_hashes = process_videos(frame_hashes, conflicting_frame_hashes, test_data_structure, use_disk=True)
    # pt(frame_hashes, conflicting_frame_hashes)
    
    test_folder = os.path.join(os.getcwd(), "videos_for_testing", "compiled_tiny_videos_for_testing", "compiled")
    test_folder = fr'C:\Users\user\Downloads\_Tor\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\Season 01'
    test_files = b_find_seasons.find_videos_in_folder(test_folder)
    pt(test_files)
    
    frame_hashes, conflicting_frame_hashes = process_videos(frame_hashes, conflicting_frame_hashes, test_files, use_disk=True)
    pprint('frame_hashes:\n')
    pprint(frame_hashes)
    # pt(frame_hashes)
    pprint('conflicting_frame_hashes:\n')
    pprint(conflicting_frame_hashes)
    
    possible_conflicting_sequences = b_calculate_sequences.find_possible_sequences(conflicting_frame_hashes)
    pprint('possible_conflicting_sequences:\n')
    rprint(possible_conflicting_sequences)