# Matrix Bot for Firefly III

This project is a Matrix bot designed to help you quickly manage your cash spending by creating transactions in Firefly III. The bot listens for $spend command and create a transaction on Firefly III. 

> **Warning**: This bot uses the `matrix-nio` package, which as of 1 February 2026, has known issues with verifying devices. Use with caution.

### Prerequisites
- Firefly III instance with API access
- Matrix account for the bot

### Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd matrix_chatbot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example configuration file:
   ```bash
   cp config.json.example config.json
   ```
4. Update `config.json` with your Matrix and Firefly III credentials.

### Usage
1. Run the bot:
   ```bash
   python matrix_bot.py
   ```
2. Send a message in the format:
   ```
   $spend [amount] on/for [description]. Note: [optional note].
   ```
   Example:
   ```
   $spend 50 on groceries. Note: Weekly shopping.
   ```

## Configuration
The bot uses a `config.json` file for its settings. Below is an example:
```json
{
    "matrix": {
        "homeserver": "YOUR_MATRIX_HOMESERVER",
        "user_id": "@your_bot:matrix.org",
        "password": "YOUR_BOT_PASSWORD"
    },
    "firefly_iii": {
        "url": "YOUR_FIREFLY_URL",
        "api_token": "YOUR_ACCESS_TOKEN"
    }
}
```

## License
This project is licensed under the MIT License.