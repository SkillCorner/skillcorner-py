# Python SkillCorner Client
## Goal
Skillcorner API retrieves football tracking data.

## Details
SkillcornerClient uses HTTPBasicAuth to authenticate to https://skillcorner.com domain. Username and password 
can be passed as attributes while creating SkillcornerClient instance or set as environment variables 
(SKC_USERNAME, SKC_PASSWORD) and read automatically by SkillcornerClient class.

Methods of SkillcornerClient are generated automatically using metaclass _MethodsGenerator. This metaclass, 
basing on pre-prepared dictionaries, freezes particular arguments which cannot be changed and generates 
proper method signature. 

## Project Structure
client.py - contains SkillcornerClient class and all methods allowing to interact with Skillcorner API.

example.py - contains examples of usage SkillcornerClient methods.

tests - contains mock-based, unit tests allowing to verify if Skillcorner API client works properly.

## Installation
Package can be installed using pip command: `pip install skillcorner`.

To install package with extra requirements for testing environment use: `pip install -e skillcorner[test]`.

To install package with extra requirements for physical visualisation in pandasgui use:
`pip install -e skillcorner[physical_visualisation]`. To use this library make sure that all needed dependencies are 
installed in your environment (mainly tested with Ubuntu): 

`apt-get install libglib2.0-0 ffmpeg libsm6 libxext6 libnss3 libxcursor-dev libxcomposite-dev libxdamage-dev libxrandr-dev libxtst-dev libxss-dev libdbus-1-dev libevent-dev libfontconfig1-dev libxcb-xinerama0 libxcb-xkb-dev libxcb-render-util0 libxcb-keysyms1 libxcb-image0 libxkbcommon-x11-0 libxcb-icccm4`

If you are on Debian you may also need to run: 

`ln -s /usr/lib/x86_64-linux-gnu/libxcb-util.so.0 /usr/lib/x86_64-linux-gnu/libxcb-util.so.1`
