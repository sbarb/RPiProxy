currently this is a Proxy Server 
for the `Raspberry Pi` 
to control `GPIO pins`
through a `web ui`

Flask - Client/http-Server  -> Socket - Server -> GPIO

proxyserver.py -> piserver-main.py -> GPIO

Flask is the http server that acts as the client to the Socket Server

# give your Pi a static IP address
https://www.modmypi.com/blog/tutorial-how-to-give-your-raspberry-pi-a-static-ip-address