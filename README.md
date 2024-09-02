# picamera2-flask

## code.py
- This has the code to run the cameara and flask server and show it on local website.

## livecam.service 
- Copy this script to `/etc/systemd/system`.
	
		`sudo cp livecam.service /etc/systemd/system`

- Enable this service at boot.
	
		`sudo systemctl enable livecam`

## config_template.py
- Replace the 'xxyyzz' with your telegram API token.
- After that rename and savve this file as config.py.