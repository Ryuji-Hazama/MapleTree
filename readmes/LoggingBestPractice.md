# Logging Best Practice

## What Is "Logging"

### The flight recorder of the application

&nbsp;&nbsp;&nbsp;&nbsp;When you are developing an application, you might experience that your application is crashing silently. Then you will insert a bunch of `print()` lines to determine where the application failed, and what was causing the error. That is a log, and those outputs are showing the exact path of your process, and help you understand what is working correctly, why, and where your code failed after the application halts.

&nbsp;&nbsp;&nbsp;&nbsp;However, those logs are disappearing when you close the output terminal, or the terminal was automatically closed by the application. That is why you need to output logs to a file like a flight recorder in a black box.

### Four W's of Logging

&nbsp;&nbsp;&nbsp;&nbsp;Every time the event occurs, the logger should capture the "Four W's" to get the details of the event.

- **When** &mdash; When the event occured.
- **Whrere** &mdash; Where the event happened.
- **What** &mdash; What was the event.
- **Weight** &mdash; How seriouc is the event?

### Logging vs `print()`

&nbsp;&nbsp;&nbsp;&nbsp;Many beginner developers use `print()` to see what their code is doing. While `print()` works for quick debugging, it is a 'disposable' way to log, and it is not recommended for production code. Here are some reasons why:

#### Lack of control

&nbsp;&nbsp;&nbsp;&nbsp;With `print()`, you have no filtering options. You see everything or nothing. With a logger, you can filter logs by severity level. You can choose what to see depending on the situation. For example, you can set the logger to only show warnings and errors in production, while showing debug information during development.

&nbsp;&nbsp;&nbsp;&nbsp;Also, with `print()`, you need to change your code to toggle the logging on and off. With a logger, you can easily enable or disable logging by changing the configuration and no code changes are required.

#### Lifetime

&nbsp;&nbsp;&nbsp;&nbsp;Logs created with `print()` dissapear once the program ends or the terminal is closed. In contrast, logs created with a logger can be saved to a file, allowing you to review them later. This is especially useful for debugging issues that occur in production environments.

#### Context

&nbsp;&nbsp;&nbsp;&nbsp;Loggers can automatically include contextual information such as timestamps, file names, line numbers, and function names. This information can be invaluable when trying to understand the flow of your application and identify where issues are occurring. With `print()`, you would need to manually include this information in every log statement, which can be error-prone and time-consuming.

#### Why you log

&nbsp;&nbsp;&nbsp;&nbsp;Logging is essential for understanding the behavior of your application, especially when things go wrong. You don't log for the things go right, but for the things that go wrong and you aren't there to see it happen.

&nbsp;&nbsp;&nbsp;&nbsp;Logginng is like a flight recorder. You can see what happened before the crash, and you can understand why the crash happened. If the log dissapears because of the crash, then you have no way to understand what happened, and it will be very difficult to find the cause of the crash. But if the log is saved to a file like a flight recorder in a black box, then you can review the log and fix the issue more quickly.

## Outputs

### What to log

&nbsp;&nbsp;&nbsp;&nbsp;You should log the events that are important for understanding the behavior of your application, especially when things go wrong. This includes:

#### Errors and exceptions

#### Warnings

#### Important state changes

### What not to log

&nbsp;&nbsp;&nbsp;&nbsp;While you are developing or debugging your application, you might want to log everything to understand the flow of your application and its variables. However, there are some things that you should not log, especially in production environments for security and performance reasons. This includes:

#### Sensitive information

#### 'Garbage' information

## Log Levels

&nbsp;&nbsp;&nbsp;&nbsp;Log levels are used to indicate the severity of an event. They help you filter logs and focus on the most important information. I will show you the log lovels based on my `MapleX` logger, but the concept is similar in other logging libraries.

### `TRACE`

### `DEBUG`

### `INFO`

### `WARNING`

### `ERROR`

### `FATAL`

### `NONE`

&nbsp;&nbsp;&nbsp;&nbsp;The `NONE` level is a special level in `MapleX` that not commonly exists in other logging libraries. It is used to bypass all the log level filters and always output the log, or surpress all other log levels if you set this in the logger configuration. This is useful for debugging in production environments, where you want to log a specific event, but don't want to log any other lower level events under the same logger configuration. For example, you can set the log level to `NONE` for a specific logger to always log suspicious events, while setting the log level to `WARNING` for other loggers to only log warnings and errors.
