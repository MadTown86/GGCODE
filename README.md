# GGCODE

## Dependencies:
No additional dependencies outside of Python 3.11

## Purpose: 
GGCODE is a mini application that is meant to help CNC (Computer Numerical Control) Programmers / Setup Personnel alter their '.NC' files in a simple, intuitive manner instead of having to go through the code with tools such as Notepad or any other text editor.

## Value Proposition:
> This tool will ultimately save you time and time is money.

## Description:
This simple tool will allow the user to select a .NC (G-Code File), view it and select options to alter the file according to a set of options.

## Features:
-Renumber the N###'s (Line Numbers) to a custom start, increment, end.
-Remove N###'s everywhere except for tool changes
-Update Comments at Tool Changes and M00
-Alter WorkOffset (G54..G59 -> G154 P1...G154P99)
-Alter Tool Numbers
-Create 'Tool List' at Head of Program from altered tool data
-Alter standard G84 tapping routines from single peck with FEED/SPEED Ratio (RPM: IPM) to PECK(AMT) to Final Depth, using G95 (Feed Per Revolution): F(TAP PITCH)

## Gotchas:
1. To get GGCODE to recognize taps properly you need to have the word TAP or tap in a comment in the line before a tool change or the line of the tool change.
2. 
