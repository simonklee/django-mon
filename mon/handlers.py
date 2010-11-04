from django.http import HttpResponse
from piston.handler import BaseHandler

from mon.models import Record

class MonHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Record
    fields = Record.data_fields()

    def read(self, request, pattern=None):
        if not pattern:
            return Record.objects.all()

        items = pattern.split('/')
        words = (f.lower() for f in items if f.isalpha())
        digits = (o for o in items if o.isdigit())

        fields = [f for f in words if f in self.fields]

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

        return Record.objects.values(*fields).filter(**dates)
