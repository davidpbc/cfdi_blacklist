# -*- coding: utf-8 -*-
from crud import find_by_rfc
from cfdi_xml import CfdiXml
import sys
import os

folder_path = input('Introduce la ruta completa del directorio que quieres procesar.\n')


def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for name in files:
            if name.split('.')[-1].upper() in ('XML'):
                filename = '{}{}{}'.format(root, os.sep, name)
                process_xml_file(filename)


def process_xml_file(filename):
    sys.stdout.write('Buscando problemas en {}\n'.format(filename))
    fileCfdi = CfdiXml(filename)
    rfcs = [fileCfdi.get_rfc_emisor(), fileCfdi.get_rfc_receptor()]
    blacklist = find_by_rfc(rfcs=rfcs)
    if blacklist:
        for bl in blacklist:
            archivo = bl.get('defi') and 'Definitivos' or 'Presuntos'
            sys.stdout.write(
                'Problema con archivo {}\nContiene RFC: {} de la persona {}\n'
                'El cual esta indicado en la línea {} del archivo de {} del SAT\n' \
                    .format(
                        filename,
                        bl.get('rfc'),
                        bl.get('name'),
                        bl.get('csv_line'),
                        archivo))
    else:
        sys.stdout.write('Ningún problema detectado.\n')
    sys.stdout.write('-----------------------------------------\n')


if os.path.isdir(folder_path):
    process_folder(folder_path)
else:
    sys.stdout.write("La ruta de directorio es inválida!")
