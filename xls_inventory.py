import config

from werkzeug.utils import secure_filename
import pandas

import os

def generate_groups_for_file(xls, messages):
    try:
        xls_filename = secure_filename(xls.filename)
        xls.save(os.path.join(config.UPLOAD_FOLDER, xls_filename))

        # get le fichier excel inventaire
        inventory_raw = pandas.read_excel(
            os.path.join(config.UPLOAD_FOLDER, xls_filename),
            usecols=[0,1],
            skiprows=0,
        )
        inventory_raw.set_axis(['name', 'famille',], axis=1, inplace=True)
        inventory = inventory_raw.set_index('name')
    except Exception as e:
        messages.append('Impossible de recuperer les infos du fichier Excel (groups): ' + str(e))
        return None
    
    try:
        os.remove(os.path.join(config.UPLOAD_FOLDER, xls_filename))
    except Exception as e:
        print('Impossible de supprimer le fichier excel: ', e)
    
    return inventory

def generate_inventory_for_file(xls, messages):
    try:
        xls_filename = secure_filename(xls.filename)
        xls.save(os.path.join(config.UPLOAD_FOLDER, xls_filename))

        # get le fichier excel inventaire
        inventory_raw = pandas.read_excel(
            os.path.join(config.UPLOAD_FOLDER, xls_filename),
        )
        inventory_raw.set_axis(['name', 'quantite',], axis=1, inplace=True)
        inventory = inventory_raw.set_index('name')
    except Exception as e:
        messages.append('Impossible de recuperer les infos du fichier Excel (inventaire): ' + str(e))
        return None
    
    try:
        os.remove(os.path.join(config.UPLOAD_FOLDER, xls_filename))
    except Exception as e:
        print('Impossible de supprimer le fichier excel: ', e)
    
    return inventory