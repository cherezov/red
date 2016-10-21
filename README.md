# red
Download proxy HTTP server. 
Listen incomming GET requests and redirects them according to path.

## Motivation
Some DLNA/UPnP devices (e.g Samsung Smart TVs) are working in bound of local network only and can't play media from internet directly.
A sort of workaround is required for such devices.

## Example
Let's say __red__ is up and listening on ```192.168.1.100:8000```  
Request like ```http://192.168.1.100:8000/http://www.somewhere.org/path/to/file.txt``` will download ```file.txt```

## Usage
```
> red.py [--ip <ip to listen on, default all current interfaces>] [--port <port to listen on, default 8000>]
```

## Requires
 * Python2
 
## TODO
 - [ ] Both py2 and py3 support
