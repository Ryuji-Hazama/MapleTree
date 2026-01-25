# Exceptions

## `class MapleException(Exception)`

&nbsp;&nbsp;&nbsp;&nbsp;This is a basic exception class for MapleTree.

## `class MapleFileNotFoundException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the file that was specified at the instance initialization was not found.

## `class KeyEmptyException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when `encrypt=True` is used at the instance initialization, but the key for encryption is missing (`None` or empty).

## `class MapleFileLockedException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the instance tries to open the file, but the other instance has already locked the file.

## `class MapleDataNotFoundException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the data is not found in the file.

## `MapleEncryptionNotEnabledException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when trying to encrypt Maple data, but the encryption flag is `False`.

## `class MapleHeaderNotFoundException(MapleDataNotFoundException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the header (specified by the user) is not found in the data.

## `class MapleTagNotFoundException(MapleDataNotFoundException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the tag (specified by the user) is not found in the data.

## `class NotAMapleFileException(MapleDataNotFoundException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the file is not a Maple file.

- The file without a "MAPLE" line.

## `class InvalidMapleFileFormatException(NotAMapleFileException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the file format is an invalid Maple format.

- The file has a "MAPLE" line, but the format is wrong or broken.

## `class MapleFileEmptyException(NotAMapleFileException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the file is empty (No data)

## `class MapleSyntaxException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the syntax of the MapleTree function (mostly its parameter) is invalid.

## `class MapleTypeException(MapleSyntaxException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the user hands the unknown keyword arguments as the `**kwargs` to the MapleTree function.
