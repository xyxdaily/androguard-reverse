

import sys
from typing import Union, BinaryIO

#  External dependecies
# import asn1crypto
from asn1crypto.x509 import Name
from loguru import logger

class MyFilter:
    def __init__(self, level:int) -> None:
        self.level = level

    def __call__(self, record):
        levelno = logger.level(self.level).no
        return record["level"].no >= levelno


def set_log(level:int) -> None:
    """
    Sets the log for loguru based on the level being passed.
    The possible values are TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    """
    logger.remove(0)
    my_filter = MyFilter(level)
    logger.add(sys.stderr, filter=my_filter, level=0)


# Stuff that might be useful

def read_at(buff: BinaryIO, offset:int, size:int=-1) -> bytes:
    idx = buff.tell()
    buff.seek(offset)
    d = buff.read(size)
    buff.seek(idx)
    return d


def readFile(filename: str, binary:bool=True) -> bytes:
    """
    Open and read a file
    :param filename: filename to open and read
    :param binary: True if the file should be read as binary
    :return: bytes if binary is True, str otherwise
    """
    with open(filename, 'rb' if binary else 'r') as f:
        return f.read()


def get_certificate_name_string(name:Union[dict,Name], short:bool=False, delimiter:str=', ') -> str:
    """
    Format the Name type of a X509 Certificate in a human readable form.

    :param name: Name object to return the DN from
    :param short: Use short form (default: False)
    :param delimiter: Delimiter string or character between two parts (default: ', ')

    :type name: dict or :class:`asn1crypto.x509.Name`
    :type short: boolean
    :type delimiter: str

    :rtype: str
    """
    if isinstance(name, Name):#asn1crypto.x509.Name):
        name = name.native

    # For the shortform, we have a lookup table
    # See RFC4514 for more details
    _ = {
        'business_category': ("businessCategory", "businessCategory"),
        'serial_number': ("serialNumber", "serialNumber"),
        'country_name': ("C", "countryName"),
        'postal_code': ("postalCode", "postalCode"),
        'state_or_province_name': ("ST", "stateOrProvinceName"),
        'locality_name': ("L", "localityName"),
        'street_address': ("street", "streetAddress"),
        'organization_name': ("O", "organizationName"),
        'organizational_unit_name': ("OU", "organizationalUnitName"),
        'title': ("title", "title"),
        'common_name': ("CN", "commonName"),
        'initials': ("initials", "initials"),
        'generation_qualifier': ("generationQualifier", "generationQualifier"),
        'surname': ("SN", "surname"),
        'given_name': ("GN", "givenName"),
        'name': ("name", "name"),
        'pseudonym': ("pseudonym", "pseudonym"),
        'dn_qualifier': ("dnQualifier", "dnQualifier"),
        'telephone_number': ("telephoneNumber", "telephoneNumber"),
        'email_address': ("E", "emailAddress"),
        'domain_component': ("DC", "domainComponent"),
        'name_distinguisher': ("nameDistinguisher", "nameDistinguisher"),
        'organization_identifier': ("organizationIdentifier", "organizationIdentifier"),
    }
    return delimiter.join(["{}={}".format(_.get(attr, (attr, attr))[0 if short else 1], name[attr]) for attr in name])
