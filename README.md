# picamera2-flask

## Virtual env python
- Python virtual environments should be created in such a way as to include your site packages. This is because the
libcamera Python bindings are not available through PyPI so you can’t install them explicitly afterwards.To create a virtual environment for python3.

	``` bash
	cd /home/gen64/
	python -m venv --system-site-packages picam-env
	source /home/gen64/.venv/picam-env/bin/activate
	```
- Install picamera-2

	```bash
	sudo apt install -y python3-libcamera python3-kms++
	sudo apt install -y python3-prctl libatlas-base-dev ffmpeg python3-pip
	sudo apt install -y python3-pyqt5 python3-opengl # only if you want GUI features
	pip3 install numpy --upgrade
	pip3 install picamera2
	```

## code.py
- This has the code to run the cameara and flask server and show it on local website.

## livecam.service 
- Copy this script to `/etc/systemd/system`.
```bash	
sudo cp livecam.service /etc/systemd/system
```

- Enable this service at boot.
```bash
sudo systemctl enable livecam
```
## config_template.py
- Replace the 'xxyyzz' with your telegram API token.
- After that rename and savve this file as config.py.