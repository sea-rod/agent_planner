from langchain_core.tools import tool
from .google_calendar import GoogleCalendar

google_cal = GoogleCalendar()
google_cal.connect("credentials.json")



@tool()
def get_events() -> list:
    """"
        It returns the events in the calendar
    """ 
    return google_cal.get_events()

@tool
def create_event(summary,description,strt_dateTime,end_dateTime,**kwargs) -> dict:
    """
        creates an event on google calendar
        you pass a json param
        param:
            events (str): in the following format 
            {
                'summary': 'Google I/O 2015',
                'description': 'A chance to hear more about Google\'s developer products.',
                'start': {
                'dateTime': '2025-10-23T09:00:00+05:30',
                },'end': {
                'dateTime': '2025-10-23T10:00:00+05:30',
                }}
        """
    event = {
        "summary":summary,
        "description":description,
        "start":{
            "dateTime":strt_dateTime
        },
        "end":{
            "dateTime":end_dateTime
        }
    }
    return google_cal.create_event(event)

