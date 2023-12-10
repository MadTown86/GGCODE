# GGCODE

## Dependencies:
No additional dependencies outside of Python 3.11

## Purpose: 
GGCODE is a mini application that is meant to help CNC (Computer Numerical Control) Programmers / Setup Personnel alter their '.NC' files in a simple, intuitive manner instead of having to go through the code with tools such as Notepad or any other text editor.

## Value Proposition:
> This tool will ultimately save you time and time is money.

## Description:
This simple tool will allow the user to select a .NC (G-Code File), view it and make common alterations to the file before saving it.

## Features:
+ Renumber the N###'s (Line Numbers) to a custom start, increment, end.
+ Remove N###'s everywhere except for tool changes.
+ Update Tool Comments.
+ Alter WorkOffset (G54..G59 -> G154 P1...G154P99).
+ Alter Tool Numbers.
+ Create 'Tool List' at Head of Program from altered tool data.
+ Alter standard G84 tapping routines from single peck with FEED/SPEED Ratio (RPM: IPM) to PECK(AMT) to Final Depth, using G95 (Feed Per Revolution): F(TAP PITCH).
+ View panel to see results of changes

## Basic Instructions:
+ Open Program (Run ggcode_main.py in IDE) -> Focus/Click on 'FILE' Tab
+ Click 'Browse' and select a file
+ Click 'Initial Scan' and view pane populates
+ 'RENUMBER' Tab requires one to make a selection then click 'Send To File'
+ All other Tabs require one to accumulate a list of changes by making a selection/data entry and clicking 'Store Changes', click 'Send To File' when finished
+ View Output
+ Click 'Confirm' and save as a new file
+ ***CHECK IT THOROUGHLY BEFORE RUNNING ON A MACHINE!!!!****

## Gotchas:
1. To get GGCODE to recognize taps properly you need to have the word TAP or tap in tool change comment (same line as M6T## or line before M6T##).
2. You need to also include common tap callouts ('M6x1' / '1/2-13' / '1/4-20' / 'M2.5x.45' / etc.) for it to 'try' and recognize the thread pitch and update code to rigid peck tapping.
3. I haven't included all necessary exception handling that would prevent this tool from crashing if the .NC code file chosen isn't properly formated.
4. There is no 'back' button on the edits, so unfortunately you will either have to continue editing to get to a previous state (if possible) or just re-open the file and try again
5. Last main 'Gotcha' for now is the quirkiness of the 'Tool->' and '<-Tool' feature.  It doesn't align very well to make sure that the tool is placed in the same portion of the view each time.


