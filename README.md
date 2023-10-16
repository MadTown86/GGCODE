# mrp

Purpose: 
I have yet to find a GCode editing tool (free) that allows one to edit the GCode in an easy, intuitive and useful way.

Description:
This simple tool will allow the user to select a .NC (G-Code File), view it and select options to alter the file according to a set of options.

Options/Features:
Renumber the N###'s (Line Numbers) to a custom start, increment, end.
Remove N###'s everywhere except for tool changes
Update Comments at Tool Changes and M00
Alter WorkOffset (G54..G59 -> G154 P1...G154P99) Per Tool
Scan Tool Comments to update/alter data related to each tool and standardize tool comments (DIA, FLUTES, HELIXANGLE, OAL, LOC)
Create 'Tool List' at Head of Program from altered tool data
Alter standard G84 tapping routines from single peck with FEED/SPEED Ratio (RPM: IPM) to PECK(AMT) to Final Depth, using G95 (Feed Per Revolution): F(TAP PITCH)
