# AppSpeedXray
- Main source code repository for AppSpeedXray

![AppSpeedXray Components][components]

- The system consists of a Mobile app crawler, a Mobile app tester, a performance analyzer, and a manager.


## [Mobile APK Crawler](https://github.com/munhyunsu/AppSpeedXray/tree/master/MobileAPKCrawler)
- The mobile app crawler collects APK files of target mobile apps from Android app marketplace and emulator.
- We have implemented a mobile app crawler with Python Selenium and Android emulator that downloads APK files.


## [Mobile APP Tester](https://github.com/munhyunsu/AppSpeedXray/tree/master/MobileAppTester)
- AppSpeedXray run a Mobile app tester that installs the APK file, invoking the mobile app with the user inputs with monkeyrunner, and that records the packet, XML, CPU usage and video log files.
- In fuzz testing the user input hit ratio is low, because random user events may not often land on the correct position on the menu of the mobile app. Therefore, Mobile app tester devise a clickable component parsing function that extracts the XML layout log files for the mobile app and finds the 'clickable' components that can receive user events.

### Need to integrate with Website


## [Performance Analyzer](https://github.com/munhyunsu/AppSpeedXray/tree/master/PerformanceAnalyzer)
- A performance analyzer calculates the speed index, mobile app performance metrics, performance score and traffic statistics. For this purpose, performance analyzer consist of scene detector, snapshot generator and similarity calculator modules.



[components]: https://drive.google.com/uc?id=1RMAGQyN-5mcae4kRVJ1UMsppw-OUhoPj

## Coded by
- Hyunsu Mun (munhyunsu@gamil.com)

