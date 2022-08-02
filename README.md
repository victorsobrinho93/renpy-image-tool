# Ren'py Image Creation Tool
Streamline your Ren'py VN development.<br>
RITC is a tool intended to shorten the time spent writing (or copy-pasting) image blocks in Ren'py, and everything else that comes with it.<br>
<strong>Currently compatible with Ren'py 8 and later versions of Ren'py 7 (Not exactly sure when it stopped being required to add the full file path).<br> Adding support for the older syntax soon.

# <strong>Current features</strong><br>
<strong>Scene preview:</strong> Fine-tune your image before output.<br>
<strong>Alternative timings</strong>: Create multiple, alternatively timed scenes at once based on the same frames.<br>
<strong>ConditionalSwitch</strong>: Easily create ConditionalSwitches off your new images.<br>
<strong>Sound effects</strong>: Insert sound effects directly into your animation loops, just select the file and set up the timing.</br>

# ReadMe
As of now this program has <strong>basic</strong> validation.</br>
I've done what I could to stop garbage from going in, then coming out, however not everything has a feedback.</br>
For now, make sure that the rict_script file is inside your "game" folder, and/or not moved to or from there until your work is done.</br>
(It's created at the directory of the first rpy file you selected and not recreated unless moved or renamed, or the settings.ini modified.)
For best results select a *.rpy from the 'game' folder as your first file, even if you have no intentions of modifying it.</br>
The same goes for audio files, (as of 1.3.0a) make sure to use distinct file names for every sound effect.
