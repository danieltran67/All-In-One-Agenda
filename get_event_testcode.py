#Method 1

var now = new Date();
var twoHoursFromNow = new Date(now.getTime() + (2 * 60 * 60 * 1000));
var events = CalendarApp.getDefaultCalendar().getEvents(now, twoHoursFromNow);
Logger.log('Number of events: ' + events.length);

#Method 2

event = service.events().get(calendarId='primary', eventId='eventId').execute()

print event['summary']