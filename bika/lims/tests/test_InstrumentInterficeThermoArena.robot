*** Settings ***

Library         BuiltIn
Library         Selenium2Library  timeout=5  implicit_wait=0.2
Library         String
Resource        keywords.txt
Library         bika.lims.testing.Keywords
Resource        plone/app/robotframework/selenium.robot
Library         Remote  ${PLONEURL}/RobotRemote
Variables       plone/app/testing/interfaces.py
Variables       bika/lims/tests/variables.py

Suite Setup     Start browser
Suite Teardown  Close All Browsers

Library          DebugLibrary

*** Variables ***
${input_identifier} =  thermoscientific_arena_20XT

*** Test Cases ***
test 20XT RPR file
    [Documentation]  It just checks if there is any error in the importation process.
    Log in                              test_labmanager         test_labmanager
    Wait until page contains            You are now logged in
    ${PATH_TO_TEST} =         run keyword   resource_filename
    Import Instrument File    Thermo Scientific - Arena 20XT  ${PATH_TO_TEST}/files/ArenaRPR.csv  ${input_identifier}


*** Keywords ***

Import Instrument File
    [Documentation]  Select the instrument and file type.
    ...              Then import the file created by the instrument.
    [arguments]  ${instrument}  ${file}  ${input_identifier}

    Click Link                  Import
    Wait until page contains    Select a data interface
    Select from list            exim  ${instrument}
    Element Should Contain      ${input_identifier}_format  CSV
    Import AR Results Instrument File    ${file}  ${input_identifier}_file

Import AR Results Instrument File
    [Documentation]  Import the file from test files folder, and submit it.
    [arguments]                 ${file}
    ...                         ${input_identifier}
    Choose File                 ${input_identifier}  ${file}
    Click Button                Submit
    Wait until page contains    Log trace
