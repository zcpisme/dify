import os
import json
from typing import Any, Union
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

class LocalChatLoadTool(BuiltinTool):
    """Local Chat Load Tool to load chat messages from a JSONL file saved by LocalChatSaveTool"""

    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any]
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        Invoke Local Chat Load Tool to load chat messages from a JSONL file.
        """
        result = []
        user_id = tool_parameters.get("user_id", "")
        last_chat_id = 0

        current_file_directory = os.path.dirname(__file__)
        root_directory = os.path.abspath(os.path.join(current_file_directory, '../../../../../../..'))
        # Define paths for the user's chat history and summary files
        chat_history_folder = os.path.join(root_directory, 'chatlog_db', 'chat_history')
        summary_folder = os.path.join(root_directory, 'chatlog_db', 'chat_summary')
        chat_history_path = f'{chat_history_folder}/{user_id}.jsonl'
        summary_path = f'{summary_folder}/{user_id}.jsonl'
        
        # Initialize containers for the loaded chat history and latest summary
        loaded_chats = []
        latest_summary = None
        
        if os.path.exists(summary_path):
            with open(summary_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        latest_summary = record  # Keep updating to get the last record
                    except json.JSONDecodeError:
                        continue  # Skip improperly formatted JSON lines
            try:
                result.append(self.create_text_message(text=latest_summary['summary']))
                last_chat_id = int(latest_summary['last_chat_id'])
            except:
                pass

        # Load chat messages from chat_history_path starting from last_chat_id
        if os.path.exists(chat_history_path):
            with open(chat_history_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        if record.get("id", 0) >= last_chat_id:
                            loaded_chats.append(f"{record['id']}: 用户: {record['user_query']}, 雷姆: {record['llm_response']}")
                    except json.JSONDecodeError:
                        continue  # Skip improperly formatted JSON lines
        
        # Load the latest summary record from summary_path
        loaded_chats_str = '|'.join(loaded_chats)
        # Prepare the response message with the loaded chat history and latest summary
        result.append(
            self.create_json_message(
                {
                    "status": "success",
                    "message": "Messages loaded successfully",
                    "loaded_chats_str": loaded_chats_str,
                    "latest_summary": latest_summary
                }
            )
        )
        
        return result
