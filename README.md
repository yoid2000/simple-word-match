# simple-word-match

On my linux machine, the repo is at `/opt/simple-word-match`

There is a service file at: `sudo vim /etc/systemd/system/simple-word-match.service`


To reload systemd to apply the new service, start the service, and enable it to run on boot:

```
sudo systemctl daemon-reload
sudo systemctl start simple-word-match
sudo systemctl enable simple-word-match
```

To check if the service is running:

`sudo systemctl status simple-word-match`

Don't forget that gunicorn needs to be installed in the venv:

pip install gunicorn

To use the app from a browser:

http://192.168.178.40:8100