from django.db import models

from contacts.models import Contact

TXN_TYPE = [
    ('CR', 'Credit'),
    ('DB', 'Debit')
]

class Transaction(models.Model):
    txn_id = models.UUIDField(primary_key=True)
    txn_type = models.CharField(max_length=2, choices=TXN_TYPE)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    amount = models.FloatField()
    created_at = models.DateTimeField()

    def __str__(self):
        return str(self.txn_id) + '_' + str(self.txn_type)
