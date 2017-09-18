# Launcher
A wrapper for Chobby to launch Chobby + engine + set default configs up, etc

## Building on Wine

Requires docker to be installed and user to be added to the docker group.

First enter the docker_wine folder and build:

docker build . -t chwine

Then to create a frozen release run the following command from the root of the repository:

docker run -v $PWD/chobby_launcher:/chobby_launcher chwine /bin/sh -c 'cd chobby_launcher; wine /home/user/.wine/drive_c/Python35-32/Scripts/pyinstaller.exe --noconsole la
uncher.spec -y'

To test the frozen release (doesn't work for me), run the below:

docker run --net host -e DISPLAY=$DISPLAY -v $PWD/chobby_launcher:/chobby_launcher  chwine /bin/sh -c 'cd chobby_launcher; wine dist/launcher/launcher.exe'
