# Ares_util #

## Představení

## Instalace

```shell
pip install ares-util
```


## Použití ##


```shell
$ python
>>> from ares_util.ares import call_ares
>>> call_ares(42)
False
>>> call_ares(27074358)
{'legal': {'company_name': u'Asseco Central Europe, a.s.', 'business_number': 27074358}, 'address': {'city': u'Praha', 'region': u'Hlavn\xed m\u011bsto Praha', 'street':
u'Bud\u011bjovick\xe1 778/3a', 'city_part': u'Michle'}}
```

### Django podpora

> Viz TODOs.

# TODOs

- [ ] Dokončit podporu pro Django (validátory formulářových polí)
- [ ] Travis CI, Coveralls, Crate.io

# Licence

The MIT License (MIT)

Copyright (c) 2013 Vašek Dohnal

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
