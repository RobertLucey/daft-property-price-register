import os

import pandas

from daft_property_price_register.models.daft_sale import DaftSales


def main():

    sales = DaftSales.load()

    print('Loaded %s sales' % (len(sales)))
    print('Do something with the data in the variable \'sales\'...')

    import pdb; pdb.set_trace()
    pass


if __name__ == '__main__':
    main()
