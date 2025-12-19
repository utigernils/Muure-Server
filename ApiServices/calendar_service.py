"""
Calendar service for fetching and parsing web calendar (iCal) data.
"""
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from icalendar import Calendar
import pytz
import recurring_ical_events


class CalendarService:
    """Handles fetching and parsing iCal calendar data."""
    
    def __init__(self, config):
        self.config = config
        self.calendar_url = config.calendar_url
        self.timezone = pytz.timezone(config.calendar_timezone)
    
    async def get_calendar_events(self) -> List[Dict[str, Any]]:
        """Fetch calendar events and return today's or next upcoming events."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.calendar_url, timeout=10.0)
                response.raise_for_status()
                
                # Parse iCal data
                cal = Calendar.from_ical(response.content)
                events = []
                
                now = datetime.now(self.timezone)
                today = now.date()
                
                # Look ahead 365 days for events
                end_date = today + timedelta(days=365)
                
                # Get all events (including recurring ones) in range
                expanded_events = recurring_ical_events.of(cal).between(today, end_date)
                
                # Extract events from calendar
                for component in expanded_events:
                    event_start = component.get('dtstart')
                    if not event_start:
                        continue
                    
                    # Handle both datetime and date objects
                    if hasattr(event_start.dt, 'date'):
                        # Convert to local timezone if it's timezone-aware
                        event_datetime = event_start.dt
                        if event_datetime.tzinfo is not None:
                            event_datetime = event_datetime.astimezone(self.timezone)
                        
                        event_date = event_datetime.date()
                        event_time = event_datetime.time()
                        is_all_day = False
                    else:
                        event_date = event_start.dt
                        event_time = None
                        is_all_day = True
                    
                    # Only include today and future events (double check as between might include overlapping)
                    if event_date >= today:
                        summary = str(component.get('summary', 'No title'))
                        description = str(component.get('description', ''))
                        location = str(component.get('location', ''))
                        
                        events.append({
                            'date': event_date.isoformat(),
                            'time': event_time.isoformat() if event_time else None,
                            'is_all_day': is_all_day,
                            'title': summary,
                            'description': description,
                            'location': location
                        })
                
                # Sort events by date and time
                events.sort(key=lambda x: (x['date'], x['time'] or '00:00:00'))
                
                # Find today's events or next day with events
                todays_events = [e for e in events if e['date'] == today.isoformat()]
                
                if todays_events:
                    return {
                        'date': today.isoformat(),
                        'is_today': True,
                        'events': todays_events
                    }
                
                # Find next day with events
                if events:
                    next_date = events[0]['date']
                    next_events = [e for e in events if e['date'] == next_date]
                    return {
                        'date': next_date,
                        'is_today': False,
                        'events': next_events
                    }
                
                # No events found
                return {
                    'date': today.isoformat(),
                    'is_today': True,
                    'events': []
                }
                
        except Exception as e:
            raise Exception(f"Failed to fetch calendar: {str(e)}")
