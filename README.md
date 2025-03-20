
API Automated Tests  
------------  
This test repo contains automated tests for the star wars apis 'planets' endpoint https://swapi.dev/documentation#planets
  
Requirement  
-----------------------  
To run the automated tests, Python3.9 or above is needed:  
https://www.python.org/downloads/release  
  
Install  
-----------------------  
Clone the repo  

`git clone `
  
After cloning the repo, cd into it  

`cd `

Install dependencies  

`pip3 install -r requirements.txt`
  
Usage  
-----  
To run the tests in parallel, with certain mark, generate html report, rerun failed test and allow ipdb  

`pytest -n auto --dist=loadscope -m test_mark --html report.html --reruns 2 --reruns-delay 5 -s`
e.g. `pytest -n auto --dist=loadscope -m planets_api --html report.html --reruns 2 --reruns-delay 5 -s`

OR if you just want to run all the tests and see the results on cli simply run

e.g. `pytest -s`

Note: If you want an easily sharable html test report then run with `--self-contained-html`
  

File Structure  
----  
All the test files should be put within the `/test/{resource_name}`

  
Before Commit  
----  
We want to make sure the code is following good coding standard, please make sure no pylint issues  
  
    pylint $(git ls-files '*.py')  
