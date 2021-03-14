from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import viewsets
from rest_framework import status

from contacts.models import Contact
from .models import Transaction
from django.core.paginator import Paginator
from .serializers import TransactionSerializer, TransactionCreateSerializer
import uuid
from dateutil import parser


class TransactionView(viewsets.ViewSet):
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        try:
            page_size = 3
            page = request.GET.get('page', 1)
            txn_type = request.GET.get('txn_type', None)
            phone_number = request.GET.get('phone_number', None)
            if phone_number is None:
                if txn_type is not None:
                    transactions = Transaction.objects.filter(txn_type=txn_type).order_by('-created_at')
                else:
                    transactions = Transaction.objects.all().order_by('-created_at')
            else:
                try:
                    user = Contact.objects.get(phone_number=phone_number)
                except Exception as exception:
                    return Response("User with this phone number does not exist", status=status.HTTP_400_BAD_REQUEST)
                if txn_type is not None:
                    transactions = Transaction.objects.filter(txn_type=txn_type, contact=user).order_by('-created_at')
                else:
                    transactions = Transaction.objects.filter(contact=user).order_by('-created_at')
            paginator = Paginator(transactions, page_size)
            resources = paginator.page(page)
            serializer = TransactionSerializer(resources, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response("Invalid Page number", status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            serializer = TransactionCreateSerializer(data=request.data)
            if serializer.is_valid():
                txn_id = uuid.uuid1()
                phone_number = request.data['phone_number']
                txn_type = request.data['txn_type']
                amount = request.data['amount']
                created_at = request.data['created_at']
                created_at_time = parser.parse(created_at)
                try:
                    user = Contact.objects.get(phone_number=phone_number)
                except Exception as exception:
                    return Response("Invalid phone number passed in the request body",
                                    status=status.HTTP_400_BAD_REQUEST)
                recent_transaction = Transaction.objects.filter(contact=user, created_at=created_at_time)
                if len(recent_transaction)>0:
                    return Response("Transaction already synced",
                                    status=status.HTTP_400_BAD_REQUEST)
                transaction = Transaction.objects.create(txn_id=txn_id,
                                                         txn_type=txn_type,
                                                         contact=user,
                                                         amount=amount,
                                                         created_at=created_at_time)
                transaction.save()
                result = dict()
                result['message'] = "Transaction created successfully"
                result['data'] = self.request.data
                return Response(data=result, status=status.HTTP_201_CREATED)
            else:
                return Response("Invalid request body. Please provide valid transaction params",
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(str(exception))
            return Response("Invalid Page number", status=status.HTTP_400_BAD_REQUEST)
