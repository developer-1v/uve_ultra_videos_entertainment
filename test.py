import os
import subprocess

def create_chapter_file(input_file, output_file):
    # Get the total number of frames in the video
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
         '-show_entries', 'stream=nb_read_frames', '-of', 'default=nokey=1:noprint_wrappers=1', input_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    total_frames = int(result.stdout)

    # Calculate the frame range to skip
    start_skip = total_frames // 2 - 44
    end_skip = total_frames // 2 + 44

    # Calculate the duration of each frame
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
         'stream=avg_frame_rate', '-of', 'default=nokey=1:noprint_wrappers=1', input_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    frame_rate = eval(result.stdout.decode().strip())
    frame_duration = 1 / frame_rate

    # Calculate the time to skip
    start_time = start_skip * frame_duration
    end_time = end_skip * frame_duration

    chapter_file_content = """;FFMETADATA1
[CHAPTER]
TIMEBASE=1/1000
START=0
END={start_time_ms}
title=Part 1

[CHAPTER]
TIMEBASE=1/1000
START={start_time_ms}
END={end_time_ms}
title=Skip

[CHAPTER]
TIMEBASE=1/1000
START={end_time_ms}
END={duration_ms}
title=Part 2""".format(
        start_time_ms=int(start_time * 1000),
        end_time_ms=int(end_time * 1000),
        duration_ms=int(total_frames * frame_duration * 1000)
    )

    chapter_file_path = os.path.splitext(output_file)[0] + '.ffmetadata'
    with open(chapter_file_path, 'w') as chapter_file:
        chapter_file.write(chapter_file_content)

    # Debug: Print the generated metadata content
    print("Generated ffmetadata content:")
    print(chapter_file_content)

    # Use FFmpeg to add chapters to the MKV file
    try:
        subprocess.run([
            'ffmpeg', '-i', input_file, '-i', chapter_file_path, '-map_metadata', '1', '-codec', 'copy', output_file
        ], check=True)
        print(f"Chapters added to MKV file: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

input_video = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\aa.mp4'
output_video = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\output.mkv'
create_chapter_file(input_video, output_video)