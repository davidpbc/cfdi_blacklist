# -*- coding: utf-8 -*-
import hashlib
import base64
from lxml import etree
import requests

RESPONSE_STR = 'Respuesta del servicio de Solicitud de Descarga: {}'


class RequestDownload():
    URL_REQUEST = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc'
    SOAP_ACTION = 'http://DescargaMasivaTerceros.sat.gob.mx/ISolicitaDescargaService/SolicitaDescarga'
    NSMAP = {
        's': 'http://schemas.xmlsoap.org/soap/envelope/',
        'des': 'http://DescargaMasivaTerceros.sat.gob.mx',
        'xd': 'http://www.w3.org/2000/09/xmldsig#'
    }

    def __init__(self, fiel):
        self.fiel = fiel

    def generate_soapreq(
        self, requester_rfc, init_date, end_date,
        issuer_rfc, receiver_rfc, req_type
    ):
        soap_req = etree.Element('{{{}}}{}'.format(self.NSMAP['s'], 'Envelope'), nsmap=self.NSMAP)
        
        etree.SubElement(soap_req, '{{{}}}{}'.format(self.NSMAP['s'], 'Header'))

        body = etree.SubElement(soap_req, '{{{}}}{}'.format(self.NSMAP['s'], 'Body'))

        solicitadescarga = etree.SubElement(body, '{{{}}}{}'.format(self.NSMAP['des'], 'SolicitaDescarga'))

        solicitud = etree.SubElement(solicitadescarga, '{{{}}}{}'.format(self.NSMAP['des'], 'solicitud'))
        solicitud.set('RfcSolicitante', requester_rfc)
        solicitud.set('FechaFinal', end_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        solicitud.set('FechaInicial', init_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        solicitud.set('TipoSolicitud', req_type)
        if issuer_rfc:
            solicitud.set('RfcEmisor', issuer_rfc)
        
        if receiver_rfc:
            solicitud.set('RfcReceptor', receiver_rfc)
        
        signature = etree.SubElement(solicitud, 'Signature', nsmap={None: 'http://www.w3.org/2000/09/xmldsig#'})

        signedinfo = etree.SubElement(signature, 'SignedInfo', nsmap={None: 'http://www.w3.org/2000/09/xmldsig#'})

        canonicalizationmethod = etree.SubElement(signedinfo, 'CanonicalizationMethod')
        canonicalizationmethod.set('Algorithm', 'http://www.w3.org/2001/10/xml-exc-c14n#')

        signaturemethod = etree.SubElement(signedinfo, 'SignatureMethod')
        signaturemethod.set('Algorithm', 'http://www.w3.org/2000/09/xmldsig#rsa-sha1')

        reference = etree.SubElement(signedinfo, 'Reference')
        reference.set('URI', '#_0')

        transforms = etree.SubElement(reference, 'Transforms')

        transform = etree.SubElement(transforms, 'Transform')
        transform.set('Algorithm', 'http://www.w3.org/2001/10/xml-exc-c14n#')

        digestmethod = etree.SubElement(reference, 'DigestMethod')
        digestmethod.set('Algorithm', 'http://www.w3.org/2000/09/xmldsig#sha1')

        digestvalue = etree.SubElement(reference, 'DigestValue')

        signaturevalue = etree.SubElement(signature, 'SignatureValue')

        keyinfo = etree.SubElement(signature, 'KeyInfo')
        
        x509data = etree.SubElement(keyinfo, 'X509Data')

        x509issuerserial = etree.SubElement(x509data, 'X509IssuerSerial')

        x509issuername = etree.SubElement(x509issuerserial, 'X509IssuerName')
        
        x509serialnumber = etree.SubElement(x509issuerserial, 'X509SerialNumber')
        
        x509certificate = etree.SubElement(x509data, 'X509Certificate')

        to_digest = etree.tostring(solicitadescarga, method='c14n', exclusive=1)

        # digest = hashlib.new('sha1', to_digest).digest()
        digest = base64.b64encode(hashlib.new('sha1', to_digest).digest())
        
        digestvalue.text = digest

        to_sign = etree.tostring(signedinfo, method='c14n', exclusive=1)

        firma = self.fiel.sign_sha1(to_sign)

        signaturevalue.text = firma

        x509certificate.text = self.fiel.cer_to_b64()

        x509issuername.text = self.fiel.get_issuer_data()

        x509serialnumber.text = self.fiel.get_serial()
        
        return etree.tostring(soap_req, encoding='unicode')

    def request_download(
            self, token, requester_rfc, init_date, end_date,
            issuer_rfc=None, receiver_rfc=None, req_type='CFDI'
        ):
        
        soapreq = self.generate_soapreq(
            requester_rfc, init_date, end_date, issuer_rfc, receiver_rfc, req_type)
        """ if soapreq:
            return soapreq """

        headers = {
            'Content-type': 'text/xml;charset="utf-8"',
            'Accept': 'text/xml',
            'Cache-Control': 'no-cache',
            'SOAPAction': self.SOAP_ACTION,
            'Authorization': 'WRAP access_token="{}"'.format(token)
        }

        response = requests.post(self.URL_REQUEST, data=soapreq, headers=headers, verify=True)

        if response.status_code != requests.codes['ok']:
            if not response.text.startswith('<s:Envelope'):
                ex = RESPONSE_STR.format(response.text)
            else:
                resp_xml = etree.fromstring(response.text)
                ex = resp_xml.find('s:Body/s:Fault/faultstring', namespaces=self.NSMAP).text
            raise Exception(ex)

        if not response.text.startswith('<s:Envelope'):
            ex = RESPONSE_STR.format(response.text)
            raise Exception(ex)

        nsmap= {
            's': 'http://schemas.xmlsoap.org/soap/envelope/',
            None: 'http://DescargaMasivaTerceros.sat.gob.mx'
        }

        resp_xml = etree.fromstring(response.text)

        val = 's:Body/SolicitaDescargaResponse/SolicitaDescargaResult'

        res = resp_xml.find(val, namespaces=nsmap)

        request_vals = {
            'id_solicitud': res.get('IdSolicitud'),
            'cod_estatus': res.get('CodEstatus'),
            'mensaje': res.get('Mensaje')
        }

        return request_vals
