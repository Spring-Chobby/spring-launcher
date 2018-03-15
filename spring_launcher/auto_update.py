# Imports
from client_config import ClientConfig
from pyupdater.client import Client

# Constants
APP_NAME = 'Acme'
APP_VERSION = '1.0'

LIB_NAME = 'My external library'
LIB_VERSON = '2.4.1'

# This could potentially cause slow app start up time.
# You could use client = Client(ClientConfig()) and call
# client.refresh() before you check for updates
client = Client(ClientConfig(), refresh=True)

# Returns an update object
update = client.update_check(APP_NAME, APP_VERSION)

# Optionally you can use release channels
# Channel options are stable, beta & alpha
# Note: Patches are only created & applied on the stable channel
app_update = client.update_check(APP_NAME, APP_VERSION, channel='stable')
lib_update = client.update_check(LIB_NAME, LIB_VERSON)

# Use the update object to download an update & restart the app
if app_update is not None:
    downloaded = app_update.download()
    if downloaded is True:
        app_update.extract_restart()

# It's also possible to update an external library, file or anything else needed by your application.
if lib_update is not None:
    downloaded = lib_update.download()
    if downloaded is True:
        # The path to the archive.
        lib_update.abspath
