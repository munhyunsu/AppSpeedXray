# Mobile App Tester
![Render method][render]


## Feature
- UI Automation
- Capture screen, network traffic, CPU load, layout information

## Rendering completion detecting method
- Since it is not possible to find rendering completion event time directly from a mobile app, AppSpeedXray record the video file of a mobile app during the test, and determine the rendering completion event time when the similarity metric between two images becomes larger than the threshold.


## Working description
1. Search target apk files(or parse target app list)
2. Capture the packets, and Record the screen, and Log XML layouts
3. Quickly, execute app using adb
4. After execution send any UDP packet for marking
5. If the app complete rendering then generate user input to device
6. reqeat 4-5 until 5 input is inserted

[render]: https://lh5.googleusercontent.com/rSc_UoX5dH-uI9MKpo1ED55sZzgicUf99elh5ICVj64wqPVIfK9j6ZtpVvRG5RAI2KUTgK0NEDoggI4Y_wQB1VZJMbdzPtf7gUNTCMkuVfBYAbaQ4epN=w1175
