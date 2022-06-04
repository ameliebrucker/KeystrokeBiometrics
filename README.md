# Keystroke Biometrics

## Description

This software captures typing behaviour. Free texts and fixed texts (depending on a template text) can be submitted as samples. The application offers the possibility to statistically evaluate several entries in relation to each other by using euklidean distance and to present the results to the user via diagrams.

## Installation

Please install python version 3.10.2 or upwards. You can start the software by executing the module keystroke_biometrics or the contained \__main__.py file via python.

Please note that correct functionality cannot be guaranteed with a Python version < 3.10.2, even if the application starts. For this purpose, it may be necessary to specify the exact version when starting the software (e.g. by entering "python3.10 keystroke_biometrics" as command) if it is not set as default.

__Stand Alone Application on Windows:__
In the directory "dist" you can find the subfolder "KeystrokeBiometrics_Windows", which contains a Windows executable file with the same name. Using this file to run the software does not require a python installation. The Windows application was created with the PyInstaller module. 

## Usage

### Submitting samples (relevant for study participants)

__Samles with free text:__
Click on "recording samples (free text)" in the navigation bar. Enter a text in the input field, your keystrokes will be recorded. Finish the input with the enter key. The "recording results" page is now displayed. You can discard or save your sample. You will then automatically return to the recording page.

__Samples with fixed text:__
Samples with fixed text are based on a given template text from which they may not deviate. Click on "Recording samples (fixed text)" in the navigation bar. Enter the template text in the text field. Finish the input with the enter key or a click on "Set template text". You can now enter the sample in the input field, your keystrokes will be recorded. Note that the entered text must match the template text, otherwise the text will be deleted. Finish the input with the enter key. The "recording results" page is now displayed. You can discard or save your sample. You will then automatically return to the recording page. It is possible to set a new template text by clicking on the button "Change template text".

Tip: Prefer short texts over long ones to avoid typing errors.

### Carrying out the verification process (relevant for persons conducting a study)

__Collecting several samples:__
Samples can be submitted via one or more devices. The samples are located as binary files in the folder "data". If samples from different devices are to be evaluated, all samples must be moved to the "data" folder of the evaluating instance.

__Initiate the verification process:__
Click on "Verification" in the navigation bar. All previously saved samples will be displayed here. Select at least one learning sample and one test sample. Start the verification process by clicking on the button "Start verification process". If desired, click on "Encrypt testsamples for verification" beforehand. The test samples are then treated as if their plaintext is unknown. The results are shown afterwards. The default setting for this is a series of threshold values in the range from 0 to the maximum measured Euclidean distance of the current verification process. The values are displayed normalised on the x-axis from 0 to 1, where 1 corresponds to the maximum threshold value. You can adjust the maximum threshold value yourself by entering a new value in the "Adjust the threshold" field and confirming it by clicking on "Apply new threshold".

__Evaluation of the verification process:__
False Acceptance Rate (FAR): To be able to evaluate the FAR, select the samples belonging to a user as learn samples and the samples belonging to other users (imposter) as test samples. The subsequently displayed acceptance rate shows the FAR.
False Rejection Rate (FRR): To be able to evaluate the FRR, select the samples that belong to a user as learning samples and test samples. The rejection rate that is then displayed shows the FRR.

## Screenshots

Recording (free text)                                   | Recording results
------------------------------------------------------- | -------------------------------------------------------
![image](/screenshots/recording_free_text.png?raw=true) | ![image](/screenshots/recording_results.png?raw=true)

Verification                                            | Verification results
------------------------------------------------------- | -------------------------------------------------------
![image](/screenshots/verification.png?raw=true)        | ![image](/screenshots/verification_results.png?raw=true)

Find more screenshots here: [Screenshots Keystroke Biometrics](screenshots/)

## Changes and independent further work

If you would like to use this project for yourself and make local changes to it, make sure everything works fine by running the unittests located in the "tests" directory. In your terminal, navigate to "keystroke_biometrics". Run "python -m unittest tests.keyboardcapture_test" and "python -m unittest tests.verification_test". You may need to specify the correct python version (3.10.2 or upwards) by running this command if it is not set as default.

## Sources and acknowledgment

The methods and formulars of the verification process included in this project are based on the following sources:
R. Joyce, G. Gupta: Identity Authentication Based on Keystroke Latencies, 1990, https://dl.acm.org/doi/pdf/10.1145/75577.75582, page 171 (last visit 21/05/2022)
F. Monrose, A. D. Rubin: Keystroke dynamics as a biometric for authentication, 2000, http://www1.cs.columbia.edu/~hgs/teaching/security/hw/keystroke.pdf, page 352-356 (last visit 21/05/2022)
