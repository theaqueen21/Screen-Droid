# **ScreenDroid**

ScreenDroid is an Android debugger that allows you to share your Android device's screen wirelessly or via USB. It has a CLI interface in version 1 and a GUI interface in version 2.

>#  Features

- Version 1 supports one device at a time and has a limited set of features.
- Version 2 supports multiple devices, routing traffic to a specific adapter, and has a full feature set. It also has a startup animation and prevents multiple instances of the process from running. It has keybinds for refreshing, killing processes, and exiting the application.

>#  Built With
* [ADB](https://developer.android.com/studio/command-line/adb) - Automate this tool
* [Scrcpy](https://github.com/Genymobile/scrcpy) - Automate this tool
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - Graphical User Interface
* [Pillow](https://pillow.readthedocs.io/en/stable/) - Extract each frame from a .mp4 file
* [Imageio](https://imageio.readthedocs.io/en/stable/) - Read .mp4 files
* [Subprocess](https://docs.python.org/3/library/subprocess.html) - Run commands and capture their output
* [Re](https://docs.python.org/3/library/re.html) - Filter command outputs and extract data
* [Sys](https://docs.python.org/3/library/sys.html) - Get temporary folder path generated by pyinstaller


># Compatibility

In order to use our app, the following requirements must be met:

- Your device must have USB debugging enabled in the developer options.
- Android 11 and higher officially support wireless screen sharing (it may also work on older versions).
- Android 5 and higher officially support wired screen sharing.
- Your device and PC must be on the same LAN.

># Tested Devices

We have tested our app on the following devices:

- Samsung Galaxy S10 (Android 12)
- Oppo Reno 5G (Android 12.1)
- Samsung Galaxy J5 2016 (Android 10, Lineage OS 17)
- Samsung Galaxy Tab 4 (Android 4.4.2)
- Samsung Galaxy Note 10.1 (Android 9, Lineage OS 16)

># Development

Our app was developed and tested on Python 3.9 to 3.10.4.
It is currently being developed and tested on Python 3.10 to 3.X.

># Known Issues

We are aware of the following issues with our app:

- Slow Startup
- Low Quality UI and Old Design
- If our app is ended incorrectly due to any system or user error, the lock file `AppData\Local\Temp\ADBV2.lock` might not get deleted, which will prevent the program from launching unless it is deleted manually.

># Upcoming Features

We have a number of exciting features in the pipeline for our app. Here's a sneak peek at what you can expect:

- **File Transfer**: Our app will allow you to easily download and upload files, both over wired and wireless connections.
- **Progress Monitoring**: Keep track of the progress of your file transfers with our built-in progress monitor.
- **WhatsApp Backup**: Don't worry about losing your WhatsApp data again! Our app will allow you to easily create backups of your chat history and media.
- **Custom Refresh Time**: Set the refresh time for the app to suit your needs.
- **User Settings**: Customize your experience with the ability to save your preferred settings.

Stay tuned for updates on these exciting new features!

># Donations (Monero):




![image](https://user-images.githubusercontent.com/94680549/212542650-0da201d1-704b-47e8-b11c-46d2435da4b0.png)
Thank You In Advance!
