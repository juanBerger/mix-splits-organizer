-- BUILD INSTRUCTIONS --
Uses pyinstaller

pyinstaller MixSplitsOrganizer.py --windowed --onefile

[Use the unix executable from this]


TO DO:
Make a .app with codesigning
Remember last opened directory


[GENERAL ASSUMPTIONS / TROUBLESHOOTING]:

    Stereo files always have some stereo file indicator in the presence of 5.1
    In the case where there is no stereo signature, FUL indicates TV/Stereo. Put another way, OLVs have to be named 'OLV'
    This means that if a group of files has no surround and no FUL and no OLV, it will fail (there is no other basis for determining if the files are TV or OLV)



