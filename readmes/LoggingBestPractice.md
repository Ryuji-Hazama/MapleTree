# Logging Best Practice

## What Is "Logging"

### The flight recorder of the application

&nbsp;&nbsp;&nbsp;&nbsp;When you are developing an application, you might experience that your application is crashing silently. Then you will insert a bunch of `print()` lines to determine where the application failed, and what was causing the error. That is a log, and those outputs are showing the exact path of your process, and help you understand what is working correctly, why, and where your code failed after the application halts.

&nbsp;&nbsp;&nbsp;&nbsp;However, those logs are disappearing when you close the output terminal, or the terminal was automatically closed by the application. That is why you need to output logs to a file like a flight recorder in a black box.

### Four W's of Logging

&nbsp;&nbsp;&nbsp;&nbsp;Every time the event occurs, the logger should capture the "Four W's" to get the details of the event.

- **When** &mdash; When the event occurred.
- **Where** &mdash; Where the event happened.
- **What** &mdash; What was the event.
- **Weight** &mdash; How serious is the event?

### Logging vs `print()`

&nbsp;&nbsp;&nbsp;&nbsp;Many beginner developers use `print()` to see what their code is doing. While `print()` works for quick debugging, it is a 'disposable' way to log, and it is not recommended for production code. Here are some reasons why:

#### Lack of control

&nbsp;&nbsp;&nbsp;&nbsp;With `print()`, you have no filtering options. You see everything or nothing. With a logger, you can filter logs by severity level. You can choose what to see depending on the situation. For example, you can set the logger to only show warnings and errors in production, while showing debug information during development.

&nbsp;&nbsp;&nbsp;&nbsp;Also, with `print()`, you need to change your code to toggle the logging on and off. With a logger, you can easily enable or disable logging by changing the configuration and no code changes are required.

#### Lifetime

&nbsp;&nbsp;&nbsp;&nbsp;Logs created with `print()` disappear once the program ends or the terminal is closed. In contrast, logs created with a logger can be saved to a file, allowing you to review them later. This is especially useful for debugging issues that occur in production environments.

#### Context

&nbsp;&nbsp;&nbsp;&nbsp;Loggers can automatically include contextual information such as timestamps, file names, line numbers, and function names. This information can be invaluable when trying to understand the flow of your application and identify where issues are occurring. With `print()`, you would need to manually include this information in every log statement, which can be error-prone and time-consuming.

#### Why you log

&nbsp;&nbsp;&nbsp;&nbsp;Logging is essential for understanding the behavior of your application, especially when things go wrong. You don't log for the things go right, but for the things that go wrong and you aren't there to see it happen.

&nbsp;&nbsp;&nbsp;&nbsp;Logging is like a flight recorder. You can see what happened before the crash, and you can understand why the crash happened. If the log disappears because of the crash, then you have no way to understand what happened, and it will be very difficult to find the cause of the crash. But if the log is saved to a file like a flight recorder in a black box, then you can review the log and fix the issue more quickly.

## Outputs

### What to log

&nbsp;&nbsp;&nbsp;&nbsp;You should log the events that are important for understanding the behavior of your application, especially when things go wrong. This includes:

#### Errors and exceptions

&nbsp;&nbsp;&nbsp;&nbsp;Errors and exceptions are the most important events to log, as they indicate that something went wrong in your application. Also, many logger libraries can automatically capture the stack trace when an exception occurs, which can be very helpful for debugging. Those logs can help you understand what went wrong, where it went wrong, and why it went wrong.

#### Warnings

&nbsp;&nbsp;&nbsp;&nbsp;Warnings are events that indicate a potential issue in your application. They may not cause the application to crash, but they can lead to unexpected behavior or performance issues. Logging warnings can help you identify and fix potential problems before they become critical.

#### Important state changes

&nbsp;&nbsp;&nbsp;&nbsp;Logging important state changes in your application can help you understand the flow of your application and identify where issues are occurring. For example, you might want to log when a user logs in or out, when a database connection is established or closed, or when a critical function is called.

### What not to log

&nbsp;&nbsp;&nbsp;&nbsp;While you are developing or debugging your application, you might want to log everything to understand the flow of your application and its variables. However, there are some things that you should not log, especially in production environments for security and performance reasons. This includes:

#### Sensitive information

&nbsp;&nbsp;&nbsp;&nbsp;You should never log sensitive information such as passwords, credit card numbers, or personally identifiable information (PII). Logging sensitive information can lead to security breaches and legal issues. If you need to log sensitive information for debugging purposes, make sure to mask or obfuscate it before logging, and remove those logs before deploying to production.

#### 'Garbage' information

&nbsp;&nbsp;&nbsp;&nbsp;You might want to log everything during development, but in production, you should avoid logging 'garbage' information that is not useful for understanding the behavior of your application. This includes logging every single variable change or every single function call, which can lead to log bloat and make it difficult to find important information in the logs. Also, those logs can have a performance impact on your application, especially if they are logged synchronously.

## Log Levels

&nbsp;&nbsp;&nbsp;&nbsp;Log levels are used to indicate the severity of an event. They help you filter logs and focus on the most important information. I will show you the log levels based on my `MapleX` logger, but the concept is similar in other logging libraries.

### `TRACE`

&nbsp;&nbsp;&nbsp;&nbsp;The `TRACE` level is the lowest log level, and it is used for very detailed information that is typically only useful for debugging. It can include information about the flow of the application, variable values, and other low-level details when you are hunting for a specific hard-to-find issue. You should suppress `TRACE` logs in production environments, or they can cause a performance impact and make it difficult to find important information in the logs.

### `DEBUG`

&nbsp;&nbsp;&nbsp;&nbsp;The `DEBUG` level is used for information that is useful for coding and debugging, but not as detailed as `TRACE`. It can include information about the state of the application, such as when a function is called or when a variable is updated. You can use this level to understand 'how' and 'why' something is happening in your application. Like `TRACE`, you should suppress `DEBUG` logs in production environments to reduce the amount of logs and improve performance.

### `INFO`

&nbsp;&nbsp;&nbsp;&nbsp;The `INFO (INFORMATION)` level is used for general information about the application's operation. It can include information about the application's startup, shutdown, or other significant events that are not errors or warnings. `INFO` logs are standard 'milestones' that can be useful in production environments to understand the normal operation and the flow of the application. But you should avoid logging too much information at this level, and focus on logging important events that can help you understand the behavior of your application.

### `WARN`

&nbsp;&nbsp;&nbsp;&nbsp;The `WARN (WARNING)` level is used for events that indicate a potential issue in your application. They may not cause the application to crash, but they can lead to unexpected behavior or performance issues, such as deprecated API usage, or a failed connection to a third-party service. You can use this level to flag unexpected events or conditions that may require attention, but do not necessarily indicate a failure and the application can continue running. Logging warnings can help you identify and fix potential problems before they become critical.

### `ERROR`

&nbsp;&nbsp;&nbsp;&nbsp;The `ERROR` level is used for events that indicate a failure in your application. They indicate that something went wrong and the user probably got an error message, but the rest of the application can continue running. Logging errors can help you understand what went wrong, where it went wrong, and why it went wrong, so you can fix the issue and prevent it from happening again. You should also log the exception message and stack trace when an error occurs, as it can provide valuable information for debugging.

### `FATAL`

&nbsp;&nbsp;&nbsp;&nbsp;The `FATAL` (or `CRITICAL` might be used in some logging libraries) level is the highest log level, and it is used for events that indicate a critical failure in your application. They indicate that something went wrong, and the application cannot continue running or is in an unstable state. This level is used when the application encounters a situation that it cannot recover from, and is about to crash. Logging fatal errors can help you understand what went wrong, where it went wrong, and why it went wrong, so you can fix the issue and prevent it from happening again. You should also log the exception message and stack trace when a fatal error occurs, as it can provide valuable information for debugging.

### `NONE`

&nbsp;&nbsp;&nbsp;&nbsp;The `NONE` level is a special level in `MapleX` that not commonly exists in other logging libraries. It is used to bypass all the log level filters and always output the log, or suppress all other log levels if you set this in the logger configuration. This is useful for debugging in production environments, where you want to log a specific event, but don't want to log any other lower level events under the same logger configuration. For example, you can set the log level to `NONE` for a specific logger to always log suspicious events, while setting the log level to `WARN` for other loggers to only log warnings and errors.

## Conclusion

&nbsp;&nbsp;&nbsp;&nbsp;Logging is an essential part of software development, and it can help you understand the behavior of your application, especially when things go wrong. By following the best practices for logging, you can ensure that your logs are useful, informative, and easy to understand. Remember to log important events, avoid logging sensitive information, and use log levels to filter logs and focus on the most important information.

&nbsp;&nbsp;&nbsp;&nbsp;If you master the art of logging, you can become a more effective developer and create applications that are easier to maintain and debug. You will never lose your important logs again when your application silently crashes and wipes out all the logs in the terminal. You can always review the logs in the log file, and understand what happened, where it happened, and why it happened.

&nbsp;&nbsp;&nbsp;&nbsp;So, start logging wisely, and use the power of logging to improve your development process and create better applications!

&nbsp;&nbsp;&nbsp;&nbsp;If you want to learn about how to use the `MapleX` logger, check out the [documentation](https://github.com/Ryuji-Hazama/MapleTree/blob/main/README.md) and the [Logger README](https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/README_Logger.md) for more details and examples. `MapleX` is designed to be beginner-friendly and easy to use, so you can start logging effectively in your applications right away!

&nbsp;&nbsp;&nbsp;&nbsp;Happy logging, and may your logs always be informative and helpful!
