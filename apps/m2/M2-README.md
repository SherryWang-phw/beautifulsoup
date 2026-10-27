# Milestone-2

## API functions I used in Milestone 1 and in Part-1 of Milestone-2

| API                     | Class/Definition                  | File                | Start line |
| ----------------------- | --------------------------------- | ------------------- | ---------: |
| `BeautifulSoup`       | `BeautifulSoup`class            | `bs4/__init__.py` |        133 |
| `BeautifulSoup()`     | `BeautifulSoup.__init__`        | `bs4/__init__.py` |        209 |
| `SoupStrainer`        | `SoupStrainer`class             | `bs4/filter.py`   |        313 |
| `SoupStrainer()`      | `SoupStrainer.__init__`         | `bs4/filter.py`   |        345 |
| `find_parent()`       | `PageElement.find_parent`       | `bs4/element.py`  |        992 |
| `find_next_sibling()` | `PageElement.find_next_sibling` | `bs4/element.py`  |        803 |
| `find_all()`          | `Tag.find_all`                  | `bs4/element.py`  |       2715 |
| `find_all()`          | `ElementFilter.find_all`        | `bs4/filter.py`   |        137 |
| `find()`              | `Tag.find`                      | `bs4/element.py`  |       2684 |
| `find()`              | `ElementFilter.find`            | `bs4/filter.py`   |        123 |
| `get()`               | `Tag.get`                       | `bs4/element.py`  |       2160 |
| `prettify()`          | `Tag.prettify`                  | `bs4/element.py`  |       2601 |

### BeautifulSoup  -- bs4/__init__.py line133-line1144

### bs4/__init__.py line209

```python
    def __init__(
        self,
        markup: _IncomingMarkup = "",
        features: Optional[Union[str, Sequence[str]]] = None,
        builder: Optional[Union[TreeBuilder, Type[TreeBuilder]]] = None,
        parse_only: Optional[SoupStrainer] = None,
        from_encoding: Optional[_Encoding] = None,
        exclude_encodings: Optional[_Encodings] = None,
        element_classes: Optional[Dict[Type[PageElement], Type[PageElement]]] = None,
        **kwargs: Any,
    ):
        """Constructor.

        :param markup: A string or a file-like object representing
         markup to be parsed.

        :param features: Desirable features of the parser to be
         used. This may be the name of a specific parser ("lxml",
         "lxml-xml", "html.parser", or "html5lib") or it may be the
         type of markup to be used ("html", "html5", "xml"). It's
         recommended that you name a specific parser, so that
         Beautiful Soup gives you the same results across platforms
         and virtual environments.

        :param builder: A TreeBuilder subclass to instantiate (or
         instance to use) instead of looking one up based on
         `features`. You only need to use this if you've implemented a
         custom TreeBuilder.

        :param parse_only: A SoupStrainer. Only parts of the document
         matching the SoupStrainer will be considered. This is useful
         when parsing part of a document that would otherwise be too
         large to fit into memory.

        :param from_encoding: A string indicating the encoding of the
         document to be parsed. Pass this in if Beautiful Soup is
         guessing wrongly about the document's encoding.

        :param exclude_encodings: A list of strings indicating
         encodings known to be wrong. Pass this in if you don't know
         the document's encoding but you know Beautiful Soup's guess is
         wrong.

        :param element_classes: A dictionary mapping BeautifulSoup
         classes like Tag and NavigableString, to other classes you'd
         like to be instantiated instead as the parse tree is
         built. This is useful for subclassing Tag or NavigableString
         to modify default behavior.

        :param kwargs: For backwards compatibility purposes, the
         constructor accepts certain keyword arguments used in
         Beautiful Soup 3. None of these arguments do anything in
         Beautiful Soup 4; they will result in a warning and then be
         ignored.

         Apart from this, any keyword arguments passed into the
         BeautifulSoup constructor are propagated to the TreeBuilder
         constructor. This makes it possible to configure a
         TreeBuilder by passing in arguments, not just by saying which
         one to use.
        """
        if "convertEntities" in kwargs:
            del kwargs["convertEntities"]
            warnings.warn(
                "BS4 does not respect the convertEntities argument to the "
                "BeautifulSoup constructor. Entities are always converted "
                "to Unicode characters."
            )

        if "markupMassage" in kwargs:
            del kwargs["markupMassage"]
            warnings.warn(
                "BS4 does not respect the markupMassage argument to the "
                "BeautifulSoup constructor. The tree builder is responsible "
                "for any necessary markup massage."
            )

        if "smartQuotesTo" in kwargs:
            del kwargs["smartQuotesTo"]
            warnings.warn(
                "BS4 does not respect the smartQuotesTo argument to the "
                "BeautifulSoup constructor. Smart quotes are always converted "
                "to Unicode characters."
            )

        if "selfClosingTags" in kwargs:
            del kwargs["selfClosingTags"]
            warnings.warn(
                "Beautiful Soup 4 does not respect the selfClosingTags argument to the "
                "BeautifulSoup constructor. The tree builder is responsible "
                "for understanding self-closing tags."
            )

        if "isHTML" in kwargs:
            del kwargs["isHTML"]
            warnings.warn(
                "Beautiful Soup 4 does not respect the isHTML argument to the "
                "BeautifulSoup constructor. Suggest you use "
                "features='lxml' for HTML and features='lxml-xml' for "
                "XML."
            )

        def deprecated_argument(old_name: str, new_name: str) -> Optional[Any]:
            if old_name in kwargs:
                warnings.warn(
                    'The "%s" argument to the BeautifulSoup constructor '
                    'was renamed to "%s" in Beautiful Soup 4.0.0'
                    % (old_name, new_name),
                    DeprecationWarning,
                    stacklevel=3,
                )
                return kwargs.pop(old_name)
            return None

        parse_only = parse_only or deprecated_argument("parseOnlyThese", "parse_only")
        if parse_only is not None:
            # Issue a warning if we can tell in advance that
            # parse_only will exclude the entire tree.
            if parse_only.excludes_everything:
                warnings.warn(
                    f"The given value for parse_only will exclude everything: {parse_only}",
                    UserWarning,
                    stacklevel=3,
                )

        from_encoding = from_encoding or deprecated_argument(
            "fromEncoding", "from_encoding"
        )

        if from_encoding and isinstance(markup, str):
            warnings.warn(
                "You provided Unicode markup but also provided a value for from_encoding. Your from_encoding will be ignored."
            )
            from_encoding = None

        self.element_classes = element_classes or dict()

        # We need this information to track whether or not the builder
        # was specified well enough that we can omit the 'you need to
        # specify a parser' warning.
        original_builder = builder
        original_features = features

        builder_class: Type[TreeBuilder]
        if isinstance(builder, type):
            # A builder class was passed in; it needs to be instantiated.
            builder_class = builder
            builder = None
        elif builder is None:
            if isinstance(features, str):
                features = [features]
            if features is None or len(features) == 0:
                features = self.DEFAULT_BUILDER_FEATURES
            possible_builder_class = builder_registry.lookup(*features)
            if possible_builder_class is None:
                raise FeatureNotFound(
                    "Couldn't find a tree builder with the features you "
                    "requested: %s. Do you need to install a parser library?"
                    % ",".join(features)
                )
            builder_class = possible_builder_class

        # At this point either we have a TreeBuilder instance in
        # builder, or we have a builder_class that we can instantiate
        # with the remaining **kwargs.
        if builder is None:
            builder = builder_class(**kwargs)
            if (
                not original_builder
                and not (
                    original_features == builder.NAME
                    or (
                        isinstance(original_features, str)
                        and original_features in builder.ALTERNATE_NAMES
                    )
                )
                and markup
            ):
                # The user did not tell us which TreeBuilder to use,
                # and we had to guess. Issue a warning.
                if builder.is_xml:
                    markup_type = "XML"
                else:
                    markup_type = "HTML"

                # This code adapted from warnings.py so that we get the same line
                # of code as our warnings.warn() call gets, even if the answer is wrong
                # (as it may be in a multithreading situation).
                caller = None
                try:
                    caller = sys._getframe(1)
                except ValueError:
                    pass
                if caller:
                    globals = caller.f_globals
                    line_number = caller.f_lineno
                else:
                    globals = sys.__dict__
                    line_number = 1
                filename = globals.get("__file__")
                if filename:
                    fnl = filename.lower()
                    if fnl.endswith((".pyc", ".pyo")):
                        filename = filename[:-1]
                if filename:
                    # If there is no filename at all, the user is most likely in a REPL,
                    # and the warning is not necessary.
                    values = dict(
                        filename=filename,
                        line_number=line_number,
                        parser=builder.NAME,
                        markup_type=markup_type,
                    )
                    warnings.warn(
                        GuessedAtParserWarning.MESSAGE % values,
                        GuessedAtParserWarning,
                        stacklevel=2,
                    )
        else:
            if kwargs:
                warnings.warn(
                    "Keyword arguments to the BeautifulSoup constructor will be ignored. These would normally be passed into the TreeBuilder constructor, but a TreeBuilder instance was passed in as `builder`."
                )

        self.builder = builder
        self.is_xml = builder.is_xml
        self.known_xml = self.is_xml
        self._namespaces = dict()
        self.parse_only = parse_only

        if hasattr(markup, "read"):  # It's a file-type object.
            markup = markup.read()
        elif not isinstance(markup, (bytes, str)) and not hasattr(markup, "__len__"):
            raise TypeError(
                f"Incoming markup is of an invalid type: {markup!r}. Markup must be a string, a bytestring, or an open filehandle."
            )
        elif len(markup) <= 256 and (
            (isinstance(markup, bytes) and b"<" not in markup and b"\n" not in markup)
            or (isinstance(markup, str) and "<" not in markup and "\n" not in markup)
        ):
            # Issue warnings for a couple beginner problems
            # involving passing non-markup to Beautiful Soup.
            # Beautiful Soup will still parse the input as markup,
            # since that is sometimes the intended behavior.
            if not self._markup_is_url(markup):
                self._markup_resembles_filename(markup)

        # At this point we know markup is a string or bytestring.  If
        # it was a file-type object, we've read from it.
        markup = cast(_RawMarkup, markup)

        rejections = []
        success = False
        for (
            self.markup,
            self.original_encoding,
            self.declared_html_encoding,
            self.contains_replacement_characters,
        ) in self.builder.prepare_markup(
            markup, from_encoding, exclude_encodings=exclude_encodings
        ):
            self.reset()
            self.builder.initialize_soup(self)
            try:
                self._feed()
                success = True
                break
            except ParserRejectedMarkup as e:
                rejections.append(e)
                pass

        if not success:
            other_exceptions = [str(e) for e in rejections]
            raise ParserRejectedMarkup(
                "The markup you provided was rejected by the parser. Trying a different parser or a different encoding may help.\n\nOriginal exception(s) from parser:\n "
                + "\n ".join(other_exceptions)
            )

        # Clear out the markup and remove the builder's circular
        # reference to this object.
        self.markup = None
        self.builder.soup = None
```

### SoupStrainer -- filter.py line313-line682

### bs4/filter.py line345

```python
def __init__(
        self,
        name: Optional[_StrainableElement] = None,
        attrs: Dict[str, _StrainableAttribute] = {},
        string: Optional[_StrainableString] = None,
        **kwargs: _StrainableAttribute,
    ):
        if string is None and "text" in kwargs:
            string = cast(Optional[_StrainableString], kwargs.pop("text"))
            warnings.warn(
                "As of version 4.11.0, the 'text' argument to the SoupStrainer constructor is deprecated. Use 'string' instead.",
                DeprecationWarning,
                stacklevel=2,
            )

        self.name_rules = cast(
            List[TagNameMatchRule], list(self._make_match_rules(name, TagNameMatchRule))
        )
        self.attribute_rules = defaultdict(list)

        if not isinstance(attrs, dict):
            # Passing something other than a dictionary as attrs is
            # sugar for matching that thing against the 'class'
            # attribute.
            attrs = {"class": attrs}

        for attrdict in attrs, kwargs:
            for attr, value in attrdict.items():
                if attr == "class_" and attrdict is kwargs:
                    # If you pass in 'class_' as part of kwargs, it's
                    # because class is a Python reserved word. If you
                    # pass it in as part of the attrs dict, it's
                    # because you really are looking for an attribute
                    # called 'class_'.
                    attr = "class"

                if value is None:
                    value = False
                for rule_obj in self._make_match_rules(value, AttributeValueMatchRule):
                    self.attribute_rules[attr].append(
                        cast(AttributeValueMatchRule, rule_obj)
                    )

        self.string_rules = cast(
            List[StringMatchRule], list(self._make_match_rules(string, StringMatchRule))
        )
```

### find_parent-- bs4/element.py line992-line1020

```python

    def find_parent(
        self,
        name: _FindMethodName = None,
        attrs: _StrainableAttributes = {},
        **kwargs: _StrainableAttribute,
    ) -> _AtMostOneElement:
        """Find the closest parent of this PageElement that matches the given
        criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param self: Whether the PageElement itself should be considered
           as one of its 'parents'.
        :kwargs: Additional filters on attribute values.
        """
        # NOTE: We can't use _find_one because findParents takes a different
        # set of arguments.
        r = None
        results = self.find_parents(
            name, attrs, 1, _stacklevel=3, **kwargs
        )
        if results:
            r = results[0]
        return r

    findParent = _deprecated_function_alias("findParent", "find_parent", "4.0.0")
```

### find_next_sibling -- bs4/element.py line803-line825

```python
def find_next_sibling(
        self,
        name: _FindMethodName = None,
        attrs: _StrainableAttributes = {},
        string: Optional[_StrainableString] = None,
        **kwargs: _StrainableAttribute,
    ) -> _AtMostOneElement:
        """Find the closest sibling to this PageElement that matches the
        given criteria and appears later in the document.

        All find_* methods take a common set of arguments. See the
        online documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a `NavigableString` with specific text.
        :kwargs: Additional filters on attribute values.
        """
        return self._find_one(self.find_next_siblings, name, attrs, string, **kwargs)

    findNextSibling = _deprecated_function_alias(
        "findNextSibling", "find_next_sibling", "4.0.0"
  
  
  
  
    )
```

### find_all -- bs4/element.py line2715-line2748

```python

    def find_all(
        self,
        name: _FindMethodName = None,
        attrs: _StrainableAttributes = {},
        recursive: bool = True,
        string: Optional[_StrainableString] = None,
        limit: Optional[int] = None,
        _stacklevel: int = 2,
        **kwargs: _StrainableAttribute,
    ) -> _QueryResults:
        """Look in the children of this `PageElement` and find all
        `PageElement` objects that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param recursive: If this is True, find_all() will perform a
            recursive search of this PageElement's children. Otherwise,
            only the direct children will be considered.
        :param limit: Stop looking after finding this many results.
        :param _stacklevel: Used internally to improve warning messages.
        :kwargs: Additional filters on attribute values.
        """
        generator = self.descendants
        if not recursive:
            generator = self.children
        return self._find_all(
            name, attrs, string, limit, generator, _stacklevel=_stacklevel + 1, **kwargs
        )

    findAll = _deprecated_function_alias("findAll", "find_all", "4.0.0")
    findChildren = _deprecated_function_alias("findChildren", "find_all", "3.0.0")
```

### find_all -- bs4/filter.py line137-line156

```python
    def find_all(
        self, generator: Iterator[PageElement], limit: Optional[int] = None
    ) -> _QueryResults:
        """A lower-level equivalent of :py:meth:`Tag.find_all`.

        You can pass in your own generator for iterating over
        `PageElement` objects. Only elements that match this
        `ElementFilter` will be returned in the :py:class:`ResultSet`.

        :param generator: A way of iterating over `PageElement`
            objects.

        :param limit: Stop looking after finding this many results.
        """
        results: _QueryResults = ResultSet(self)
        for match in self.filter(generator):
            results.append(match)
            if limit is not None and len(results) >= limit:
                break
        return results
```

### find -- bs4/element.py line2684-line2713

```python

    def find(
        self,
        name: _FindMethodName = None,
        attrs: _StrainableAttributes = {},
        recursive: bool = True,
        string: Optional[_StrainableString] = None,
        **kwargs: _StrainableAttribute,
    ) -> _AtMostOneElement:
        """Look in the children of this PageElement and find the first
        PageElement that matches the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param recursive: If this is True, find() will perform a
            recursive search of this Tag's children. Otherwise,
            only the direct children will be considered.
        :param string: A filter on the `Tag.string` attribute.
        :param limit: Stop looking after finding this many results.
        :kwargs: Additional filters on attribute values.
        """
        r = None
        results = self.find_all(name, attrs, recursive, string, 1, _stacklevel=3, **kwargs)
        if results:
            r = results[0]
        return r

    findChild = _deprecated_function_alias("findChild", "find", "3.0.0")
```

### find -- bs4/filter.py line123-line135

```python
def find(self, generator: Iterator[PageElement]) -> _AtMostOneElement:
        """A lower-level equivalent of :py:meth:`Tag.find`.

        You can pass in your own generator for iterating over
        `PageElement` objects. The first one that matches this
        `ElementFilter` will be returned.

        :param generator: A way of iterating over `PageElement`
            objects.
        """
        for match in self.filter(generator):
            return match
        return None
```

### get -- bs4/element.py line2160-line2171

```python

    def get(
        self, key: str, default: Optional[_AttributeValue] = None
    ) -> Optional[_AttributeValue]:
        """Returns the value of the 'key' attribute for the tag, or
        the value given for 'default' if it doesn't have that
        attribute.

        :param key: The attribute to look for.
        :param default: Use this value if the attribute is not present
            on this `Tag`.
        """
        return self.attrs.get(key, default)
```

### prettify -- bs4/element.py line2601-line2617

```python

    def prettify(
        self,
        encoding: Optional[_Encoding] = None,
        formatter: _FormatterOrName = "minimal",
    ) -> Union[str, bytes]:
        """Pretty-print this `Tag` as a string or bytestring.

        :param encoding: The encoding of the bytestring, or None if you want Unicode.
        :param formatter: A Formatter object, or a string naming one of
            the standard formatters.
        :return: A string (if no ``encoding`` is provided) or a bytestring
            (otherwise).
        """
        if encoding is None:
            return self.decode(indent_level=0, formatter=formatter)
        else:
            return self.encode(encoding=encoding, indent_level=0, formatter=formatter)
```
