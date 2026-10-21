# ServiceNow MCP Server

An MCP server that lets AI assistants (Claude Desktop, Copilot Studio)
work with ServiceNow: list, get, create and update records,
upload attachments and send emails.

## Setup
1. git clone https://github.com/ashusingh0909-png/servicenow-mcp.git
2. python -m venv .venv
3. .venv\Scripts\activate
4. pip install -r requirements.txt
5. Copy .env.example to .env and add your ServiceNow URL and login.

## Connect to Claude Desktop
Add this to claude_desktop_config.json (use your own paths):

(three backticks) json
{
  "mcpServers": {
    "servicenow-mcp": {
      "command": "C:\\path\\to\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\server.py"]
    }
  }
}
(three backticks)

## Tools
list_records, get_record, create_record, update_record,
send_email, upload_attachment

## Security
Use a least-privilege ServiceNow user and list only the tables you
need in SNOW_TABLES. Never commit your .env file.
