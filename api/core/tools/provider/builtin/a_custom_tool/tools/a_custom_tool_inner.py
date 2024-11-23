import os
from typing import Any, Union
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

class LocalImageTool(BuiltinTool):
    """Local Image Tool to read local image URLs and return a result"""

    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any]
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        Invoke Local Image Tool to read images from a folder.
        """
        result = []

        # Iterate over images in the folder

        image_url = tool_parameters.get("image_url", "")

        # Append the image message to the result
        result.append(self.create_image_message(image=image_url))

        # Append a JSON message with the image URL to the result
        result.append(
            self.create_json_message(
                {
                    "url": image_url,
                }
            )
        )

        return result
