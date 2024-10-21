Hashing Methods:
- xxhash:
- ImageHash:
    - https://pypi.org/project/ImageHash/
    - https://github.com/JohannesBuchner/imagehash
- VisHash:
    - https://github.com/GoFigure-LANL/VisHash
    - pip install git+https://github.com/GoFigure-LANL/VisHash.git


FIND REPETITIVE CLIPS:
- Process first video, saving its frame images as dictionary keys, and the frame number as the value. 
- Process the next video, and compare the frames with the keys in the dictionary. 
- If a frame matches a key (previous video frame), then we start a new list of matching_frames_sequence_#.
    These aren't necessarily going to be removed, as they could just be flashbacks etc. They are just documented. 
- Once the matches end, we move on and look for new frames that might match the previous video's frames. 

NOTE: Ram usage:
<!-- - Only the last num_saved_videos (3) processed videos are kept in memory at once.  -->
- Hold the entire first video in memory, as a dict or hash
- The frames/keys/values of the first video are deleted after the second video is processed.
- I think we need a dual-direction dictionary to make this happen. 



Hash map must contain:
 - Key: 
    - The Frame's image data (low res, or hashed value, or full res, etc)
 - Value:
    - Tuple of:
        - Tuple of:
            - An int that identifies the video it was found in (processedvideo #1, 2 etc).
            - The frame number




User options for cutting:
- Automatic finding and cutting (default)
- Option to include the Opening credits, ending credits, etc (so it doesn't scan for those)
- User-inserted IMages for start frame image & 
    - End Frame image
    - Amount of frames after the start image.
    - Go to the end of the video after the start image.
    - User-inserted start image can be a "loose" image search. It's for things like the next episode previews
    in My Hero Academia that have the same image that says "preview" in Japanese letters, but there are different colors etc. 
- user-inserted video clips to be removed. 







SPEEDUP:
- We convert all frames to grayscale & make them down to a small small number. 
- Save that number as a dictionary key and the frame as the value (is there a more compact way of doing this?)
- When we look at the cut frames, we look for matching 

Solve: 

CUTTING THE CLIP TOO EARLY:

Option 1: - If we are getting the start/end image frames ourselves, then we can simply record the number of frames, and save that within the start_image title ('moviename_start_frame_132' = start frame then clip lasts 132 frames). 
    - Howver, this isn't dynamic, and doesn't allow a user to just input their 2 images for the same result. 

Option 2:
    - When we are looking for close matches, we record all of the close matches, and then sort them
    and choose the absolute closest match (instead of one that is "close enough" as it is
    currently doing). 
    - priority goes to the closest one, but if there are ties, then we pick the last one.  



GET RID OF THE PREVIEW AT THE END:
- Maybe the start of the preview has a specific image, always? 
    - maybe the preview is always the last thing, even if there is an extra's scene (are the extra's 
    always before the preview?)
    
- If start_frame also has some numbers afterwards, then this means it doesn't need an end frame, and we just to cut out those frames that it tells us to cut. 
- We can also label is as "final cut frame" to have the same effect.









- We should be able to specify if a particular cut can show up more than once. 
    (commercial transitions could happen multiple times, but an intro would only be once, so once that cut was found, we no longer have to look for it). 
- Specify roughly when the cut should show up.

- We copy/remember (and paste in a config file), the length of each video, the names of them, 
and the cuts that were found. 




- We have 2 distinct processes:
    1 - We mark & record (file) all of the positions of the cuts. This is regardless of movies.
        - the time to cut is Based on the opening frame of the entire episode. 
        Thus, whether the videos we obtain are off by differents amounts of seconds, it won't matter. 
    2 - We cut those out, and re-stitch the video together. 



Include Movies & OVA's???:
- If yes, then in Description for the video, we put where the movies/ova's start and end times so peeps can skip them if desired. 


One Cut vs. individual Episodes:
- One cut is cool, but is this viable as a video format?
- Might make more sense to do individual episodes on a playlist.
- Or each season as one video





Process for using clips instead of frames:
- We input the clips. 
    - App looks for a unique start frame: One that is easily identifiable as a unique frame.
    - Records amount of black screen time before unique start frame, if any (if processed from a clip video
    instead of images)
    - Checks to see if the final frame of the clip is a unique frame or black frame. 
    - If black, then backtracks to find the last unique frame and uses that final frame.
    - Records the black time after this final unique frame. 
    - We now have the 2 needed images (and black screen times) for the app to search, 
    for this particular cut. 



