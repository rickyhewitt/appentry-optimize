#!/usr/bin/env python
## appentry-optimize [0.3.3]
##
## A program to optimize .desktop files in freedesktop.org compatible
## desktop environments (Gnome, KDE, Xfce).
##
## Requires: Python 3.x
##
## Licensed under the GNU GPL
## Programming by Ricky Hewitt - ricky@rickyhewitt.dev
##
## Changes in 0.3.3 (23/Dec/2024):
##  - Updated for python 3.x
##
## Changes in 0.3.2 (20/Dec/2024):
##  - Adopted MIT License
##  - Uploaded to github, added README.md
##
## Changes in 0.3.1 (22/Feb/2012):
##  - Added error handling for when KDE directory is not present
## 
## Changes in 0.3:
##  - Modified final report (now reports kB instead of bytes) and displays full original bytes.
##  - Checks to see if backup/ already exists before creating it.
##  - Multiple backups are now possible (rather than backup.tar.gz it will be backup[date-time].tar.gz)
##  - Added command line arguments. Use -b to enable backup, -h to display help and -v for increased verbosity.
##  - Verbosity by default is now decreased. Use the new option -v for increased verbosity.
##  - KDE 3.x and 4 support
##  - Only attempts to optimize .desktop files now.
##  - A check is now performed to help ensure a valid locale is given.
##
## rickyhewitt.dev
 
## Import
import os, sys
from time import strftime, gmtime
 
##########################
# User definable variables
# Do not forget to update the locale section.
 
# locale defines the locale you wish to KEEP in the optimization process. All other locales
# will be removed. If no locale is specified (or invalid), then it will remove ALL locales apart from the
# one with no locale specification. (example: en_GB, fr, ca)
locale = "en_GB"
 
# app_path defines where to look for the .desktop files used for the application menu
app_path = "/usr/share/applications/" # Don't forget ending forward slash (/)!

# Filename for the archive (backup-day-month-year_hour-minute-second.tar.gz)
filename_backup = "backup-" + strftime("%d-%m-%y_%H-%M-%S", gmtime()) + ".tar.gz"
##########################
 
class AppEntry:
    # Set any variables we might need..
    workingData = []
    workingNameLocale = []
         
    def CheckDir(self, path):
        """Search for the location of the .desktop files being used for the application menu."""
        if os.access(path, 1) == True:
            return 1
        else:
            return 0
             
    def ListFiles(self):
        """List all the .desktop files used in app_path"""
        try:
            freedesktop_listdir = os.listdir(app_path)
            try:
                kde_listdir = os.listdir(app_path + "kde/")
                kde4_listdir = os.listdir(app_path + "kde4/")
            except OSError:
                kde_listdir = []
                kde4_listdir = []
        except OSError:
            sys.exit(app_path + " was not found!")
        final_listdir = []
        x = 0
       
        # Modify the paths for kde files
        for i in kde_listdir:
            # Filter by *.desktop files.
            if i[len(i)-8:len(i)] == ".desktop":
                final_listdir.append("kde/" + i)
                x = x + 1

        # The same for kde4
        for i in kde4_listdir:
            if i[len(i)-8:len(i)] == ".desktop":
                final_listdir.append("kde4/" + i)
                x = x + 1

        # Finally for freedesktop/gnome/xfce, etc..
        for i in freedesktop_listdir:
            if i[len(i)-8:len(i)] == ".desktop":
                final_listdir.append(i)
                x = x + 1
 
        return final_listdir
         
    def Optimize(self, filename):
        """Perform the optimization routines in the preferred order (and additional stuff)"""
        self.OptimizeLocale(filename, "Comment")
        self.OptimizeLocale(filename, "GenericName")
        self.OptimizeLocale(filename, "Name")
         
    def OptimizeLocale(self, filename, field_type):
        """Remove all locales (Name=) except from the one specified.
        filename specified the filename we want to optimize (the .desktop file).."""
        # Strip of Name entries and leave only the locales we want to keep.
        file = open(filename, 'r')
        for line in file.readlines():
            if line.startswith(field_type+'=') or line.startswith(field_type+"["+locale+"]"):
                self.workingNameLocale.append(line[:-1])
        file.close()
                 
        # Now grab all other lines so we can save them to the new file with the newly created locale data.
        file = open(filename, 'r')
        for line in file.readlines():
            if not line.startswith(field_type):
                self.workingData.append(line[:-1])
        file.close()
         
        # Write the new file..
        file = open(filename, 'w')
        file.write(self.workingData.pop(0)+"\n")
        file.write(self.workingData.pop(0)+"\n")
        for i in self.workingNameLocale:
            file.write(i+"\n")
        for i in self.workingData:
            file.write(i+"\n")
        file.close()
         
        # Reset variables
        self.workingData = []
        self.workingNameLocale = []
             
 
def CheckRoot():
    """This function will check to see if the user is running under root priviledges"""
    if not os.geteuid()==0:
        sys.exit("\n  Please run as root!\n")
    else:
        return 1
         
def CreateBackup(mode_backup):
    """This function will create a backup and put it into a gziped tape archive."""
    if mode_backup == 1 and AppEntry().CheckDir(app_path):
        try:
            print("Attempting to create backup in "+app_path+" backup")
            os.chdir(app_path)

            # Create the backup directory if it does not exist.
            if AppEntry().CheckDir(app_path+"backup/") == 0:
                os.system("mkdir ./backup/")
            else:
                print("Backup directory already exists.. will continue to make backup.")
           
            # Archive the files and place into backup/backup[date-time].tar.gz
            os.system("tar -czf " + filename_backup + " ./*")
            os.system("mv ./" + filename_backup + " ./backup/" + filename_backup)
            print("Backup created in "+app_path+"backup/" + filename_backup)
            return 1
        except:
            print("Failed to create backup in CreateBackup()..")
            return 0
    else:
        print("Backup was disabled. Backup was not created.")
        return 1

def CheckLocale(locale):
    """This function checks to see if a valid locale has been given, and quit if otherwise."""
    # A list of default valid locales.
    valid_locales = ["af", "be", "bg", "bn", "br", "bs", "ca", "cs", "csb", "da", "de", "el", "eo", "es", "et", "eu", "fa", "fi", "fr",
             "fy", "ga", "gl", "he", "hi", "hr", "hu", "id", "is", "it", "ja", "ka", "kk", "km", "lb", "lt", "lv", "mk", "ms", "nb",
             "nds", "ne", "nl", "nn", "pa", "pl", "pt", "pt_BR", "ro", "ru", "rw", "se", "sk", "sl", "sr", "sv", "ta", "te", "tg", "th",
             "tr", "tt", "uk", "uz", "en_GB", "en_US"]

    for i in valid_locales:
        if i == locale:
            return 1
    else:
        print("Error!\nAn invalid locale was given. Locale \"" + locale + "\" was not found.")
        sys.exit(1)
     
def main():
    # Show starting messages and version information..
    print("xfce4-appentry-optimize")
     
    # Create instance of class AppEntry..
    AppEntryInstance = AppEntry()
    # Set some variables..
    filelist = []
    currentFile = ""
    FileOriginalSize = 0
    FileEndSize = 0
    TotalOriginalBytes = 0
    TotalSavedBytes = 0
    x = 0 # number of shortcuts (to work out how many have been optimized at end)

    # Default argument values
    mode_verbosity = 0
    mode_backup = 0

    # Check arguments
    for arg in sys.argv:
        if arg == "--enable-verbosity" or arg == "-v":
            mode_verbosity = 1
        if arg == "--enable-backup" or arg == "-b":
            mode_backup = 1
        if arg == "--help" or arg == "-h":
            print("Usage:")
            print("  --enable-verbosity, -v | Enable verbose mode for more output.")
            print("  --enable-backup, -b    | Enable backup.")
            print("  --help, -h             | Display help.\n")
            sys.exit(1)
     
    # Search for the location of the .desktop files..
    if CheckRoot() and CreateBackup(mode_backup) and CheckLocale(locale):
        for i in AppEntryInstance.ListFiles():
            # Create a list of files (with full path) to optimize..
            filelist.append(app_path+i)
            currentFile=filelist.pop(0)
            if mode_verbosity == 1:
                print("Optimizing \""+currentFile+"\":")
             
            # Deal with byte stat counting
            FileOriginalSize = os.path.getsize(currentFile)
            if mode_verbosity == 1:
                print("  Current size is: "+str(FileOriginalSize)+" bytes")
                             
            # Optimize
            if mode_verbosity == 1:
                print("  Optimizing locale data..")
            try:
                AppEntryInstance.Optimize(currentFile)
            except:
                "Could not optimize.. probably not a .desktop file."
             
            # Deal with byte stat counting
            FileEndSize = os.path.getsize(currentFile)
            FileSavedBytes = (FileOriginalSize-FileEndSize)
            if mode_verbosity == 1:
                print("  Bytes Saved: "+str(FileSavedBytes)+" bytes\n")
            TotalOriginalBytes = TotalOriginalBytes + FileOriginalSize
            TotalSavedBytes = (TotalSavedBytes+FileSavedBytes)
             
            # Reset and increment some variables..
            currentFile = ""
            x = x+1
       
        # Display final results
        print("\nRESULTS:\n  Saved a total of "+str(TotalSavedBytes/1000)+" kB from " + str(TotalOriginalBytes/1000) + " kB, across "+str(x)+" shortcuts.")
    else:
        sys.exit("Something went wrong!\n")
            
if __name__ == "__main__":
    main()
