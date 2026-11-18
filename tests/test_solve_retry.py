from unittest import mock

import pytest

from onepoint3acres import onepoint3acres as m


class FakeSolver:
	def __init__(self, outcomes):
		self.outcomes = list(outcomes)
		self.calls = 0

	def turnstile(self, **kwargs):
		self.calls += 1
		o = self.outcomes.pop(0)
		if isinstance(o, Exception):
			raise o
		return o


def make(outcomes):
	solver = FakeSolver(outcomes)
	return m.OnePointThreeAcres("a=b", solver), solver


@mock.patch.object(m.time, "sleep")
def test_transient_error_is_retried(sleep):
	acres, solver = make([Exception("ERROR_NO_SLOT_AVAILABLE"), Exception("timeout"), {"code": "ok"}])
	assert acres._solve_turnstile("u") == {"code": "ok"}
	assert solver.calls == 3
	assert [c.args[0] for c in sleep.call_args_list] == [30, 60]


@mock.patch.object(m.time, "sleep")
def test_fatal_error_not_retried(sleep):
	acres, solver = make([Exception("ERROR_ZERO_BALANCE")])
	with pytest.raises(Exception, match="ZERO_BALANCE"):
		acres._solve_turnstile("u")
	assert solver.calls == 1
	sleep.assert_not_called()


@mock.patch.object(m.time, "sleep")
def test_gives_up_after_max_attempts(sleep):
	acres, solver = make([Exception("ERROR_NO_SLOT_AVAILABLE")] * m.SOLVE_MAX_ATTEMPTS)
	with pytest.raises(Exception, match="NO_SLOT"):
		acres._solve_turnstile("u")
	assert solver.calls == m.SOLVE_MAX_ATTEMPTS
