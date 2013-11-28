# Ares_util #

## Představení

Jednoduchý nástroj pro validaci<sup>1</sup> českého IČ. U předaného čísla je nejdříve ověřen jeho kontrolní součet (viz [Reference](https://github.com/illagrenan/ares_util/master/README.md#reference)) a dle výsledku se následně zasílá požadavek na [ARES XML API](http://wwwinfo.mfcr.cz/ares/ares_xml.html.cz).

Pokud je IČ validní, vrací nástroj `dict` se základními údaji o firmě (obchodní název, adresa).


> Doporučuji prostudovat [Podmínky provozu ARES API](http://wwwinfo.mfcr.cz/ares/ares_podminky.html.cz), zejména pak:
> 
> Ministerstvo financí vyhrazuje právo omezit nebo znemožnit přístup k www aplikaci ARES uživatelům, kteří:
> * odešlou k vyřízení více než 1000 dotazů v době od 8:00 hod. do 18:00 hod.,
> * odešlou k vyřízení více než 5000 dotazů v době od 18:00 hod. do 8:00 hod. rána následujícího dne,
> * opakovaně posílají nesprávně vyplněné dotazy,
> * opakovaně posílají stejné dotazy,
> * mají větší počet současně zadaných dotazů (pro automatizované XML dotazy),
> * obcházejí povolené limity využíváním dotazování z většího množství IP adres,
> * automatizovaně propátrávají databázi náhodnými údaji nebo generují většinu nesprávných dotazů.


## Instalace

```shell
pip install ares-util
```

## Použití ##

> Testováno v Python `2.7.*`.

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

- [ ] Dokončit podporu pro Django (validátory formulářových polí).
- [ ] Travis CI, Coveralls, Crate.io.
- [ ] Ověřit a případně vyřešit kompatibilitu s Python 3.

# Reference
1. http://www.abclinuxu.cz/blog/bloK/2008/10/kontrola-ic, http://latrine.dgx.cz/jak-overit-platne-ic-a-rodne-cislo

# Technické informace

XML response z ARESu je zpracována pomocí [xmltodict](https://github.com/martinblech/xmltodict).

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
