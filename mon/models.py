from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

class Record(models.Model):

    created = models.DateTimeField(_('created'), auto_now_add=True)
    current = models.FloatField(_('current'), null=True)
    volt = models.FloatField(_('voltage'), null=True)
    temp = models.FloatField(_('temperature'), null=True)
    light = models.FloatField(_('Photocell'), null=True)

    def __unicode__(self):
        return u'%s' % str(self.created)

    class Meta:
        get_latest_by = 'created'
        ordering = ('-created',)

    @staticmethod
    def data_fields():
        return ['current', 'volt', 'temp', 'light', 'created']

    @staticmethod
    def data_fields_abbr():
        return {'i': 'current', 'v': 'volt', 'c': 'temp', 'lux': 'light', 't': 'created'}
