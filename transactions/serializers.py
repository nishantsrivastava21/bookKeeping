from rest_framework import serializers

from transactions.models import TXN_TYPE


class TransactionSerializer(serializers.Serializer):
    txn_id = serializers.UUIDField()
    txn_type = serializers.CharField()
    contact = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.FloatField()
    created_at = serializers.DateTimeField()


class TransactionCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)
    txn_type = serializers.ChoiceField(choices=TXN_TYPE)
    amount = serializers.FloatField()
    created_at = serializers.CharField()