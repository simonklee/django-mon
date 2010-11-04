from django.http import HttpResponse

try:
    from simplejson import JSONEncoder
except ImportError:
    from django.utils.simplejson import JSONEncoder

from apps.mon.models import Record


def mon_router(request, pattern, *args, **kwargs):
    "Split url-pattern to dates and data-fields."
    valid_fields = Record.data_fields()

    if not pattern:
        return mon_monitor(request, valid_fields, dict(), args, kwargs)

    items = pattern.split('/')
    words = (f.lower() for f in items if f.isalpha())
    digits = (o for o in items if o.isdigit())

    fields = [f for f in words if f in valid_fields]

    dates = {
        'year': None,
        'month': None,
        'day': None
    }

    for p in digits:
        l = len(p)
        num = int(p)
        if l is 4:
            dates['year'] = num
        elif not dates['month'] and l < 13:
            dates['month'] = num
        else:
            dates['day'] = num

    for k, v in dates.items():
        if v:
            dates['created__%s' % k] = v
        del dates[k]

    return mon_monitor(request, fields, dates, args, kwargs)

def mon_monitor(request, fields, dates, *args, **kwargs):
    records = Record.objects.values(*fields).filter(**dates)
    data = list(records)
    for d in data:
        try:
            d['created'] = d['created'].isoformat()
        except KeyError:
            break
    return HttpResponse(JSONEncoder().encode(data), mimetype='application/json')
