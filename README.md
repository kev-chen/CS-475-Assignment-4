[//]: # (Kevin Chen)
[//]: # (Assignment 4)
[//]: # (CS 475)

# CS-475-Assignment-4
Simple Network Security Protocol


## Configuration
By default, the client is set up to connect to an AWS EC2 instance running the server code. To change this, edit the `serverName` key in `Client/settings.json` to a specific hostname running the server code.

Also by default, both the client and server are set up on port 13456. This can also be changed in `serverPort` key in the `Client/settings.json` and `Server/settings.json` files.

The encryption/decryption is reliant on:
- `Client/client_private_key.pem`
- `Client/server_public_key.pem`
- `Server/client_public_key.pem`
- `Server/server_private_key.pem`

There is only one client set up in the server's clients list, which the client will take the name of by default.

Note: Port 13456 must be used when connecting to the EC2 instance.


## Usage
Make sure the pycrypto module is installed by running 
  ```
    pip3 install pycrypto
  ```

### Client

`cd Client` to get into the Client directory, then run:
  ```
    python3 driver.py
  ```
If all defaults are unchanged, then this will immediately start the authentication algorithm and attempt to connect to the EC2 instance. Upon success, you should see the following:

  ```
    Successfully authorized. Server response: test_client_name,<session_key>
    ec2-52-32-60-227.us-west-2.compute.amazonaws.com>
  ```

Otherwise, failing authentication will be met with:
  ```
    Authentication Failed
  ```
You can cause authentication to fail by:
- Deleting a row from any *.pem file
- Deleting any *.pem file
- Changing the `clientName` key in `Client/settings.json`

Upon a successful connection, there are three commands: `ls`, `pwd`, and `quit` that will be executed on the server machine.

### Server
`cd Server` to get into the Server directory, then run:
  ```
    python3 driver.py
  ```

The server should output `Started listening on port 13456...` when successfully started. 
If running the server code from another machine, be sure to configure the client to connect to that machine in `Client/settings.json`. This setting can be configured to the output of running `hostname` if the server and client are running on the same machine.

### Keygen

To generate a new client keypair, configure client information, and add the new client to the server: 
From the root directory:

1. Run `python3 keygen.py <private_key_name.pem> <public_key_name_.pem>`
2. Place the newly generated `<private_key_name.pem>` file in the `Client` directory
3. Place the newly generated `<public_key_name.pem>` file in the `Server` directory
4. In `Client/settings.json`, change the clientName key value to a new name
5. In `Client/settings.json`, change the clientPrivateKey value to `<private_key_name.pem>`
6. In `Server/clients.json`, add a key-value pair for the new clientName: `<public_key_name.pem>`