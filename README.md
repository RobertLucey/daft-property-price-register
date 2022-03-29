Daft Property Price Register
============================

Easy way of interacting with daft property price register.

To enter a debugger with access to all sale data run `make load` (if working from the repo) or `load_daft` if you have installed the package and you will have access to the variable `sales` which contains everything

Installation
------------

`pip install daft-property-price-register`


Usage
-----

```python

>>> from daft_property_price_register.models.daft_sale import DaftSales
>>> sales = DaftSales.load()
>>> sales[0].serialize()
{'address': '11 Latchford Green, Castaheany, Clonee, Clonee, Co. Dublin',
 'bathrooms': 3.0,
 'bedrooms': 2.0,
 'date': '21/05/21',
 'not_full_market_price': False,
 'price': 310000,
 'property_type': 'Terraced House'}
```
