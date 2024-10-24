

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from rich import print as rprint
from print_tricks import pt

def process_videos(main_videos, clips_main_folder, clips_mapping):
    # Process each main video
    for video_index, main_video_path in enumerate(main_videos):
        print(f"Processing video {video_index + 1}/4: {os.path.basename(main_video_path)}")
        
        # Load the main video
        main_clip = VideoFileClip(main_video_path)
        segments = []
        last_cut = 0
        
        # Sort clips by their insertion frame for this video
        current_video_clips = []
        for clip_info in clips_mapping:
            clip_path = clip_info[0]
            if video_index + 1 < len(clip_info):  # Check if this clip applies to current video
                frame_number = clip_info[video_index + 1]
                current_video_clips.append((frame_number, clip_path))
        
        current_video_clips.sort()  # Sort by frame number
        
        # Process each clip
        for frame_number, clip_path in current_video_clips:
            # Add segment from main video up to this point
            if frame_number > last_cut:
                segment = main_clip.subclip(last_cut/30, frame_number/30)  # Assuming 30fps
                segments.append(segment)
            
            # Add the clip
            clip_full_path = os.path.join(clips_main_folder, clip_path)
            insert_clip = VideoFileClip(clip_full_path)
            segments.append(insert_clip)
            
            last_cut = frame_number
        
        # Add remaining part of main video
        if last_cut < main_clip.duration * 30:
            segments.append(main_clip.subclip(last_cut/30))
        
        # Concatenate all segments
        final_video = concatenate_videoclips(segments)
        
        # Generate output path
        output_path = main_video_path.replace('.mkv', '_processed.mkv')
        final_video.write_videofile(output_path,
                                    codec='libx264',
                                    audio_codec='aac')

        # Clean up
        final_video.close()
        main_clip.close()
        for segment in segments:
            segment.close()



if __name__ == '__main__':
    main_videos_folder = 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\1_clips_to_build_vids\\'
    main_videos = [
        os.path.join(main_videos_folder, '_s01e01_40.mkv'),
        os.path.join(main_videos_folder, '_s01e02_40.mkv'),
        os.path.join(main_videos_folder, '_s01e03_40.mkv'),
        os.path.join(main_videos_folder, '_s01e04_40.mkv'),
    ]
    
    clips_main_folder = 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\1_clips_to_build_vids\\'
    clips_mapping = (
        ('main_opening_15.mkv',         1, 2, 3, 4),
        ('main_closing_15.mkv',         39, 38, 37, 36),
        ('black_scene_2.mkv',           6, 7, 8, 9),
        ('black_scene_5.mkv',           14, 15, 16, 17),
        ('commercial_start_5.mkv',      18, 19, 20, 21),
        ('commercial_stop_5.mkv',       23, 24, 25, 26),
        ('flashback_a_5.mkv',           9, 10, 11, 12),
        ('flashback_b_5.mkv',           33, 34, 35, 36),
        ('ending_flashback_a_5.mkv',    38, 39),
        # ('ending_flashback_b_5.mkv',    40, 41),
        )
    process_videos(main_videos, clips_main_folder, clips_mapping)
