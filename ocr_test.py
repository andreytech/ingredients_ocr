import click
from flask import Blueprint

import pandas as pd

ocr_test_bp = Blueprint('ocr', __name__)

@ocr_test_bp.cli.command('test')
@click.argument('name')
def ocr_test(name):

    print("farsh: {}".format(name))

@ocr_test_bp.cli.command('csv')
def csv_parse():
    csv_path = 'nabori_sredstv_dlia_lica.csv'
    data = pd.read_csv(csv_path, low_memory=False, encoding='windows-1251', sep=';', names=['name', 'link', 'brand', 'description', 'images'])
    for i,row in data.iterrows():
        if i == 0:
            continue
        # print(vars(row))
        print(row['description'])
        print('------------------------------------------')

        # sql = "INSERT INTO employee.employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sql, tuple(row))
        # print("Record inserted")
        # # the connection is not auto committed by default, so we must commit to save our changes
        # conn.commit()



