

class AppendEntries:

    def __init__(self, term, prevLogIndex, prevLogTerm):
        assert isinstance(term, int)
        self._term = term
        assert isinstance(prevLogIndex, int)
        self._prevLogIndex = prevLogIndex
        assert isinstance(prevLogTerm, int)
        self._prevLogTerm = prevLogTerm

    def getTerm(self):
        return self._term

    def getPrevLogIndex(self):
        return self._prevLogIndex


class AppendEntriesReply:
    def __init__(self, term, success):
        assert isinstance(term, int)
        assert isinstance(success, bool)
        self.term = term
        self.success = success

