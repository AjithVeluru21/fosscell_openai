we need to make a matrix squeezer thingy in code. basically you take a big grid of letters and start folding it like paper. the user passes a list of fold directions like left, up, right, down.
when you fold it left, the right side flips over onto the left side. if it’s an odd size, the middle column is the crease and stays still but the stuff passing over it mirrors to the other side.
here is the tricky part: letters pile up. every slot on the board is actually a pile of letters. when a pile flips onto another pile, the whole pile turns upside down because of the physical flip, then sits on top of the target pile.
also they interact:

• a vowel hitting a consonant zaps them both out of existence from the pile.

• two identical letters hitting each other fuse into a capitalized version.

at the very end, just show what the grid looks like from the top view. if a pile got completely wiped out, show a dashboard/underscore line.
write the function for this.
