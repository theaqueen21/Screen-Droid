# ScreenDroid

ScreenDroid is an Android debugger that allows you to share your Android device's screen wirelessly or via USB. It has a CLI interface in Version 1 and a GUI interface in Version 2.

## Features

- Version 1 supports one device at a time and has a limited set of features.
- Version 2 supports multiple devices, routing traffic to a specific adapter, and has a full feature set. It also includes a startup animation, prevents multiple instances of the process from running, and provides keybindings for refreshing, killing processes, and exiting the application.

## Built With

- [ADB](https://developer.android.com/studio/command-line/adb) - Automate this tool (r34.0.3)
- [Scrcpy](https://github.com/Genymobile/scrcpy) - Automate this tool (v2.0)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Graphical User Interface
- [Pillow](https://pillow.readthedocs.io/en/stable/) - Extract each frame from a .mp4 file
- [Imageio](https://imageio.readthedocs.io/en/stable/) - Read .mp4 files
- [Subprocess](https://docs.python.org/3/library/subprocess.html) - Run commands and capture their output
- [Re](https://docs.python.org/3/library/re.html) - Filter command outputs and extract data

## Compatibility

To use our app, please ensure the following requirements are met:

- Your device must have USB debugging enabled in the developer options.
- ScreenDroid supports wireless screen sharing for Android devices, including Android 11 and higher, as well as older versions of Android. For older versions of Android, we have implemented an alternative method that requires a cable connection to obtain the necessary data and command the phone to listen to the correct port. This alternative method is already available in the app.

Please note that the official wireless screen sharing method, which works exclusively with Android 11 and higher, is currently under development and will be available in a future update.

Your device and PC must be on the same LAN for both the official wireless screen sharing method (Android 11 and higher) and the alternative method (for older versions of Android) to work.



## Tested Devices

We have tested our app on the following devices:

- Samsung Galaxy S10 (Android 12)
- Oppo Reno 5G (Android 12.1)
- Samsung Galaxy J5 2016 (Android 10, Lineage OS 17)
- Samsung Galaxy Tab 4 (Android 4.4.2)
- Samsung Galaxy Note 10.1 (Android 9, Lineage OS 16)

## Development

Our app was developed and tested on Python 3.9 to 3.10.4. It is currently being developed and tested on Python 3.10 to 3.X.

## Known Issues

We are aware of the following issues with our app:

- Slow Startup
- A bug occasionally occurs that may cause the device's name to disappear from the list box when running a task. This bug is random and rare, and its occurrence may result in unexpected errors. 
- Low Quality UI and Old Design
- If our app is terminated incorrectly due to any system or user error, the lock file `AppData\Local\Temp\ADBV2.lock` might not get deleted, which will prevent the program from launching unless it is deleted manually.

## Upcoming Features

We have a number of exciting features in the pipeline for our app. Here's a sneak peek at what you can expect:

- **File Transfer**: Easily download and upload files, both over wired and wireless connections.
- **Progress Monitoring**: Keep track of the progress of your file transfers with our built-in progress monitor.
- **WhatsApp Backup**: Create backups of your chat history and media easily.
- **Custom Refresh Time**: Set the refresh time for the app to suit your needs.
- **User Settings**: Customize your experience with the ability to save your preferred settings.
- **Update Mechanism**: An update mechanism will be added.
- **Tree Process**: Allow running ADB processes to proceed without requiring ScreenDroid to be open.
- **Automatic Backup**: Automatically back up selected folders and improved app startup performance.


Stay tuned for updates on these exciting new features!

## Donations (Monero)

![image](https://user-images.githubusercontent.com/94680549/212542650-0da201d1-704b-47e8-b11c-46d2435da4b0.png)

Thank you in advance!
