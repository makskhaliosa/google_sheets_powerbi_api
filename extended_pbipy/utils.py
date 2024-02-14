def remove_empty_values(
    d: dict,
) -> dict:
    """
    Recursively remove keys with a value of '', [],
    `None` or `{}` from a dictionary.
    If the result of removing `None` is `{}`, then this is removed until
    only keys with values remain.

    Parameters
    ----------
    `d` : `dict`
        dict to remove None or empty dicts from.

    Returns
    -------
    `dict`
        dict with `None` or `{}` removed.
    """

    new_d = {}

    for k, v in d.items():
        if isinstance(v, dict):
            v = remove_empty_values(v)
        if v:
            new_d[k] = v

    return new_d
