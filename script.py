import xml.etree.ElementTree as ET
import json

def xml_to_json(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    def parse_element(element):
        """Convert an ElementTree element to a JSON-compatible dictionary"""
        result = dict(element.attrib)
        children = list(element)
        if children:
            result['children'] = [parse_element(c) for c in children]
        if element.text:
            text = element.text.strip()
            if text:
                result['text'] = text
        return result
    
    return json.dumps(parse_element(root), indent=4)

def json_to_xml(json_file):
    json_data = json.load(json_file)
    
    def convert_to_xml_element(json_obj, element_name):
        """Convert a JSON-compatible dictionary to an ElementTree element"""
        element = ET.Element(element_name)
        for key, value in json_obj.items():
            if key == 'children':
                for child in value:
                    child_element = convert_to_xml_element(child, list(child.keys())[0])
                    element.append(child_element)
            elif key == 'text':
                element.text = value
            else:
                element.set(key, value)
        return element
    
    return ET.tostring(convert_to_xml_element(json_data, list(json_data.keys())[0]), encoding='unicode')

  
  # XML to JSON
with open('input.xml', 'r') as xml_file:
    json_str = xml_to_json(xml_file)
    print(json_str)

# JSON to XML
with open('input.json', 'r') as json_file:
    xml_str = json_to_xml(json_file)
    print(xml_str)
