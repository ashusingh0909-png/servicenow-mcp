import os
import base64
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import truststore
truststore.inject_into_ssl()
import ssl
import truststore
CTX = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

load_dotenv()

mcp = FastMCP("servicenow-mcp")

BASE = os.environ["SNOW_URL"].rstrip("/")
AUTH = (os.environ["SNOW_USER"], os.environ["SNOW_PASSWORD"])
ALLOWED = set(os.environ.get("SNOW_TABLES", "incident,task,sc_request").split(","))

def call(method, path, headers=None, **kw):
    h = {"Accept": "application/json", **(headers or {})}
    r = httpx.request(method, BASE + path, auth=AUTH, timeout=60, verify=CTX,
                      headers=h, **kw)
    r.raise_for_status()
    return r.json().get("result", {})

def check(table):
    if table not in ALLOWED:
        raise ValueError(f"Table '{table}' is not allowed")

@mcp.tool()
def list_records(table: str, query: str = "", fields: str = "", limit: int = 10) -> list:
    """List records from a ServiceNow table. query is an encoded query
    like 'active=true^priority=1'. fields is comma-separated, e.g. 'number,short_description'."""
    check(table)
    params = {"sysparm_query": query, "sysparm_limit": min(limit, 50),
              "sysparm_display_value": "true"}
    if fields:
        params["sysparm_fields"] = fields
    return call("GET", f"/api/now/table/{table}", params=params)

@mcp.tool()
def get_record(table: str, sys_id: str) -> dict:
    """Get one record by its sys_id."""
    check(table)
    return call("GET", f"/api/now/table/{table}/{sys_id}",
                params={"sysparm_display_value": "true"})
@mcp.tool()
def create_record(table: str, fields: dict) -> dict:
    """Create a record. fields example: {"short_description": "Printer down", "urgency": "2"}"""
    check(table)
    return call("POST", f"/api/now/table/{table}", json=fields)

@mcp.tool()
def update_record(table: str, sys_id: str, fields: dict) -> dict:
    """Update fields on an existing record, e.g. {"work_notes": "Checked, waiting on user"}"""
    check(table)
    return call("PATCH", f"/api/now/table/{table}/{sys_id}", json=fields)

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email through ServiceNow."""
    return call("POST", "/api/now/email",
                json={"to": to, "subject": subject, "text": body})

@mcp.tool()
def upload_attachment(table: str, sys_id: str, file_name: str,
                      content_base64: str,
                      content_type: str = "application/octet-stream") -> dict:
    """Attach a file to a record. The file content must be base64 text."""
    check(table)
    return call("POST", "/api/now/attachment/file",
                params={"table_name": table, "table_sys_id": sys_id,
                        "file_name": file_name},
                content=base64.b64decode(content_base64),
                headers={"Content-Type": content_type})@mcp.tool()
def create_record(table: str, fields: dict) -> dict:
    """Create a record. fields example: {"short_description": "Printer down", "urgency": "2"}"""
    check(table)
    return call("POST", f"/api/now/table/{table}", json=fields)

@mcp.tool()
def update_record(table: str, sys_id: str, fields: dict) -> dict:
    """Update fields on an existing record, e.g. {"work_notes": "Checked, waiting on user"}"""
    check(table)
    return call("PATCH", f"/api/now/table/{table}/{sys_id}", json=fields)

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email through ServiceNow."""
    return call("POST", "/api/now/email",
                json={"to": to, "subject": subject, "text": body})

@mcp.tool()
def upload_attachment(table: str, sys_id: str, file_name: str,
                      content_base64: str,
                      content_type: str = "application/octet-stream") -> dict:
    """Attach a file to a record. The file content must be base64 text."""
    check(table)
    return call("POST", "/api/now/attachment/file",
                params={"table_name": table, "table_sys_id": sys_id,
                        "file_name": file_name},
                content=base64.b64decode(content_base64),
                headers={"Content-Type": content_type})
mcp.run()