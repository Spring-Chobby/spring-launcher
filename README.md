# Launcher
A wrapper for Spring to distribute and launch Spring games and Lua lobbies.

## Building natively (Recommended)

Requirements: PyQT5, pyinstaller (for freezing). See additional Python version restrictions for pyinstaller: https://github.com/pyinstaller/pyinstaller

Setting up a virtualenv and installing requirements:

1. Setup a virtual environment: `virtualenv --python=/usr/bin/python3 env`
2. Activate the virtual environment: `source env/bin/activate`
2. Install dependencies: `pip install PyQT5 pyinstaller`

Freezing:

1. Activate the virtual environment: `source env/bin/activate`
2. Change into the spring_launcher directory: `cd spring_launcher`
3. Freeze it with pyinstaller: `pyinstaller --windowed launcher.spec -y`

## Building on Wine (Unsupported)

Requires docker to be installed and user to be added to the docker group.

First enter the docker_wine folder and build:

docker build . -t chwine

Then to create a frozen release run the following command from the root of the repository:

docker run -v $PWD/spring_launcher:/spring_launcher chwine /bin/sh -c 'cd spring_launcher; wine /home/user/.wine/drive_c/Python35-32/Scripts/pyinstaller.exe --noconsole la
uncher.spec -y'

To test the frozen release (doesn't work for me), run the below:

docker run --net host -e DISPLAY=$DISPLAY -v $PWD/spring_launcher:/spring_launcher  chwine /bin/sh -c 'cd spring_launcher; wine dist/launcher/launcher.exe'
