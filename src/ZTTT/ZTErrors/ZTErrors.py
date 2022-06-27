# Z Errors


class ZTError(Exception):
    pass


class ZTBadFunctionCall(AttributeError, ZTError):
    pass


class ZTGameException(ZTError):
    pass


class ZTWrongInput(ValueError, ZTGameException):
    pass
