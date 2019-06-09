#!/usr/bin/env python3

import sys
from Crypto.PublicKey import RSA

def main():
    privateKeyFileName = sys.argv[1]
    publicKeyFileName = sys.argv[2]

    key = RSA.generate(1024)

    with open(privateKeyFileName, 'wb') as pemFile:
        pemFile.write(key.exportKey('PEM'))

    with open(publicKeyFileName, 'wb') as pemFile:
        pemFile.write(key.publickey().exportKey('PEM'))


if __name__ == '__main__':
    main()