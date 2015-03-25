
class LogEntriesStore:

    def getLastIndex(self):
        "Get the index of the last log entry."
        raise NotImplementedError("Method must be implemented by subclass")

    def deleteFromIndex(self, logIndex):
        "Delete existing entry at given index and all that follow."
        raise NotImplementedError("Method must be implemented by subclass")

    def getTermForIndex(self, logIndex):
        "Get the term for entry at given index."
        raise NotImplementedError("Method must be implemented by subclass")



class RaftPersistentState:

    def __init__(self, currentTerm, logEntriesStore):
        assert isinstance(currentTerm, int)
        self._currentTerm = currentTerm
        assert isinstance(logEntriesStore, LogEntriesStore)
        self._logEntriesStore = logEntriesStore

    def getCurrentTerm(self):
        return self._currentTerm

    def getLogEntriesStore(self):
        return self._logEntriesStore
        
