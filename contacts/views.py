from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, authentication, permissions, status

from contacts.models import Contact
from contacts.serializers import ContactSerializer


class ContactView(viewsets.ViewSet):

    def create(self, request):
        try:
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                users = Contact.objects.filter(phone_number=self.request.data['phone_number'])
                if len(users)>0:
                    return Response("User with this mobile number already exist in the system",
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    phone_number = self.request.data['phone_number']
                    first_name = self.request.data['first_name']
                    last_name = self.request.data['last_name']
                    contact = Contact.objects.create(phone_number=phone_number,
                                                     first_name=first_name,
                                                     last_name=last_name)
                    contact.save()
                    result = dict()
                    result['message'] = "New Contact created successfully"
                    result['data'] = self.request.data
                    return Response(data=result, status=status.HTTP_201_CREATED)
            else:
                return Response("Invalid request body. Please provide valid phone number, "
                                "first and last name", status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            return Response("Oops! Something went wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR)