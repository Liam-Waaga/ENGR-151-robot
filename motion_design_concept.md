
# This is the main design ideas for the motion subsystem

## Step 1, find out where we are
For this step, our main idea is to rotate (and potentially move) until we find the white edge.

## Step 2, find the first color
At which point we will move along it. Adjusting course occasionally to stay on the path. Once we find a color, if it is the correct first color, then we continue and do our dance, and go to the next color. If it is the wrong one, we turn around and find the right one.

## Step 3, get the rest of the colors
We will continue around the exterior of the track, finding the colors in the right order. Once we have gone to each and done the dance, we will procede to do the victory dance.

## Event loop
Each event loop we will do three things.
1. We will check sensors to find out what has changede since the last event cycle.
2. We will do calculations to figure out what we need to do next.
3. We will command the motors to move according to the new trajectory.
