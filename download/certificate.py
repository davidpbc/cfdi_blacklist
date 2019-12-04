# -*- coding: utf-8 -*-
import base64

from OpenSSL import crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class Certificates():
    def __init__(self, cer_der, key_der, passphrase):
        self.import_cer(cer_der)
        self.import_key(key_der, passphrase)

    def import_cer(self, cer_der):
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
