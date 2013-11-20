rem
rem     Take all the images from this directory and build rescaled
rem     slim versions in the according folders below
rem
rem     NOTE: Icons must be square to start wth otherwise they will get streched
rem     (by removing the '!' and using only width or height image aspect ratio ca be kept) 
rem
mogrify -resize 40x40! -path ../../ *.png