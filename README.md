# Client server application

## Image compression and transmission
In terminal window 1, start the server:

```
python server.py
```

In terminal window 2, establish TCP/IP connection, compress and transmit image:

```
python client.py
```

<img src="./All.png" alt="Different compression ratios" width="300"/>
<img src="./Bytes.png" alt="Number of bytes transferred for different compression ratios" width="150"/>
<img src="./MSE.png" alt="Mean squared error for different compression ratios" width="150"/>

## Send email

To send a custom email:

```
python send_email.py
```