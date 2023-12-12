"""
This module parses the data from SRO.xml and returns the root element.

SRO.xml file is expected to be in the 'data' directory located in the same directory as this module.
"""

import os
import xml.etree.ElementTree as ET


def parse_xml_data(xml_file_path=None):
    '''Read the data form SRO.xml and return the root'''
    if xml_file_path is None:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        xml_file_path = os.path.join(data_dir, "SRO.xml")
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        return root
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"XML file not found at: {xml_file_path}") from exc
    except (ET.ParseError, IOError, PermissionError) as e:
        raise ValueError(f"Error parsing XML file at {xml_file_path}: {e}") from e
    