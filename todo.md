Remaining tasks todo
====================

In order to make this a reasonably useful application it needs some tlc...

Configuration file
-------------------
Probably based on pythons ConfigParser.

User specified parameters:
 * API token (possibly encrypted)
 * Debug level
 * Poll rate
 * Notifications on/off
 * Proxy server (https)

API token encryption
--------------------
The API token is stored in the configuration file in plain text format. Not an ideal way to store authentication data...

setuptools installer support
----------------------------
Create an appropriate directory structure and setup.py installer file.

Load icons from relative paths
------------------------------
Relative to source directory... Right now it's full paths and that's just stupid.

Update ListStore model properly
-------------------------------
After polling the toggl server for the latest time entries, update the ListStore model intelligently with only the entries that have changed.

Asynchronous poll
-----------------
Get the multi-threaded polling working. It appears to be non-trivial with regular python treads and the gtk GUI loop. Luckily Google reveal lots of results on this issue...

As an alternative, use the gtk timer event to regularly poll for new data.

