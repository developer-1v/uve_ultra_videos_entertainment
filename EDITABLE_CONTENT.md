# The types of video clips that need rules (for cutting, or for keeping in the video):

This file is organized by: 
- TYPES
- RULES
- RULE CATEGORIES
- DECISION TREES

# TYPES:
- Opening Scene
- Closing Scene
- Commercial Break
    - opening
    - closing
- Repeated video sequences with different audio content. 
- Black scenes
- Flashbacks in general
- Ending Flashbacks / Ending Replays on opening of next video



# RULES:
- Opening Scene (delete):
    - Must appear in at least __ 3 (user-defined) videos.
    - Should appear within the first __ 5m (user-defined) of start of video.
    - Should be at least __ 15 seconds long (user-defined).

- Closing Scene (delete):
    - Must appear in at least __ 3 (user-defined) videos.
    - Should appear within the last __ 5m (user-defined) of the video.
    - Should be at least __ 15 seconds long (user-defined).

- Commercial Breaks (delete):
    - Must appear in at least __ 3 (user-defined) videos.

- Black Scenes (keep):
    (often meant for transitions or for dramatic effect. Also, would be very hard to dinstinguish and eliminate). 
    - Keep unless they are within a video sequence that must be deleted. 

- Repeated Video Sequences with different audio content (keep):
    (Anime will have the same clips of people talking, walking or whatever, in multiple videos, but have different audio
    These video scenes are short enough to be hard to notice without software).
    - Keep unless they are within a video sequence that must be deleted. 
    - Identification: it will:
        - Have different audio than the other matches. 

- Story Flashbacks (keep):
    - Keep unless they are within a video sequence that must be deleted. 
    - Identification: It will:
        - not be an opening or a closing scene, 
        - likely not be in multiple videos in a row (but spread out through the series).

- NOTE: Story Flashbacks and Repeated Video sequences with different audio are treated the same way in our software. 
    - We shouldn't take the time to distinguish these. 
    - We don't need to track the audio for the repeated video sequences with different audio. 
    - Most of these should be NOT CAUGHT by our software, because they will be spaced out enough. That is good. We don't
    have any benefit to catching these. 


- Ending Flashbacks on opening of next video: (DELETE):
    (Something like: The last minute(s) of the last video are either shown in their entirety
    at the beginning of the next video, or some parts of it are shown again. 
    We want to get rid of these because we literally just saw that scene using UVE and can ignore it
    so we can immediately get back into the story). 
    - Identification: It will:
        - be a frame sequence that was started in the last __ 5m (user-defined) of the previous video.
            (ignoring other sequences that have been deleted like the closing scene)
        - start within the first __ 5m (user-defined) of the current video. 
        - Shown up only 2 within the last __ 3 episodes (user-defined).


# RULE categories:
- length
- time location
- time location in comparison to the other reoccurence of this sequence
- number # of reocurrences
- not another identified scene type (opening/closing/commercial etc)


# 🌳 Decision Trees for frame sequences:

### 🤔 Did this identical sequence:
    - ✅ Show up in the last (3) episodes?
        - ✅ Yes:
            - Is it shorter than (15) seconds?
                - ✅ Yes:
                    - Commercial Break(s)
                        - Mark all for deletion.
                        - note the average time. 
                - ❌ No:
                    Does this appear within the first (5) minutes of the video?
                        - ✅ Yes:
                            - Opening Scene (delete)
                        - ❌ No:
                            Does this appear within the last (5) minutes of the video?
                                - ✅ Yes:
                                    - _Closing Scene_ (delete)

        - ❌ No:
            - Is the first of these sequences within the last (5) minutes of the last video, 
            and the one AFTER within the first (5) minutes of the start of the next video?
                - ✅ Yes:
                    - Ending Flashback on opening of next video (delete)


# Decision Tree as python if/else statements:
```py

first_sequence_within_last_5_minutes_of_last_video = False
next_sequence_within_first_5_minutes_of_current_video = False

# Updated logic with realistic variables and marking actions
if sequence_showed_up_in_last_3_episodes:
    if sequence_duration_seconds < 15:
        mark_commercial_breaks()
        note_average_time()
    elif sequence_start_time_minutes <= 5:
        mark_opening_scene()
    elif sequence_end_time_minutes >= 55:  # Assuming a 60-minute video
        mark_closing_scene()
elif first_sequence_within_last_5_minutes_of_last_video and next_sequence_within_first_5_minutes_of_current_video:
    mark_ending_flashback_on_opening_of_next_video()
else:
    mark_sequence_to_keep()


```
