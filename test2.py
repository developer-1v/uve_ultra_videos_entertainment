import os
import subprocess
import uuid

def create_chapter_file(input_file, output_file, start_time_ms, end_time_ms, duration_ms):
    # Generate unique identifiers for segments
    main_segment_uid = uuid.uuid4().hex
    skip_segment_uid = uuid.uuid4().hex

    # Metadata content with segmented linking
    chapter_file_content = f""";FFMETADATA1
[CHAPTER]
TIMEBASE=1/1000
START=0
END={start_time_ms}
title=Part 1
ChapterSegmentUID={main_segment_uid}

[CHAPTER]
TIMEBASE=1/1000
START={start_time_ms}
END={end_time_ms}
title=Skip
ChapterSegmentUID={skip_segment_uid}

[CHAPTER]
TIMEBASE=1/1000
START={end_time_ms}
END={duration_ms}
title=Part 2
ChapterSegmentUID={main_segment_uid}
"""

    chapter_file_path = os.path.splitext(output_file)[0] + '.ffmetadata'
    with open(chapter_file_path, 'w') as chapter_file:
        chapter_file.write(chapter_file_content)

    # Debug: Print the generated metadata content
    print("Generated ffmetadata content:")
    print(chapter_file_content)

    # Use FFmpeg to add chapters to the MKV file with segmented linking
    try:
        subprocess.run([
            'ffmpeg', '-i', input_file, '-i', chapter_file_path, '-map_metadata', '1', '-codec', 'copy', output_file
        ], check=True)
        print(f"Chapters added to MKV file: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

input_video = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\aa.mp4'
output_video = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\output.mkv'
# Example values for start, end, and duration in milliseconds
start_time_ms = 100  # Start time for the skip chapter
end_time_ms = 3800   # End time for the skip chapter
duration_ms = 4000   # Total duration of the video
create_chapter_file(input_video, output_video, start_time_ms, end_time_ms, duration_ms)