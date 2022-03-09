import os
from urllib.request import urlopen

import bs4
import pandas

from daft_property_price_register.constants import DAFT_URL
from daft_property_price_register.models.daft_sale import DaftSale


def main():

    if os.path.exists('/tmp/daft.csv'):
        print('Merging with existing')
        raw_data = pandas.read_csv('/tmp/daft.csv').to_dict(orient='records')
        data = []
        for single_sale in raw_data:
            data.append(
                DaftSale(
                    **single_sale
                )
            )
        existing_hashes = set([s.content_hash for s in data])
    else:
        data = []
        existing_hashes = set()

    for page_num in range(20000):
        print('Page #%s' % (page_num))
        source = urlopen(DAFT_URL.format(page_num=page_num))
        soup = bs4.BeautifulSoup(source, 'html.parser')

        results = soup.find_all('div', {'class': 'priceregister-searchresult'})

        for result in results:
            address = ' '.join(
                result.find(
                    'span',
                    {'class': 'priceregister-address'}
                ).text.strip().replace('\n', ' ').split()
            )
            extra_details = [
                i.strip() for i in result.find(
                    'span',
                    {'class': 'priceregister-dwelling-details'}
                ).text.split('|')
            ]

            bedrooms = None
            bathrooms = None
            if len(extra_details) == 5:
                # FIXME super lazy, don't want to think about it
                if 'bedrooms' in extra_details[3].lower():
                    bedrooms = int(extra_details[3].lower().replace('bedrooms', '').strip())
                if 'bedrooms' in extra_details[4].lower():
                    bedrooms = int(extra_details[4].lower().replace('bedrooms', '').strip())
                if 'bathrooms' in extra_details[3].lower():
                    bathrooms = int(extra_details[3].lower().replace('bathrooms', '').strip())
                if 'bathrooms' in extra_details[4].lower():
                    bathrooms = int(extra_details[4].lower().replace('bathrooms', '').strip())
                sale = DaftSale(
                    address=address,
                    price=extra_details[0],
                    date=extra_details[1],
                    property_type=extra_details[2],
                    bedrooms=bedrooms,
                    bathrooms=bathrooms
                )
            elif len(extra_details) == 4:
                if 'bedrooms' in extra_details[3].lower():
                    bedrooms = int(extra_details[3].lower().replace('bedrooms', '').strip())
                if 'bathrooms' in extra_details[3].lower():
                    bathrooms = int(extra_details[3].lower().replace('bathrooms', '').strip())
                sale = DaftSale(
                    address=address,
                    price=extra_details[0],
                    date=extra_details[1],
                    property_type=extra_details[2],
                    bedrooms=extra_details[3],
                )
            elif len(extra_details) == 3:
                sale = DaftSale(
                    address=address,
                    price=extra_details[0],
                    date=extra_details[1],
                    property_type=extra_details[2],
                )
            else:
                raise Exception()

            if sale.content_hash not in existing_hashes:
                print(sale.content_hash)
                data.append(sale)

        if page_num % 100 == 0:
            df = pandas.DataFrame([d.serialize() for d in data])
            df.to_csv('/tmp/daft.csv')

    import pdb; pdb.set_trace()
    pass



if __name__ == '__main__':
    main()
