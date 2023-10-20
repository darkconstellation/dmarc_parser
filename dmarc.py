import xml.etree.ElementTree as ET
import copy
import pandas as pd



class Dmarc:

    def __init__(self):
        pass

    def load(self, filename):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
    
    def as_dict(self):        
        return self.xml_to_dict(self.root)
    
    def as_dictflat(self):        
        return self.xml_to_dictflat()
    
    def as_df(self):        
        return pd.DataFrame(self.as_dictflat())
    
    def to_csv(self, filename):
        df = pd.DataFrame(self.as_dictflat())
        df.to_csv(filename, index=False)

    def xml_to_dict(self, element):
        dict_data = {}    
        for child in element:
            child_count = len(element.findall(child.tag))
            
            # if child_count>1 probably it is an array
            if child_count > 1:        
                rec = self.xml_to_dict(child)
                if child.tag in dict_data:
                    dict_data[child.tag].append(rec)            
                else:
                    dict_data[child.tag] = [rec]
            else:
                if child:
                    dict_data[child.tag] = self.xml_to_dict(child)
                else:            
                    dict_data[child.tag] = child.text
        return dict_data
    
    def xml_to_dictflat(self):
        dict_data = self.xml_to_dict(self.root)
        dict_obj = {}
        dict_arr = []
        
        for key, value in dict_data.items():                
                if key == 'record':
                    if isinstance(value, list):
                        for rec in value:                            
                            flattened_dict = self.flatten_dict(rec)
                            dict_obj.update(flattened_dict)                        
                            dict_arr.append(copy.deepcopy(dict_obj))
                    elif isinstance(value, dict):
                        flattened_dict = self.flatten_dict({key: value})
                        dict_obj.update(flattened_dict)                        
                        dict_arr.append(copy.deepcopy(dict_obj))
                else:
                    flattened_dict = self.flatten_dict({key: value}, skip_key='record')
                    dict_obj.update(flattened_dict)

        return dict_arr
    
    def flatten_dict(self, d, parent_key='', separator='_', skip_key=None):
        items = {}        
        for key, value in d.items():
            if key != skip_key:
                new_key = parent_key + separator + key if parent_key else key
                if isinstance(value, dict):
                    items.update(self.flatten_dict(value, new_key, separator=separator))
                else:
                    items[new_key] = value
        return items

