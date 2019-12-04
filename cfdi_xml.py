# -*- coding: utf-8 -*-
import os
from xml.dom import minidom


class CfdiXml(object):
    """
    Obtiene la información de un archivo XML para su renombrado.
    """
    fileName = ''
    comprobante = None
    com_attrs = False
    values = False
    version = False

    def __init__(self, fileName):
        """
        Método constructor de la instancia.
        Recibe el nombre de un archivo XML y lo procesa para obtener sus
        atributos, cambiar el nombre e insertar algunos de sus valores en un CSV
        """
        self.fileName = fileName
        self.attributes = dict()
        # Comprueba que el archivo exista
        if os.path.isfile(fileName):
            # Convierte el XML en un objeto MiniDOM para poder manipularlo
            self.comprobante = minidom.parse(fileName).childNodes[0]
            self.com_attrs = dict(self.comprobante.attributes.items())
        self.set_version()
        err = self.setAttributes()
        if err:
            raise ValueError('Error!.%s'% err)

    def set_version(self):
        if self.com_attrs.get('version'):
            self.version = self.com_attrs.get('version')
        elif self.com_attrs.get('Version'):
            self.version = self.com_attrs.get('Version')

    def setAttributes(self):
        """
        Obtiene los atributos del archivo XML y los guarda en la variable attributes
        """
        if self.comprobante:
            self.attributes['comprobante'] = dict(self.comprobante.attributes.items())
            errors = []
            if self.version == '3.2':
                errors.append(self.process_emisor_32())
                errors.append(self.process_receptor_32())
            elif self.version == '3.3':
                errors.append(self.process_emisor())
                errors.append(self.process_receptor())
            else:
                return "El programa solo soporta Versiones 3.3 y 3.2 de CFDi."
            if any(errors):
                error = "\n".join([x for x in errors if x])
                return "Se encontraron los siguientes errores: \n{}\nEn {}".format(error, self.fileName)
            return False

        return "El CFDi no es válido: {}".format(self.fileName)
    
    def process_receptor(self):
        """
        Obtiene los atributos del elemento cfdi:Receptor
        y los adjunta al diccionario de atributos
        """
        receptor = self.comprobante.getElementsByTagName('cfdi:Receptor')
        if not receptor:
            return "El CFDi no cuenta con Receptor"
        data = {}
        data['rfc'] = receptor[0].getAttribute('Rfc')
        data['nombre'] = receptor[0].getAttribute('Nombre')
        self.attributes['receptor'] = data
        return False

    def process_emisor(self):
        """
        Obtiene los atributos del elemento cfdi:Emisor
        y los adjunta al diccionario de atributos
        """
        emisor = self.comprobante.getElementsByTagName('cfdi:Emisor')
        if not emisor:
            return "El CFDi no cuenta con Emisor"
        data = {}
        data['rfc'] = emisor[0].getAttribute('Rfc')
        data['nombre'] = emisor[0].getAttribute('Nombre')
        self.attributes['emisor'] = data
        return False

    def process_receptor_32(self):
        """
        Obtiene los atributos del elemento cfdi:Receptor
        y los adjunta al diccionario de atributos para CFDi 3.2
        """
        receptor = self.comprobante.getElementsByTagName('cfdi:Receptor')
        if not receptor:
            return "El CFDi no cuenta con Receptor"
        data = {}
        data['rfc'] = receptor[0].getAttribute('rfc')
        data['nombre'] = receptor[0].getAttribute('nombre')
        self.attributes['receptor'] = data
        return False

    def process_emisor_32(self):
        """
        Obtiene los atributos del elemento cfdi:Emisor
        y los adjunta al diccionario de atributos para CFDi 3.2
        """
        emisor = self.comprobante.getElementsByTagName('cfdi:Emisor')
        if not emisor:
            return "El CFDi no cuenta con Emisor"
        data = {}
        data['rfc'] = emisor[0].getAttribute('rfc')
        data['nombre'] = emisor[0].getAttribute('nombre')
        self.attributes['emisor'] = data
        return False

    def get_rfc_emisor(self):
        return self.attributes['emisor']['rfc']

    def get_rfc_receptor(self):
        return self.attributes['receptor']['rfc']
