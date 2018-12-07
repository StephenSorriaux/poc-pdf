import config

from werkzeug.utils import secure_filename
import pandas

import os

def generate_inventory_for_file(xls, messages):
    try:
        xls_filename = secure_filename(xls.filename)
        xls.save(os.path.join(config.UPLOAD_FOLDER, xls_filename))

        # get le fichier excel inventaire
        inventory_raw = pandas.read_excel(
            os.path.join(config.UPLOAD_FOLDER, xls_filename),
            usecols='A,B',
            sheet_name=0,
            skiprows=[0, 1, 2, 3, 4],
            index_col=None,
            header=None
        )
        inventory_raw.set_axis(['name', 'quantite'], axis=1, inplace=True)
        inventory = inventory_raw.set_index('name')
    except Exception as e:
        messages.append('Impossible de recuprer les infos du fichier Excel: ' + str(e))
        return None
    
    try:
        os.remove(os.path.join(config.UPLOAD_FOLDER, xls_filename))
    except Exception as e:
        print('Impossible de supprimer le fichier excel: ', e)
    
    return inventory