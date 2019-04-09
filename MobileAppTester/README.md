# TODO
- Android Virtual Device!
- Detect rendering completion
- Monitor CPU load
  - using top



# Experiments Step
1. Search target apk files(or parse target app list)
2. Capture the packets, and Record the screen, and Log XML layouts
3. Quickly, execute app using adb
4. After execution send any UDP packet for marking
5. If the app complete rendering then generate user input to device
6. reqeat 4-5 until 5 input is inserted
