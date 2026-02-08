# Logging Best Practice

## What Is "Logging"

### The flight recorder of the application

&nbsp;&nbsp;&nbsp;&nbsp;When you are developing an application, you might experience that your application is crashing silently. Then you will insert a bunch of `print()` lines to determine where the application failed, and what was causing the error. That is a log, and those outputs are showing the exact path of your process, and help you understand what is working correctly, why, and where your code failed after the application halts.

&nbsp;&nbsp;&nbsp;&nbsp;However, those logs are dissapearing when you close the output terminal, or the terminal was automatically closed by the application. That is why you need to output logs to a file like a flight recorder in a blackbox.

### Four W's of Logging

&nbsp;&nbsp;&nbsp;&nbsp;Every time the event occurs, the logger should capture the "Four W's" to get the details of the event.

- **When** &mdash; When the event occured.
- **Whrere** &mdash; Where the event happened.
- **What** &mdash; What was the event.
- **Weight** &mdash; How seriouc is the event?

### Logging vs `print()`
