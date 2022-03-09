import os

LOG_LOCATION = '/var/log/daft_property_price_register/daft_property_price_register.log' if os.getenv('TEST_ENV') != 'True' else '/tmp/log/daft_property_price_register/daft_property_price_register.log'

DAFT_URL = 'https://ww1.daft.ie/price-register/?d_rd=1&min_price=0&max_price=500000000&pagenum={page_num}'
