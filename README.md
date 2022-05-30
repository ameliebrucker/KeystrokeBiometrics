# Keystroke Biometrics

## Description
This software captures typing behaviour. Free texts and fixed texts (depending on a template text) can be submitted as samples. The application offers the possibility to statistically evaluate several entries in relation to each other and to present the results to the user. 

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage

### Submitting samples (relevant for study participants)

Samles with free text:
Click on "recording samples (free text)" in the navigation bar. Enter a text in the input field, your keystrokes will be recorded. Finish the input with the enter key. The "recording results" page is now displayed. You can discard or save your sample. You will then automatically return to the recording page.

Samples with fixed text:
Samples with fixed text are based on a given template text from which they may not deviate. Click on "Recording samples (fixed text)" in the navigation bar. Enter the template text in the text field. Finish the input with the enter key or a click on "Set template text". You can now enter the sample in the input field, your keystrokes will be recorded. Note that the entered text must match the template text, otherwise the text will be deleted. Finish the input with the enter key. The "recording results" page is now displayed. You can discard or save your sample. You will then automatically return to the recording page.

Tip: Prefer short texts over long ones to avoid typing errors.

### Carrying out the verification process (relevant for persons conducting a study)

Initiate the verification process:
Click on "Verification" in the navigation bar. All previously saved samples will be displayed here. Select at least one learning sample and one test sample. Start the verification process by clicking on the button "Start verification process". If desired, click on "Encrypt testsamples for verification" beforehand. The results are then displayed.

Evaluation of the verification process:
False Acceptance Rate (FAR): To be able to evaluate the FAR, select the samples belonging to a user as learn samples and the samples belonging to other users (imposter) as test samples. The subsequently displayed acceptance rate shows the FAR.
False Rejection Rate (FRR): To be able to evaluate the FRR, select the samples that belong to a user as learning samples and test samples. The rejection rate that is then displayed shows the FRR.

## Screenshots

Recording (free text)                                   | Recording results
------------------------------------------------------- | -------------------------------------------------------
![image](/screenshots/recording_free_text.png?raw=true) | ![image](/screenshots/recording_results.png?raw=true)

### Verification
![image](/screenshots/verification.png?raw=true)

Find more screenshots here: [Screenshots Keystroke Biometrics](screenshots/)

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

python -m unittest tests.keyboardcapture_test

## Sources and acknowledgment
The methods and formulars of the verification process included in this project are based on the following sources:
R. Joyce, G. Gupta: Identity Authentication Based on Keystroke Latencies, 1990, https://dl.acm.org/doi/pdf/10.1145/75577.75582, page 171 (last visit 21/05/2022)
F. Monrose, A. D. Rubin: Keystroke dynamics as a biometric for authentication, 2000, http://www1.cs.columbia.edu/~hgs/teaching/security/hw/keystroke.pdf, page 352-356 (last visit 21/05/2022)

## License
For open source projects, say how it is licensed.
