rem
rem     Take all the images from this directory and build rescaled
rem     slim versions in the according folders below
rem
rem     NOTE: Icons must be square to start with otherwise they will get streched
rem     (by removing the '!' and using only width or height image aspect ratio ca be kept) 
rem
mogrify -resize 44x44! -path 44 *.png
mogrify -resize 57x57! -path 57 *.png
