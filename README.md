# handwritten-recognition
A flask app to recognize handwritten digits. Uses TensorFlow.
Please use tensorflow 2.9.

## Quick start
After cloning this repository, run [`start.sh`](https://github.com/penguinmoose/handwritten-recognition/blob/main/start.sh).
This script will also install the required packages.

_Note: For M1 macs, you will have to install Tensorflow seperately. See [this guide](https://developer.apple.com/metal/tensorflow-plugin/). All other packages (pillow, numpy, etc) can be installed via pip._

## Running this app
For this to work, you will have to install [`requirements.txt`](https://github.com/penguinmoose/handwritten-recognition/blob/main/requirements.txt).

If you use a M1 mac, see above note for installing tensorflow.

To run the app locally, enter the following two commands:
```
export FLASK_APP=run.py # Define flask app file
flask run # Run the application
```

To rerun after quitting the application, you don't have to enter the first command.
