import hashlib
import os
import glob
import tarfile
import statistics

import pandas as pd
from cached_property import cached_property

from daft_property_price_register.utils import isnan


class DaftSales():

    def __init__(self, *args, **kwargs):
        self._data = kwargs.get('data', [])

    def contains(self, sale):
        return sale.content_hash in self.content_hashes

    def __getitem__(self, i):
        return self._data[i]

    def __iter__(self):
        return (i for i in self._data)

    def __len__(self):
        return len(self._data)

    def append(self, data):
        self._data.append(data)

    def extend(self, data):
        self._data.extend(data)

    def serialize(self):
        return [
            d.serialize() for d in self
        ]

    @cached_property
    def content_hashes(self):
        return set([d.content_hash for d in self._data])

    @staticmethod
    def from_file(filepath):
        data = None

        ext = os.path.splitext(filepath)[-1]
        if ext in {'.tgz', '.gz'}:
            tar = tarfile.open(filepath, 'r:gz')
            tar.extractall(path=os.path.dirname(filepath))
            tar.close()

            data = []
            for sub_file in glob.iglob(
                os.path.dirname(filepath) + '/**',
                recursive=True
            ):
                ext = os.path.splitext(sub_file)[-1]
                if ext == '.csv':
                    csv_data = pd.read_csv(
                        sub_file.replace('.csv.tgz', '.csv'),
                        encoding='ISO-8859-1'
                    ).to_dict(orient='records')
                    data.extend(csv_data)
        elif ext in {'.csv'}:
            data = pd.read_csv(
                filepath,
                encoding='ISO-8859-1'
            ).to_dict(orient='records')
        else:
            raise Exception()

        sales = DaftSales()
        for sales_dict in data:
            obj = DaftSale.parse(
                sales_dict
            )
            sales.append(obj)

        return sales

    @staticmethod
    def from_dir(dirpath):
        sales = DaftSales()
        search_dir = f'{dirpath}/**'
        for filename in glob.iglob(search_dir, recursive=True):
            if os.path.splitext(filename)[-1] not in {'.tgz', '.gz'}:
                continue
            sales.extend(
                DaftSales.from_file(
                    filename
                )
            )

        return sales

    def load():
        import daft_property_price_register
        return DaftSales.from_dir(
            os.path.join(daft_property_price_register.__path__[0], 'resources')
        )

    def save(self, filepath):
        df = pd.DataFrame(self.serialize())
        df = df.drop_duplicates(subset=['date', 'address', 'price'])
        df.to_csv(filepath)

    @property
    def average_price(self):
        return statistics.mean([s.price for s in self])


class DaftSale():

    def __init__(self, **kwargs):
        self.address = kwargs.get('address', None)
        self.price = kwargs.get('price', None)
        self.not_full_market_price = '**' in kwargs.get('price', '') if isinstance(kwargs['price'], str) else kwargs['not_full_market_price']
        if self.price is not None and isinstance(self.price, str):
            self.price = int(self.price.replace(',', '').replace('â\x82¬', '').replace('€', '').replace(' **', ''))
        self.date = kwargs.get('date', None)
        self.property_type = kwargs.get('property_type', None) if not isnan(kwargs.get('property_type', None)) else None

        self.bedrooms = kwargs.get('bedrooms', None)
        self.bathrooms = kwargs.get('bathrooms', None)


    @staticmethod
    def parse(data):
        if isinstance(data, DaftSale):
            return data

        return DaftSale(
            **data
        )

    def serialize(self):
        return {
            'address': self.address,
            'price': self.price,
            'date': self.date,
            'property_type': self.property_type,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'not_full_market_price': self.not_full_market_price
        }

    @property
    def content_hash(self):
        return hashlib.md5(
            str(self.serialize()).encode()
        ).hexdigest()
