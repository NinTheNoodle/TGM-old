def call_auto_callable(auto_call, inst, cls, _used_names=None):
    """Call the mapped function for each auto_call instance on the object.

    Every class attribute for the given instance that has an key in the
    auto_call dictionary will have its mapped function called.
    The mapped function will be called with the created instance, the class
    the object was defined upon and the name of the attribute that holds it.
    """
    if _used_names is None:
        _used_names = set()

    for attr, obj in cls.__dict__.items():
        if attr in _used_names:
            continue
        try:
            call = auto_call[obj]
        except (KeyError, TypeError):
            pass
        else:
            call(inst, cls, attr)

    _used_names.update(cls.__dict__.keys())

    for base in cls.mro()[1:]:
        call_auto_callable(auto_call, inst, base, _used_names)


class AttrDict(dict):
    """An attribute accessible dictionary."""
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self[key] = value

    def __delattr__(self, item):
        del self[item]
