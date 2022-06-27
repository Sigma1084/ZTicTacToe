from .ZTEngines import ZTEngineFirst
from .ZTEngines import ZTPlayerFirst


class PvC(ZTEngineFirst, ZTPlayerFirst):
    def __init__(self, _engine_first: bool = True):
        self.__engine_first = _engine_first

        if self.__engine_first:
            self.parent = ZTEngineFirst
            ZTEngineFirst.__init__(self)

        else:
            self.parent = ZTPlayerFirst
            ZTPlayerFirst.__init__(self)

    def play(self, pos: int):
        self.parent.play(self, pos)
