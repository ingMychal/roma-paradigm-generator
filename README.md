# Roma Paradigm Generator (RPG)

This tool generates Roma language paradigms based on input words. It works as an offline extension of [romskyslovnik.online](https://romskyslovnik.online/) and the current version supports noun paradigms generation.
Verbs will be added soon.
#### Disclaimer: The underlying data used in this project is not owned by the author, and only a limited sample is provided in the SRO.xml file for demonstration purposes. 


## Table of Contents

- [Dependencies](#dependencies)
- [Usage](#usage)
- [Building Executable](#building-executable)


## Dependencies
No additional external libraries or modules need to be installed to run this application.
If you wish to build an executable using build_script.py you need to install requirements.

```bash
pip install -r requirements.txt
```




## Usage
First visit [romskyslovnik.online](https://romskyslovnik.online/) and search for the word in Slovak, e.g. 'brat' (brother). Result 'phral' is a noun (podstatné meno) so it can be used in RPG.
![image](https://github.com/ingMychal/roma-paradigm-generator/assets/56002593/f7f69cb5-9b77-419b-b44d-712facc546b8)



Run the application:

```bash
python user_interface.py
```
Input 'phral' and select appropriate animacy, in this case it is animate (Životné):
![image](https://github.com/ingMychal/roma-paradigm-generator/assets/56002593/703ad31e-f655-48f9-ae34-487d9e14bbb3)




## Building Executable
To build a standalone executable run the build script:
```bash
python build_script.py
```
Locate the generated executable in the dist directory. 
Please note that the executable built using PyInstaller is platform-specific. This means:

- The executable built on **Windows** is intended for use on Windows operating systems.
- The executable built on **Unix-like systems (e.g., macOS, Linux)** is intended for use on those specific platforms.
