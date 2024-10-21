



main.py
    get_clips
    gui
    get_image_frames_for_cuts
    process_clips
    tv_shows

compile_test_videos.py
(just used to create a compiled video of regular footage and clips to cut). 



New System:

main.py
    find_seasons 
        (gets lists of seasons and videos per season)

    downsize_videos (optional)
        (Can have several downsizing methods)
        - lower resolution
        - md5
        - xxhash
    find_repetitive_clips

