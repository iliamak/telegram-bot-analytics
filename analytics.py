"""Google Sheets analytics module for Telegram bot."""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
from typing import Optional


class Analytics:
    """Handles logging of bot events to Google Sheets."""
    
    def __init__(self, credentials_file: str = 'credentials.json'):
        """Initialize Google Sheets connection.
        
        Args:
            credentials_file: Path to service account JSON file
        """
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file, scope
        )
        client = gspread.authorize(creds)
        
        sheet_url = os.getenv('SHEET_URL')
        if not sheet_url:
            raise ValueError('SHEET_URL not found in environment variables')
            
        self.sheet = client.open_by_url(sheet_url).sheet1
        
        # Initialize headers if empty
        if not self.sheet.row_values(1):
            self.sheet.append_row([
                'Timestamp',
                'User ID',
                'Username',
                'Event',
                'Data'
            ])
    
    def log(self, user_id: int, username: Optional[str], event: str, data: str = ''):
        """Log an event to Google Sheets.
        
        Args:
            user_id: Telegram user ID
            username: Telegram username (can be None)
            event: Event name (e.g., 'start', 'help', 'message')
            data: Additional event data
        """
        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            str(user_id),
            username or '',
            event,
            str(data)
        ]
        
        try:
            self.sheet.append_row(row)
        except Exception as e:
            print(f'Error logging to Google Sheets: {e}')
            # В продакшене здесь можно добавить fallback в SQLite