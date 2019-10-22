from rest_framework import serializers
from .models import Creditcard

# Min and Max number of digits for a credit card
CC_DIGITS_MIN = 15
CC_DIGITS_MAX = 19


class CreditcardSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    email = serializers.ReadOnlyField(source='owner.email')
    cc_number = serializers.CharField(max_length=CC_DIGITS_MAX)

    def validate_cc_number(self, value):
        """Check that value is a valid cc number"""
        if len(value) < CC_DIGITS_MIN:
            raise serializers.ValidationError(
                "Credit card number is not enough digits."
                )
        if len(value) > CC_DIGITS_MAX:
            raise serializers.ValidationError(
                "Credit card number is too many digits."
                )
        if not value.isdigit():
            raise serializers.ValidationError(
                "Credit card number is not only digits."
                )
        return value

    class Meta:
        """Meta class to map serializer's fields with the model fields"""
        model = Creditcard
        fields = ('id', 'cc_number', 'email', 'mii', 'mii_details', 'iin',
                  'iin_details', 'pan', 'network', 'check_digit', 'valid'
                  )
        read_only_fields = ('id', 'email')
