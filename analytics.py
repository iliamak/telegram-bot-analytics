"""Google Sheets analytics module for Telegram bot."""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json
from typing import Optional


class Analytics:
    """Handles logging of bot events to Google Sheets."""
    
    def __init__(self):
        """Initialize Google Sheets connection."""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Попробовать загрузить credentials из переменной окружения
        credentials_json = os.getenv('GOOGLE_CREDENTIALS')
        
        if credentials_json:
            # Из переменной окружения (для Bothost/продакшена)
            try:
                creds_dict = json.loads(credentials_json)
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            except json.JSONDecodeError:
                raise ValueError('GOOGLE_CREDENTIALS is not valid JSON')
        else:
            # Из локального файла (для разработки)
            if os.path.exists('credentials.json'):
                creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            else:
                raise FileNotFoundError(
                    'Credentials not found. Set GOOGLE_CREDENTIALS env variable or add credentials.json file'
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