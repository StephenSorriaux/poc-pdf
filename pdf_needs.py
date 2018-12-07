import config
import tables

import pandas
import tabula
from werkzeug.utils import secure_filename

import math
import os

def remove_useless_lines_from_file(infos):
    sanitized_infos = []
    for table in infos:
        current_table = pandas.DataFrame(data={}, index=[])
        if len(table.columns) > 5:
            to_be_removed = []

            for col_name, series in table.items():
                try:
                    # si 2 lignes d'affilee avec NaN, on la supprime
                    math.isnan(float(series[0]))
                    math.isnan(float(series[1]))
                    to_be_removed.append(col_name)
                except (ValueError, TypeError):
                    pass
                try:
                    # si la ligne Marchandise est suivi d'un Nan, on la supprime
                    if str(series[0]) == 'Marchandise':
                        math.isnan(float(series[1]))
                        to_be_removed.append(col_name)
                except (ValueError, TypeError):
                        pass
            table = table.drop(to_be_removed, axis=1)
            try:
                table.set_axis([i for i in range(5)], axis=1, inplace=True)
            except Exception:
                print(table)
                print('Il est possible que la ligne correspondant a la marchandise soit foireuse dans le fichier.')
                raise
        for count in range(1,len(table[0])):
            name = table[0][count]
            quantite = table[1][count]
            quantite_unite = table[2][count]
            quantite_prod = table[3][count]
            quantite_prod_unite = table[4][count]
            try:
                math.isnan(float(quantite_prod_unite))
                record = pandas.DataFrame(
                    data={
                        'name': [
                            name
                        ],
                        'quantite': [float(quantite)]
                    }
                )
            except ValueError:
                record = pandas.DataFrame(
                    data={
                        'name': [
                            name
                        ],
                        'quantite': [float(quantite_prod)]
                    }
                )
            except Exception:
                print('{}, {}, {}, {}, {}'.format(name, quantite, quantite_unite, quantite_prod, quantite_prod_unite))
                print(table)
                raise
            current_table = current_table.append(record, ignore_index=True)
        if not current_table.empty:
            finalized_table = current_table.set_index('name')
            sanitized_infos.append(finalized_table)

    return sanitized_infos

def generate_needs_for_file(pdf, messages):
    pdf_filename = secure_filename(pdf.filename)
    pdf.save(os.path.join(config.UPLOAD_FOLDER, pdf_filename))

    try:
        infos = tabula.read_pdf(
            os.path.join(config.UPLOAD_FOLDER, pdf_filename),
            output_format='json',
            java_options=["-Djava.awt.headless=true"],
            multiple_tables=True,
            pages='all',
            silent=True
        )

        sanitized_infos = remove_useless_lines_from_file(infos)
        needs = tables.merge_all_tables(sanitized_infos)
    except Exception as e:
        messages.append('Erreur lors de la generation des infos a partir du fichier pdf: ' + str(e))
        return None

    try:
        os.remove(os.path.join(config.UPLOAD_FOLDER, pdf_filename))
    except Exception as e:
        print('Impossible de supprimer le fichier: ', e)
    
    return needs