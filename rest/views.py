from django.core.exceptions import ObjectDoesNotExist
from django.db.backends.sqlite3.base import IntegrityError

from django.http.response import HttpResponse

# Create your views here.
from rest_framework.renderers import StaticHTMLRenderer, XMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest.models import Customer, Complain


class CustomersView(APIView):
    renderer_classes = (XMLRenderer, JSONRenderer)

    def get(self, request):
        data = request.QUERY_PARAMS
        if data.has_key('id'):
            try:
                customer = Customer.objects.get(id=data['id'])
            except ObjectDoesNotExist:
                return HttpResponse("User with this id do not exist", 404)
        elif data.has_key('name') and data.has_key('surname') and data.has_key('patronymic'):
            try:
                customer = Customer.objects.get(name=data['name'], surname=data['surname'],
                                                patronymic=data['patronymic'])
            except ObjectDoesNotExist:
                return HttpResponse("User with this id do not exist", 404)
        else:
            return HttpResponse("Please provide ether id or name, surname and patronymic ", 400)
        customer = {'id': customer.id, 'name': customer.name, 'surname': customer.surname,
                    'patronymic': customer.patronymic}
        return Response(data=customer)

    def post(self, request):
        data = request.data
        try:
            customer = Customer.objects.create(name=data['name'], surname=data['surname'],
                                               patronymic=data['patronymic'])
        except KeyError:
            return HttpResponse("Customer name, surname or patronymic is not specified", 400)
        except IntegrityError:
            return HttpResponse("Customer already exists", )
        return Response(data={'id': customer.id})

    def put(self, request):
        return self.post(request)


    def delete(self, request):
        data = request.data
        try:
            Customer.objects.filter(name=data['name'], surname=data['surname'], patronymic=data['patronymic']).delete()
        except KeyError:
            return HttpResponse("Customer name, surname or patronymic is not specified", 400)
        return HttpResponse("Customer was successfully deleted", status=200)


class ComplainView(APIView):
    renderer_classes = (XMLRenderer, JSONRenderer)

    def get(self, request):
        data = request.QUERY_PARAMS
        if data.has_key('id'):
            try:
                complain = Complain.objects.get(id=data['id'])
            except ObjectDoesNotExist:
                return HttpResponse("Complain with this id do not exist", 404)
        else:
            return HttpResponse("ID is not specified", 400)
        complain = {'id': complain.id, 'customer_id': complain.customer_id, 'message': complain.message}
        return Response(data=complain)

    def post(self, request):
        data = request.data
        try:
            customer = Complain.objects.create(customer_id=data['customer_id'], message=data['message'])
        except KeyError:
            return HttpResponse("Customer ID or message isn't specified", 400)
        return Response(data={'id': customer.id})

    def put(self, request):
        return self.post(request)


    def delete(self, request):
        data = request.data
        try:
            Complain.objects.filter(id=data['customer_id']).delete()
        except KeyError:
            return HttpResponse("Customer ID isn't specified", 400)
        return HttpResponse("Complain was deleted")


class ComplainSelectByTimeView(APIView):
    renderer_classes = (StaticHTMLRenderer, XMLRenderer, JSONRenderer)

    def get(self, request):
        data = request.QUERY_PARAMS
        if not data.has_key('from'):
            return HttpResponse("Start date is not specified", 400)
        if not data.has_key('to'):
            return HttpResponse("End date is not specified", 400)
        if request.accepted_media_type == "text/html":
            html = "<ul>"
            for customer in Customer.objects.all():
                html += "<li>"
                html += customer.name + " " + customer.patronymic + " " + customer.surname + ":\n"
                html += "<ul>"
                for complain in Complain.objects.filter(customer_id=customer.id, complain_date__gte=data['from'],
                                                        complain_date__lte=data['to']):
                    html += "<li>"
                    html += complain.message
                    html += "</li>"
                html += "</ul>"
                html += "</li>"
            html += "</ul>"
            return Response(data=html)
        else:
            complains = []
            for customer in Customer.objects.all():
                user_complains = []
                for complain in Complain.objects.filter(customer_id=customer.id, complain_date__gte=data['from'],
                                                        complain_date__lte=data['to']):
                    user_complains.append({'id': complain.id, 'message': complain.message})
                complains.append({str(customer.id): user_complains})
        return Response(data=complains)


class ComplainSelectByTimeAndUserView(APIView):
    renderer_classes = (StaticHTMLRenderer, XMLRenderer, JSONRenderer)

    def get(self, request):
        data = request.QUERY_PARAMS
        if not data.has_key('customer_id'):
            return HttpResponse("Customer id is not specified", 400)
        if not data.has_key('from'):
            return HttpResponse("Start date is not specified", 400)
        if not data.has_key('to'):
            return HttpResponse("End date is not specified", 400)
        if request.accepted_media_type == "text/html":
            html = "<ul>"
            for complain in Complain.objects.filter(customer_id=data['customer_id'], complain_date__gte=data['from'],
                                                    complain_date__lte=data['to']):
                html += "<li>"
                html += complain.message
                html += "</li>"
            html += "</ul>"
            return Response(data=html)
        else:
            user_complains = []
            for complain in Complain.objects.filter(customer_id=data['customer_id'], complain_date__gte=data['from'],
                                                    complain_date__lte=data['to']):
                user_complains.append({'id': complain.id, 'message': complain.message})

        return Response(data=user_complains)


class ComplainSelectByUserView(APIView):
    renderer_classes = (StaticHTMLRenderer, XMLRenderer, JSONRenderer)

    def get(self, request):
        data = request.QUERY_PARAMS
        if not data.has_key('customer_id'):
            return HttpResponse("Customer id is not specified", 400)
        if request.accepted_media_type == "text/html":
            html = "<ul>"
            for complain in Complain.objects.filter(customer_id=data['customer_id']):
                html += "<li>"
                html += complain.message
                html += "</li>"
            html += "</ul>"
            return Response(data=html)
        else:
            user_complains = []
            for complain in Complain.objects.filter(customer_id=data['customer_id']):
                user_complains.append({'id': complain.id, 'message': complain.message})

        return Response(data=user_complains)


class ComplainSelectAllView(APIView):
    renderer_classes = (StaticHTMLRenderer, XMLRenderer, JSONRenderer)

    def get(self, request):
        if request.accepted_media_type == "text/html":
            html = "<ul>"
            for customer in Customer.objects.all():
                html += "<li>"
                html += customer.name + " " + customer.patronymic + " " + customer.surname + ":\n"
                html += "<ul>"
                for complain in Complain.objects.filter(customer_id=customer.id):
                    html += "<li>"
                    html += complain.message
                    html += "</li>"
                html += "</ul>"
                html += "</li>"
            html += "</ul>"
            return Response(data=html)
        else:
            complains = []
            for customer in Customer.objects.all():
                user_complains = []
                for complain in Complain.objects.filter(customer_id=customer.id):
                    user_complains.append({'id': complain.id, 'message': complain.message})
                complains.append({str(customer.id): user_complains})
        return Response(data=complains)


class CustomerSelectAllView(APIView):
    renderer_classes = (StaticHTMLRenderer, XMLRenderer, JSONRenderer)

    def get(self, request):
        if request.accepted_media_type == "text/html":
            html = "<ul>"
            for customer in Customer.objects.all():
                html += "<li>"
                html += customer.name + " " + customer.patronymic + " " + customer.surname
                html += "</li>"
            html += "</ul>"
            return Response(data=html)
        else:
            customers = []
            for customer in Customer.objects.all():
                customers.append({'id': customer.id, 'name': customer.name, 'surname': customer.surname,
                                  'patronymic': customer.patronymic})
        return Response(data=customers)