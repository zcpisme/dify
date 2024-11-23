import os
import json
from typing import Any, Union
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

class LocalSummaryTool(BuiltinTool):
    """Local Chat Save Tool to save chat messages as JSONL records"""

    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any]
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        Invoke Local Chat Save Tool to save messages to a JSONL file.
        """
        result = []
        user_id = tool_parameters.get("user_id", "")
        summary = tool_parameters.get("summary", "")
        chat_time = tool_parameters.get("chat_time", "")
        last_chat_id = tool_parameters.get("last_chat_id", "")
        # Define file path with user_id as filename
        current_file_directory = os.path.dirname(__file__)
        root_directory = os.path.abspath(os.path.join(current_file_directory, '../../../../../../..'))
        db_folder = os.path.join(root_directory, 'chatlog_db', 'chat_summary')
        db_path = f'{db_folder}/{user_id}.jsonl'
        
        # Ensure the directory exists
        os.makedirs(db_folder, exist_ok=True)
        
        # Initialize id counter
        max_id = 0
        
        # Check if the JSONL file already exists and read max id
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        max_id = max(max_id, record.get("id", 0))
                    except json.JSONDecodeError:
                        continue  # Skip any lines that aren’t properly formatted JSON
        
        # Increment the id for the new message
        new_id = max_id + 1
        
        # Prepare the new record
        new_record = {
            "id": new_id,
            "summary": summary,
            "chat_time": chat_time,
            "user_id": user_id,
            "last_chat_id": last_chat_id,
        }
        
        # Write the record to the JSONL file (creates file if it doesn't exist)
        with open(db_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(new_record, ensure_ascii=False) + "\n")
        
        # Append a JSON message with the message details to the result
        result.append(
            self.create_json_message(
                {
                    "status": "success",
                    "message": "Message saved successfully",
                    "saved_record": new_record
                }
            )
        )

        return result
