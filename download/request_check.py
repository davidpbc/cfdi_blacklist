# -*- coding: utf-8 -*-
import base64
import hashlib
import requests
from lxml import etree

RESPONSE_STR = 'Respuesta del servicio de Verificación de Solicitud de Descarga: {}'


class RequestCheck():
    URL_CHECK = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc'
    SOAP_ACTION = 'http://DescargaMasivaTerceros.sat.gob.mx/IVerificaSolicitudDescargaService/VerificaSolicitudDescarga'
    NSMAP = {
        's': 'http://schemas.xmlsoap.org/soap/envelope/',
        'des': 'http://DescargaMasivaTerceros.sat.gob.mx',
        'xd': 'http://www.w3.org/2000/09/xmldsig#'
    }

    def __init__(self, fiel):
        self.fiel = fiel
    
    def generate_soapreq(self, requester_rfc, req_id):
        soap_req = etree.Element('{{{}}}{}'.format(self.NSMAP['s'], 'Envelope'), nsmap=self.NSMAP)
        
        etree.SubElement(soap_req, '{{{}}}{}'.format(self.NSMAP['s'], 'Header'))

        body = etree.SubElement(soap_req, '{{{}}}{}'.format(self.NSMAP['s'], 'Body'))

        verificasolicituddescarga = etree.SubElement(body, '{{{}}}{}'.format(self.NSMAP['des'], 'VerificaSolicitudDescarga'))

        solicitud = etree.SubElement(verificasolicituddescarga, '{{{}}}{}'.format(self.NSMAP['des'], 'solicitud'))
        solicitud.set('IdSolicitud', req_id)
        solicitud.set('RfcSolicitante', requester_rfc)
        
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

        to_digest = etree.tostring(verificasolicituddescarga, method='c14n', exclusive=1)

        digest = base64.b64encode(hashlib.new('sha1', to_digest).digest())
        
        digestvalue.text = digest

        to_sign = etree.tostring(signedinfo, method='c14n', exclusive=1)
        
        firma = self.fiel.sign_sha1(to_sign)

        signaturevalue.text = firma

        x509certificate.text = self.fiel.cer_to_b64()

        x509issuername.text = self.fiel.get_issuer_data()

        x509serialnumber.text = self.fiel.get_serial()
        
        return etree.tostring(soap_req, encoding='utf-8')
    
    def verificar_descarga(self, token, requester_rfc, req_id):
        
        soapreq = self.generate_soapreq(requester_rfc, req_id)

        headers = {
            'Content-type': 'text/xml;charset="utf-8"',
            'Accept': 'text/xml',
            'Cache-Control': 'no-cache',
            'SOAPAction': self.SOAP_ACTION,
            'Authorization': 'WRAP access_token="{}"'.format(token)
        }

        response = requests.post(self.URL_CHECK, data=soapreq, headers=headers, verify=True)

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

        val = 's:Body/VerificaSolicitudDescargaResponse/VerificaSolicitudDescargaResult'

        res = resp_xml.find(val, namespaces=nsmap)

        request_vals = {
            'cod_estatus': res.get('CodEstatus'),
            'estado_solicitud': res.get('EstadoSolicitud'),
            'codigo_estado_solicitud': res.get('CodigoEstadoSolicitud'),
            'numero_cfdis': res.get('NumeroCFDIs'),
            'mensaje': res.get('Mensaje'),
            'paquetes': []
        }

        for id_paquete in res.iter('{{{}}}IdsPaquetes'.format(nsmap[None])):
            request_vals['paquetes'].append(id_paquete.text)

        return request_vals
