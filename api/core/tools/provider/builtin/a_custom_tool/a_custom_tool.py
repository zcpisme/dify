from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.a_custom_tool.tools.a_custom_tool_inner import LocalImageTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController
from typing import Any

class CustomProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict) -> None:
        try:
            LocalImageTool().fork_tool_runtime(
                runtime={
                    "credentials": credentials,
                }
            ).invoke(
                user_id="",
                tool_parameters={},
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
