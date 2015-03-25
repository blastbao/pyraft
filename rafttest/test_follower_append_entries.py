# AppendEntries RPC
# Invoked by leader to replicate log entries (#5.3); also used as heartbeat
# (#5.2).

import unittest

from raft import *


class SimpleLogEntriesStore(LogEntriesStore):

    def __init__(self):
        self._log = []

    def _setLog(self, log):
        self._log = log

    def getLastIndex(self):
        return len(self._log)


TEST_LEADER_TERM = 8

class FollowerAppendEntriesTest(unittest.TestCase):

    def setUp(self):
        self.followerLogEntriesStore = SimpleLogEntriesStore()
        self.follower = RaftServer(
            RaftPersistentState(TEST_LEADER_TERM, self.followerLogEntriesStore)
            )

    def _makeAppendEntries(
            self, term=TEST_LEADER_TERM, prevLogIndex=-1, prevLogTerm=-1
            ):
        return AppendEntries(term, prevLogIndex, prevLogTerm)

    # 1. Reply false if term < currentTerm (#5.1)
    def test_leaderTerm_lt_currentTerm(self):
        followerTerm = self.follower.getPersistentState().getCurrentTerm()
        appendEntries = self._makeAppendEntries(
            term = followerTerm - 1
            )
        reply = self.follower.processRpc(appendEntries)
        self.assertIsInstance(reply, AppendEntriesReply)
        self.assertEqual(reply.term, followerTerm)
        self.assertFalse(reply.success)

    # 2. Reply false if log doesn't contain an entry at prevLogIndex
    #    whose term matches prevLogTerm (#5.3)
    # Note: the above language is slightly ambiguous but I'm assuming that
    # this step refers strictly to the follower's log not having any entry
    # at prevLogIndex since step 3 covers the alternate case.
    # Note: this test case based on Figure 7, case (b) in the Raft paper
    def test_no_matching_log_entry(self):
        self.followerLogEntriesStore._setLog([1,1,1,4])
        self.assertEqual(4, self.followerLogEntriesStore.getLastIndex())
        appendEntries = self._makeAppendEntries(prevLogIndex = 10)
        reply = self.follower.processRpc(appendEntries)
        self.assertIsInstance(reply, AppendEntriesReply)
        self.assertEqual(
            reply.term,
            self.follower.getPersistentState().getCurrentTerm()
            )
        self.assertFalse(reply.success)




if __name__ == '__main__':
    unittest.main()
