from django.shortcuts import render
from django.utils import timezone
from django.db.models.functions import TruncDate
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from .models import Order
from .pagintation import OrderGetApiPagination
from .serializers import OrderSerializer, OrderGetSerializer

from api.utils.print_receipt import print_receipt


class OrderListApi(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderGetApiPagination


class OrderCreateApi(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderStatusUpdateApi(generics.UpdateAPIView):
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order.status = 1
        order.save()

        ## print_receipt(customer=True, order=order)

        serializer = OrderSerializer(order)

        return Response(serializer.data, status.HTTP_200_OK)


class OrderActiveListApi(generics.ListAPIView):
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(status=0)


class ReceiptPrintApi(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')

        if order_id is None:
            return Response({"Message": "order_id can not be None"})

        order_to_print = Order.objects.get(pk=order_id)

        # print_receipt(customer=True, order=order_to_print)

        return Response({"Message": "Receipt was printer successfully"})


class OrderFilterListApi(generics.ListAPIView):
    serializer_class = OrderGetSerializer
    pagination_class = OrderGetApiPagination

    def get_queryset(self):
        # param to get a list of Orders for current month or week
        period = self.request.query_params.get('period')

        # param to get a list of Orders for a certain day
        date = self.request.query_params.get('date')

        # params to get the list of Orders of a certain interval
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = None

        if not (start_date is None or end_date is None):
            print(f"START DATE: {start_date}")
            print(f"END DATE: {end_date}")
            queryset = Order.objects.filter(time_created__range=[start_date, end_date])

        if date is not None:
            print(f"DATE: {date}")
            orders = Order.objects.annotate(
                date=TruncDate('time_created')
            ).filter(date=date)

            queryset = orders

        if period == 'month':
            current_month = timezone.now().month
            current_year = timezone.now().year
            print(f"CURRENT MONTH: {current_month}")
            print(f"CURRENT YEAR: {current_year}")
            queryset = Order.objects.filter(time_created__month=current_month, time_created__year=current_year)

        if period == 'week':
            end_date = timezone.now()
            start_date = end_date - timezone.timedelta(days=7)

            print(f"START: {start_date}")
            print(f"END:   {end_date}")

            queryset = Order.objects.filter(time_created__range=[start_date, end_date])

        return queryset.filter(status=1)
