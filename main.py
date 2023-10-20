import os, dmarc

dmarc = dmarc.Dmarc()
path = 'dmarc_xml'
for f in os.listdir(path):        
    if f.endswith('.xml'):
        file = os.path.join(path, f)
        dmarc.load(file)
        # x = dmarc.as_dict()
        # print(file.replace('.xml','.csv'))
        dmarc.to_csv(file.replace('.xml','.csv'))

