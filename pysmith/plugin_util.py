def lambda_or_metadata_selector(selector):
    """
        Ensures that the given selector is a function. If a str is provided, it will be converted into a function that
        queries the file's :attr:`~pysmith.metadata` for the provided key.

        :param selector: The selector.
        :type layout_selector: str or func(:class:`~pysmith.FileInfo`)
        :returns: func(:class:`~pysmith.FileInfo`)
    """

    if isinstance(selector, str):
        return lambda f: f.metadata[selector]
    elif callable(selector):
        return selector

    raise ValueError("Selector is not a str or callable")
