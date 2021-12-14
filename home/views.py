from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, FormView, UpdateView

from .forms import ClientForm, ScheduleRegisterForm, UserForm
from .models import Product, Service, Schedule, Client


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            path = request.POST.get("next", None) or "/dashboard/"
            return HttpResponseRedirect(path)

    return render(request, "home/login.html", context={"next": request.GET.get("next")})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home:contact")
    return redirect(request.path)


class HomeView(TemplateView):
    template_name = "home/contact.html"


class ProductsView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "home/products.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search", "")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class ServicesView(ListView):
    template_name = "home/services.html"
    model = Service


class ClientCreateView(FormView):
    template_name = "home/register_client.html"
    success_url = reverse_lazy("home:register-client")
    form_class = UserForm
    second_form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data()
        context["client_form"] = ClientForm(self.request.POST or None)
        return context

    def form_valid(self, **kwargs):
        messages.success(self.request, "Cliente cadastrado com sucesso")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, **kwargs):
        messages.warning(self.request, "Cliente não pôde ser cadastrado")
        return super().form_valid(**kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        user_form = context["form"]
        client_form = self.second_form_class(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            client_form.instance.user = user
            if client_form.is_valid():
                client_form.save()
                return self.form_valid()

        return self.get(self.request)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "home/dashboard.html"


class ScheduleRegisterView(LoginRequiredMixin, FormView):
    template_name = "home/register_schedule.html"
    form_class = ScheduleRegisterForm
    success_url = reverse_lazy("home:register-schedule")

    def get_form(self, form_class=None):
        form = super(ScheduleRegisterView, self).get_form()
        get_service = self.request.GET.get("service")
        if get_service:
            service = Service.objects.get(id=get_service)
            form.initial["service"] = service
        form.instance.client = self.request.user.client
        return form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["schedules"] = Schedule.objects.filter(client=self.request.user.client)
        return context_data

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST
            if data.get("exclude"):
                Schedule.objects.get(id=data.get("id")).delete()
        return super().post(request, *args, **kwargs)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "home/update_client.html"
    form_class = ClientForm
    model = Client

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def form_valid(self, form):
        messages.success(self.request, "Cliente alterado com sucesso!")
        return super(ClientUpdateView, self).form_valid(form)


@csrf_exempt
def product_create(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        photo = request.POST["photo"]
        Product.objects.create(name=name, price=price, photo=photo)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


@csrf_exempt
def product_update(request, index):
    if request.method == "POST":
        name = request.POST.get("name", None)
        price = request.POST.get("price", None)
        photo = request.POST.get("photo", None)
        product = Product.objects.get(pk=index)
        if name:
            product.name = name
        if price:
            product.price = price
        if photo:
            product.photo = photo
        product.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


def product_filter(request):
    if request.GET:
        name = request.GET["name"]
        queryset = Product.objects.filter(name__icontains=name)
        return JsonResponse(list(queryset.values()), safe=False)
    else:
        return HttpResponse(status=403)


def product_detail(request):
    if request.GET:
        index = request.GET["id"]
        try:
            queryset = Product.objects.filter(pk=index)
            if queryset:
                return JsonResponse(list(queryset.values())[0], safe=False)
        except Product.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=403)


@csrf_exempt
def product_delete(request):
    if request.POST:
        index = request.POST["id"]
        try:
            product = Product.objects.get(pk=index)
            if product:
                product.delete()
                return HttpResponse(status=200)
        except Product.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=403)


@csrf_exempt
def service_create(request):
    if request.method == "POST":
        service = request.POST["service"]
        description = request.POST["description"]
        value = request.POST["value"]
        Service.objects.create(service=service, description=description, value=value)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


@csrf_exempt
def service_update(request, index):
    if request.method == "POST":
        service = request.POST.get("service", None)
        description = request.POST.get("description", None)
        value = request.POST.get("value", None)
        service_model = Service.objects.get(pk=index)
        if service:
            service_model.service = service
        if description:
            service_model.description = description
        if value:
            service_model.value = value
        service_model.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


def service_filter(request):
    if request.GET:
        service = request.GET.get("service", "")
        description = request.GET.get("description", "")
        queryset = Service.objects.filter(service__icontains=service, description__icontains=description)
        return JsonResponse(list(queryset.values()), safe=False)
    else:
        return HttpResponse(status=403)


def service_detail(request):
    if request.GET:
        index = request.GET["id"]
        try:
            queryset = Service.objects.filter(pk=index)
            if queryset:
                return JsonResponse(list(queryset.values())[0], safe=False)
        except Service.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse(status=403)


@csrf_exempt
def service_delete(request):
    if request.POST:
        index = request.POST["id"]
        try:
            service_model = Service.objects.get(pk=index)
            if service_model:
                service_model.delete()
                return HttpResponse(status=200)
        except Service.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse(status=403)


def view_schedule(request):
    queryset = Schedule.objects.all()
    return JsonResponse(list(queryset.values()))
