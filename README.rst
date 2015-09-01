Extends `collective.portlet.embed`_ changing the portlet behavior.
If an **opt-out** cookie (or a DNS header) is present and the portlet is rendering externas resources,
do not render the portlet.

Hot it works
============

Simply adding this add-on in your buildout will change all of the collective.portlet.embed instances as follow:
if...

* a cookie named ``embed-optout`` is present with value ``true``, or
* the ``DNT`` (`Do Not Track`_) header is set

...the portlet content is parsed looking for potentially malicious contents.
If contents that load external sites are found, the portlet will not be rendered.

Limitations
===========

Tricks to overtake the security check are many.

A malicious portlet creator always can (for example)
put in the portlet a JavaScript that create an ``iframe`` that load external contents and the
security check will not be able to find it.

Credits
=======

Developed with the support of `Regione Emilia Romagna`__;
Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/

.. _`collective.portlet.embed`: https://pypi.python.org/pypi/collective.portlet.embed
.. _`Do Not Track`: https://en.wikipedia.org/wiki/Do_Not_Track

