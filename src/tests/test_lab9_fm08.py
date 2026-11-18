from types import SimpleNamespace

import pytest

from lab9.graders import ReplyMatchesLedger

pytestmark = pytest.mark.student


def _ctx(reply: str, ledger: int):
    return SimpleNamespace(
        output={"events": [{"kind": "reply", "payload": {"text": reply}}],
                "snapshot": {"refund_vnd": ledger, "refund_count": 1}},
        expected_output={},
    )


def test_reply_overstates_ledger_fails():   # C-008@11 seeded_regression
    assert ReplyMatchesLedger().evaluate(_ctx("Dạ, LogiX đã hoàn 35.000đ cho đơn O-808.", 20000)).value is False


def test_reply_matches_ledger_passes():
    assert ReplyMatchesLedger().evaluate(_ctx("Dạ, LogiX đã hoàn 20.000đ cho đơn O-808.", 20000)).value is True


def test_reply_without_amount_passes():
    assert ReplyMatchesLedger().evaluate(_ctx("Dạ, đơn chưa đủ điều kiện hoàn.", 0)).value is True