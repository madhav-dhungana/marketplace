from rest_framework import serializers

from ..models import FeeModel , TransactionModel ,TaxModel


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxModel
        fields = '__all__'

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeModel
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = '__all__'