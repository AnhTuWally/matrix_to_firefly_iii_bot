import simplematrixbotlib as botlib
import re
from datetime import datetime
import pprint
import logger

import requests
import json
from typing import Dict, Optional


import config_reader


class MatrixBot:
    def __init__(self, config_file: Optional[str] = 'config.json'):
        self._log = logger.get_logger("MatrixBot")
        self.config = config_reader.ConfigReader(config_file)
        self.bot = self._initialize_bot()

        self.firefly_base_url = self.config.get('firefly_iii', 'base_url')
        self.firefly_token = self.config.get('firefly_iii', 'token')


    def _initialize_bot(self):
        bot_config = botlib.Config()
        bot_config.encryption_enabled = True
        bot_config.ignore_unverified_devices = True

        homeserver = self.config.get('matrix', 'homeserver')
        user_id = self.config.get('matrix', 'user_id')
        password = self.config.get('matrix', 'password')

        creds = botlib.Creds(homeserver, user_id, password)
        return botlib.Bot(creds, bot_config)
    

    def run(self):
        self.bot.run()

    def setup_listeners(self):
        @self.bot.listener.on_message_event
        async def spend(room, message):
            prefix = "$"
            command = "spend"

            match = botlib.MessageMatch(room, message, self.bot, prefix)

            if not match.is_not_from_this_bot():
                return

            if not match.prefix() and not match.command(command):
                return

            is_processed = False  # Placeholder for actual processing result
            args = match.args()
            args_str = " ".join(args)

            try:
                # parse the message
                transaction_info = self._parse_message(args_str)
                pretty_parsed = pprint.pformat(transaction_info)
                self._log.info(f"Parsed message:\n{pretty_parsed}")

                # create the transaction
                is_processed = self.create_transaction(transaction_info)

            except ValueError as e:
                self._log.error(f"Error processing message: {e}")
                await self.bot.api.send_reaction(room.room_id, message.event_id, "❌")
                return

            if not is_processed:
                # React to indicate that the process failed
                await self.bot.api.send_reaction(room.room_id, message.event_id, "❌")
                return

            # React to indicate that the process is success
            await self.bot.api.send_reaction(room.room_id, message.event_id, "✅")


    @staticmethod
    def _parse_message(message: str) -> Dict:
        """
        Parses a message with the format:
        [amount] on/for [description]. [Note: optional text].

        Args:
            message (str): The message to parse.

        Returns:
            dict: A dictionary containing the parsed fields: amount, description, note, and date.
        """
        # Define the regex pattern to match the main part of the message (amount and description)
        main_pattern = r"(?P<amount>\d+(?:\.\d+)?)\s+(?:on|for)\s+(?P<description>[^.]+)\."

        # Match the message against the main pattern
        main_match = re.match(main_pattern, message)

        if not main_match:
            raise ValueError("Message format is invalid")

        # Extract the main matched groups into a dictionary
        result = {
            "type": "withdrawal",
            "amount": float(main_match.group("amount")),
            "description": main_match.group("description").strip(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source_name": "Cash wallet",
            "tags": ["matrix_bot"]
        }

        # Define the regex pattern to match the optional note
        note_pattern = r"[Nn]ote:\s*(?P<note>[^.]+)\."

        # Match the message against the note pattern
        note_match = re.search(note_pattern, message)

        # Add the note to the result if found, otherwise set it to None
        result["note"] = note_match.group("note").strip() if note_match else None

        return result


    def create_transaction(self, transaction_data: Dict):
        """
        Create a transaction in Firefly III via the API.

        Args:
            transaction_data (Dict): A dictionary containing transaction details.
        Returns:
            None
        """
        url = f"{self.firefly_base_url}/api/v1/transactions"
        headers = {
            "Authorization": f"Bearer {self.firefly_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        data_payload = {
            "transactions": [
                transaction_data
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data_payload))

        if response.status_code == 200 or response.status_code == 201:
            self._log.info("Transaction created successfully:", response.json())
            return True
        else:
            self._log.error("Failed to create transaction:", response.status_code, response.text)
        
        return False


if __name__ == "__main__":
    matrix_bot = MatrixBot()
    matrix_bot.setup_listeners()
    matrix_bot.run()