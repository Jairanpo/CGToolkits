import sys
import os

env = 'dev'

paths = {
    'dev': 'C:\\Users\\OOL64\\Documents\\GitHub',
    'sta': 'S:\\CG\\scripts\\jair',
    'pro': 'S:\\TOOLKITS\\Maya'
}

path = paths['dev'] if env == 'dev' else paths['pro']

if env == 'dev':
    path = paths['dev']
elif env == 'sta':
    path = paths['sta']
elif env == 'pro':
    path = paths['pro']
else:
    print('Unspecified path')

if path in sys.path:
    print('Envar variable was already added')
else:
    print('Envar variable added')
    sys.path.append(path)

# ___________________________     Execution     ___________________________________

import camOps

camOps.GUI.show_dialog()
