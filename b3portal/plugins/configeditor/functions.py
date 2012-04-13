from xml.etree.ElementTree import ElementTree

class Element:
    def __init__(self, name, items = None, text = None):
        if items:
            self.attrs = {}
            for k,v in items:
                self.attrs[k] = v    
        else:
            self.attrs = {}
        self.items = []
        self.name = name
        if len(text) > 0:
            self.value = text
        else:
            self.value = None
        
    def addItem(self, elem):
        self.items.append(elem)
        
def process_element(item):
    e = Element(item.tag, item.items(), item.text.strip())
    try:
        if len(list(item)) > 0:
            for c in list(item):
                e.addItem(process_element(c))
    except TypeError:
        pass
    return e

def parse_config(name):
    tree = ElementTree()
    tree.parse(name)
    items = []
    for item in list(tree.getroot()):
        items.append(process_element(item))
    return items