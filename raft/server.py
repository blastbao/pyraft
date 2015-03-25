
from .state import RaftPersistentState
from .rpctypes import *


class RaftServer:

    def __init__(self, persistentState):
        assert isinstance(persistentState, RaftPersistentState)
        self._persistentState = persistentState

    def getPersistentState(self):
        return self._persistentState

    def processRpc(self, rpc):
        if isinstance(rpc, AppendEntries):
            success = self._processRpc_AppendEntries(rpc)
            return AppendEntriesReply(
                self._persistentState.getCurrentTerm(),
                success
                )
        else:
            raise Exception, "oops!"


    def _processRpc_AppendEntries(self, appendEntries):
        # Receiver step 1
        if appendEntries.getTerm() < self._persistentState.getCurrentTerm():
            return False
        # Receiver step 2
        logEntriesStore = self._persistentState.getLogEntriesStore()
        if logEntriesStore.getLastIndex() < appendEntries.getPrevLogIndex():
            return False
        #
        return True


