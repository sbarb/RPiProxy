currently this is a Proxy Server 
for the `Raspberry Pi` 
to control `GPIO pins`
through a `web ui`

Flask - Client/http-Server  -> Socket - Server -> GPIO

proxyserver.py -> piserver-main.py -> GPIO

Flask is the http server that acts as the client to the Socket Server


