import json

from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwner
from .serializers import CreditcardSerializer
from .models import Creditcard
from django.http import JsonResponse
from rest_framework.views import APIView


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""

    queryset = Creditcard.objects.all()
    serializer_class = CreditcardSerializer
    # Could use IsAuthenticatedOrReadOnly for testing valid card methods #
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save post data when creating a new card with owner set to user."""
        serializer.save(owner=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Creditcard.objects.all()
    serializer_class = CreditcardSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class ValidCard(APIView):
    """This class handles the validatecard http POST requests."""

    def post(self, request, format=None):
        """I have chosen to make an operation that does not directly represent
         a resource using the POST verb"""

        try:
            data = json.loads(request.body)
            # Get ccnumber
            ccnumber = data.get('ccnumber')
            mii = data.get('mii')
            mii_details = data.get('mii_details')
            iin = data.get('iin')
            iin_details = data.get('iin_details')
            pan = data.get('pan')
            network = iin_details
            check_digit = data.get('check_digit')
            valid = data.get('valid')
            response = {
                'ccnumber': ccnumber,
                'valid': valid,
                'mii': mii,
                'mii_details': mii_details,
                'iin': iin,
                'iin_details': iin_details,
                'pan': pan,
                'network': network,
                'check_digit': check_digit
            }
            status = 200

        except ValueError:
            status = 400
            response = dict(message="Bad Request",
                            status=status)

        return JsonResponse(response, safe=True, status=status)


class GenerateCard(APIView):
    """This class handles the gencard http POST requests."""

    def post(self, request, format=None):
        """I have chosen to make an operation that does not directly represent
        a resource using the POST verb"""

        try:
            data = json.loads(request.body)
            # Get ccnumber
            ccnumber = data.get('ccnumber')
            mii = data.get('mii')
            mii_details = data.get('mii_details')
            iin = data.get('iin')
            iin_details = data.get('iin_details')
            pan = data.get('pan')
            network = iin_details
            check_digit = data.get('check_digit')
            valid = data.get('valid')
            response = {'ccnumber': ccnumber,
                        'valid': valid,
                        'mii': mii,
                        'mii_details': mii_details,
                        'iin': iin,
                        'iin_details': iin_details,
                        'pan': pan,
                        'network': network,
                        'check_digit': check_digit
                        }
            status = 200

        except ValueError:
            status = 400
            response = dict(message="Bad Request", status=status)

        return JsonResponse(response, safe=True, status=status)
