"""Execute actual MOOSE menu definitions with Lua 5.1 and controlled DCS stubs."""

from pathlib import Path

from lupa.lua51 import LuaRuntime


def test_menu_command_callbacks_follow_reused_command_instances() -> None:
    root = Path(__file__).parents[2]
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().MOOSE_SOURCE = (root / "resources/plugins/base/Moose.lua").read_text(
        encoding="utf-8"
    )
    lua.execute(
        (Path(__file__).with_name("menu_command_binding_test.lua")).read_text(
            encoding="utf-8"
        )
    )
