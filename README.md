# ISP_Diagnostics

Trying to make a simpler diagnostic program for users to download and run on their computer rather than typing commands into cmd or terminal and feeling very uncomfortable in the process.

It was a project I started in January of 2022, but stopped because making GUIs is HARD

The commands.py file holds the actual functional code of the program.
The plan was to import commands.py into a GUI script written in tkinter, but tkinter looks like trash.
So then I tried to move to pysciter, but the documentation for pysciter is awful and required me to write a whole front end in html, css, and javascript to then call the commands through an api, and it was MEH.

Once a GUI was made, I was going to use py2exe and py2app to compile the necessary code into an exe for Windows or a similar executable for MacOS.

At some point I'll take another crack at a front end, but for now it's on the back burner.