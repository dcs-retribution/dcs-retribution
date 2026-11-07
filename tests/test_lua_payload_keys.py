"""Payload files whose pylon keys are local constants (CJS Super Hornet 2.4.6)."""

from dcs import lua

import game.ato.loadouts  # noqa: F401  (installs the Lua key fix)

PAYLOAD = """
local WTL = 1
local STA2 = 2
local unitPayloads = {
    ["name"] = "FA-18E",
    ["payloads"] = {
        [1] = {
            ["displayName"] = "- USN Fleet Defense",
            ["name"] = "USN Fleet Defense",
            ["pylons"] = {
                [WTL] = { ["CLSID"] = "{AIM-9X}", ["num"] = WTL },
                [STA2] = { ["CLSID"] = "<CLEAN>", ["num"] = 2 },
                [3] = { ["CLSID"] = "<CLEAN>", ["num"] = 3 },
            },
            ["tasks"] = { [1] = 11 },
        },
    },
    ["unitType"] = "FA-18E",
}
return unitPayloads
"""


def test_local_constants_used_as_table_keys_are_resolved() -> None:
    payloads = lua.loads(PAYLOAD)["unitPayloads"]["payloads"]

    assert set(payloads[1]["pylons"]) == {1, 2, 3}
    assert payloads[1]["pylons"][1]["CLSID"] == "{AIM-9X}"


def test_strings_that_look_like_keys_are_left_alone() -> None:
    text = 'local A = 1\nlocal t = { ["x"] = "[A] = 2" }\nreturn t'

    assert lua.loads(text)["t"]["x"] == "[A] = 2"
