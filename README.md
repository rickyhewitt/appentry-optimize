appentry-optimize [0.3.3]

A tool for removing unused language data in freedesktop.org compatible environments (Xfce, Gnome, KDE, others). 

Created by Ricky Hewitt <ricky@rickyhewitt.dev>

Requires: Python 3.x

License: MIT License

Changes in 0.3.3 (23/Dec/2024):
  - Updated for python 3.x
    
Changes in 0.3.2 (20/12/2024):
  - Adopted MIT License
  - Uploaded to github, added README.md

Changes in 0.3.1 (22/Feb/2012):
  - Added error handling for when KDE directory is not present
 
Changes in 0.3:
  - Modified final report (now reports kB instead of bytes) and displays full original bytes.
  - Checks to see if backup/ already exists before creating it.
  - Multiple backups are now possible (rather than backup.tar.gz it will be backup[date-time].tar.gz)
  - Added command line arguments. Use -b to enable backup, -h to display help and -v for increased verbosity.
  - Verbosity by default is now decreased. Use the new option -v for increased verbosity.
  - KDE 3.x and 4 support
  - Only attempts to optimize .desktop files now.
  - A check is now performed to help ensure a valid locale is given.
