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
    - HOW ELSE can I distinguish these from the repeated video sequences with different audio, 
    or the story flashbacks?

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


- Ending Flashbacks on opening of next video: (DELETE all but first):
    (Something like: The last minute(s) of the last video are either shown in their entirety
    at the beginning of the next video, or some parts of it are shown again. 
    We want to get rid of these because we literally just saw that scene using UVE and can ignore it
    so we can immediately get back into the story). 
    - Identification: It will:
        - be a frame sequence that was started in the last __ 5m (user-defined) of the previous video.
            (ignoring other sequences that have been deleted like the closing scene)
        - start within the first __ 5m (user-defined) of the current video. 
        - Shown up only 2 within the last __ 3 episodes (user-defined).

- Multi Ending Flashbacks (DELETE all but first):
    - Same as above, but the flashbacks are often bits and pieces but the same sequence of frames
    can show up more than once in the second video. For example, they show up before the opening, 
    then show up again after the opening.
    - I must setup test videos to handle this, because I could see me accidentally overlooking one
    of these instances. 


# RULE categories:
- length
- time location
- time location in comparison to the other reoccurences of this sequence
- number of reocurrences
- not another identified scene type (opening/closing etc)


# 🌳 Decision Trees for frame sequences:

### 🤔 Did this identical sequence:
    - ✅ Show up in the last (3) episodes?
        - ✅ Yes:
            - Is it shorter than (15) seconds?
                - ✅ Yes:
                    - mark for possible commercial breaks
                        - If consistenly continues to show up in other episodes,
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

sequence_within_last_5_minutes_of_last_video = False
equence_within_first_5_minutes_of_current_video = False

# Updated logic with realistic variables and marking actions
if sequence_showed_up_in_last_3_episodes:
    if sequence_duration_seconds < (minimal_opening_scene_seconds or minimal_closing_scene_seconds):
        mark_possible_commercial_break()
            if sequence_shows_up_in_every_episode_so_far:
                mark_commercial_break()
    elif sequence_start_time_minutes <= 5:
        mark_opening_scene()
    elif sequence_end_time_minutes >= (video_duration_minutes - 5):
        mark_closing_scene()
elif sequence_within_last_5_minutes_of_last_video and sequence_within_first_5_minutes_of_current_video:
    ## list of sequences, all but the first one
    for sequence in list_of_this_sequence[1:]:
        mark_as_an_ending_flashback() ## we skip the first one because we don't want to delete it. 
else:
    mark_sequence_to_keep()

def mark_identified_scene_type(scene_type):
    ''' 
        - Mark this scene type
        - Record the start time / start frame
            - If this is a type with a known duration (opening/closing/commercial)
                - record the duration & number of frames (dependent on frame rate)

        For Future scene types:
            - We can quickly look for that specific scene start frame 
            by looking within a region close to the previous recorded start times
            and maybe the average of those start times, then look forward and backward 
            (maybe in two different threads?)

        Then we can shortcut practically all other processing for all other episodes:
            - Find the opening, closing, commercial breaks. 
            - look for any ending flashbacks that are close to the next opening. 
            - We are done!!! Should be able to skip the remainder of every episode! 
                - Meaning we don't have to process entire episodes if we can find those few items!


        False Duplicates:
            - If we get a false duplicates, and need to distinguish them to find the correct scenes, 
            we have another ruleset for that. 
            For example, we get more than one ending scene, then we pick the one that is the longest
            scene is that is going to be the correct one in this case (if two scenes are at end of show
            but one is longer than the other, we pick the longer one). 
            
def mark_sequence_to_keep():
    '''
        - Record the start time / start frame
        - We list these in our review section. 
        - The cuts we want to make are marked as cut (but user can change)
        - These ones are marked as keep (but user can change)
    '''


```




'''
CREATE NEW TEST VIDEOS:
I need to make:
(keep 65 frames per video)
 - 4 new test videos (40 frames each)
 - 2 flashbacks (4 frames each) (same as repeated video sequence)
 - 1 black scenes per video (2 frames)
 - 1 black scene per video (5 frames)
 = 65 frames per video to keep

(delete about 20 - 28 frames per video)
 - opening clip (5 frames)
 - closing clip (5 frames)
 - Commercial break opening (3 frames)
 - Commercial break closing (3 frames)
 - 1 ending flashback (4 frames)
     - At end of video 1,
     - at start of video 2, 
     - at end of video 3
     - Twice in video 4, before and after the opening scene
'''