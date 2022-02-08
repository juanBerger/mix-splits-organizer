# mix-splits-organizer
Organizes deliverables into folders for DAP


# Cmd line version
- Supply base path as argument



# Build Instrucions - Old UI Version
- pyinstaller MixSplitsOrganizer.py --windowed --onefile
- pip3 install pyinstaller if you need to
- Have to build on Catalina 10.15 or above to avoid logout issue
- Additionally have to add this hack before building (this assumes python 3.9 which needs to be from python.org):
    https://github.com/marcelotduarte/cx_Freeze/issues/849#issuecomment-826840046


# Some Assumptions
- Stereo files always have some stereo file indicator in the presence of 5.1
- In the case where there is no stereo signature, FUL indicates TV/Stereo. SO OLVs have to always have 'OLV'