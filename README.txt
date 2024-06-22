                      ╔╦╗  ╦    ╔═╗  ┬    ┌─┐  ┌─┐
                       ║   ║    ╚═╗  │    ├─┤  ├─┘
                       ╩   ╩═╝  ╚═╝  ┴─┘  ┴ ┴  ┴  

Thank you for using TLSlap (TLS exaustion Denial-of-Service script)

OVERVIEW:
    Various ways are used to abuse the TLS functionality of websites. In this specific
    instance, TLSlap abuses the TLS handshake, which serves to establish an encrypted
    means of communication between the client and the web server.

FUNCTIONALITY:
    TLSlap uses hard-coded TLS packets. Each packet attempts to initialize a TLS session
    via the TLS handshake process. Similar to a SYN attack, TLSlap never completes the
    handshake, but instead reintroduces more TLS handshakes with the server. This ultimately
    leads to resource exhaustion and unresponsiveness from the server.

TLS VERSION: 
    TLSlap supports both TLSv1.2 and TLSv1.3. This varying TLS version can be selected when
    using TLSlap. If you do not know what TLS version a website is using (if the site even
    uses TLS encryption at all) you can click the "🔓" icon at the top-left of the URL bar.
    You will be able to see the SSL/TLS encryption information about the website. Here you
    will be able to tell if a website is behind encryption (always the case with HTTPS web-
    sites) and what version of TLS it is using.

ANONYMITY:
    TLSlap will at the request of the user download a list of SOCKS4 proxies to use. Each
    packet will make use of a SOCKS4 proxy when sending the incomplete TLS handshake. The
    user may specify how many handshakes will pass through each individual proxy. The user
    also can refuse SOCKS4 proxification altogether.

If you encountered any bugs during the use of this script, please leave a comment.
