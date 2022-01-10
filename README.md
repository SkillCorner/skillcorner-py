# Python SkillCorner Client
## Goal
Skillcorner API retrieves football tracking data.

##Details
SkillcornerClient uses HTTPBasicAuth to authenticate to https://skillcorner.com domain. Username and password can be passed as attributes while creating SkillcornerClient instance or set as environment variables (SKC_USERNAME, SKC_PASSWORD) and read automatically by SkillcornerClient class.

Methods of SkillcornerClient are generated automatically using metaclass _MethodsGenerator. This metaclass, basing on pre-prepared dictionaries, freezes particular arguments which cannot be changed and generates proper method signature. 

## Project Structure
client.py - contains SkillcornerClient class and all methods allowing to interact with Skillcorner API.

example.py - contains examples of usage SkillcornerClient methods.

tests - contains mock-based, unit tests allowing to verify if Skillcorner API client works properly.

## Installation
Package can be installed using pip command: `pip install skillcorner`.

To install package with extra requirements for testing environment use: `pip install -e skillcorner[test]`.