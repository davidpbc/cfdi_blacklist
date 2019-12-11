# -*- coding: utf-8 -*-
import base64

from OpenSSL import crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from datetime import datetime


class Certificates():
    def __init__(self, cer_der, key_der, passphrase, pem=False):
        self.import_cer(cer_der, pem)
        self.import_key(key_der, passphrase)

    def import_cer(self, cer_der, pem=False):
        if pem:
            self.cer = crypto.load_certificate(crypto.FILETYPE_PEM, cer_der)
        else:
            self.cer = crypto.load_certificate(crypto.FILETYPE_ASN1, cer_der)

    def import_key(self, key_der, passphrase):
        self.key = RSA.import_key(key_der, passphrase)
        self.signer = PKCS1_v1_5.new(self.key)

    def sign_sha1(self, text):
        sha1 = SHA.new(text)
        signature = self.signer.sign(sha1)
        return base64.b64encode(signature)

    def cer_to_b64(self):
        cer = crypto.dump_certificate(crypto.FILETYPE_ASN1, self.cer)
        return base64.b64encode(cer)

    def get_issuer_data(self):
        issuer = self.cer.get_issuer().get_components()
        data = ''
        for val in issuer:
            data += '{}={},'.format(
                val[0].decode('utf-8'), val[1].decode('utf-8'))
        return data[:-1]

    def get_serial(self):
        serial = str('%x' % self.cer.get_serial_number()). \
            replace('33', 'B').replace('3', ''). \
            replace('B', '3').replace(' ', ''). \
            replace('\r', '').replace('\n', ''). \
            replace('\r\n', '')
        return serial

    def get_cer_pem(self):
        return crypto.dump_certificate(crypto.FILETYPE_PEM, self.cer)

    def get_key_pem(self, passphrase=None):
        return self.key.exportKey(format='PEM', passphrase=passphrase, pkcs=8)

    def get_cert_dates(self):
        fmt = '%Y%m%d%H%M%S'
        date_start = str(self.cer.get_notBefore(), 'utf-8').replace('Z', '')
        date_end = str(self.cer.get_notAfter(), 'utf-8').replace('Z', '')
        return {
            'start': datetime.strptime(date_start, fmt),
            'end': datetime.strptime(date_end, fmt),
        }
