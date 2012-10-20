Unofficial Dailymotion sdk for Python
=====================================


The API will not do calls before a value is needed generally pratically 
the following code::

  >>> dailymotion = Dailymotion()
  >>> subtitle = next(dailymotion.video('xuf2hc').subtitles)

This is not important but kind of useful to know if you want to discover
the API through Python REPL. When you first retrieve a Python object, 
like in the following code::

  >>> dailymotion.video('xuf2hc')

The object is not populated yet, to discover the default available attributes
in REPL, hit any attribute that is not a base attribute of the class, try 
something improbable, like the following::

 >>> subtitle.an_egg_over_a_wall

Be funky and creative. This will trigger the network call and will populate the 
object you can now use autocompletion or inspect ``__dict__``::

 >>> subtitle.__dict__

This is not true for objects you retrieve via iteration, their populated at 
instantiation time. 

If you want to discover the API from Python, begin with plural methods in 
``Dailymotion`` then iterate over the generator with next for instance like
it's done in the above example or rtfc or 
`rtfd <http://www.dailymotion.com/doc/api/graph-api.html>`.

Current code covers only read API, no edits not deletes.

TODO: replace __iter__ by __call__ with args as the properties of the element
wanted, right now only the default properties are returned which can come short,
but a good start.
