import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import NetworkRule
from django.urls import reverse
from .forms import NetworkForm
from django.views.decorators.http import require_POST


NETWORKS_FILE = os.path.join(settings.BASE_DIR, "networks.json")

def write_networks_file():
    qs = NetworkRule.objects.filter(enable=True)
    data = []
    for r in qs:
        data.append({
            "name": r.name,
            "host": r.host,
            "path_prefix": r.path_prefix,
            "response_code": r.response_code,
        })
    with open(NETWORKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def index(request):
    networks = NetworkRule.objects.all().order_by("-updated_at")
    return render(request, "proxy_app/index.html", {"networks": networks})

def add_network(request):
    if request.method == "POST":
        form = NetworkForm(request.POST)
        if form.is_valid():
            form.save()
            write_networks_file()
            return redirect("proxy_app:index")
    else:
        form = NetworkForm()
    return render(request, "proxy_app/form.html", {"form": form})

def edit_network(request, pk):
    obj = get_object_or_404(NetworkRule, pk=pk)
    if request.method == "POST":
        form = NetworkForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            write_networks_file()
            return redirect("proxy_app:index")
    else:
        form = NetworkForm(instance=obj)
    return render(request, "proxy_app/form.html", {"form": form, "edit": True})

def delete_network(request, pk):
    obj = get_object_or_404(NetworkRule, pk=pk)
    if request.method == "POST":
        obj.delete()
        write_networks_file()
        return redirect("proxy_app:index")
    return redirect(request, "proxy_app/index.html")

@require_POST
def toggle_network(request, pk):
    obj = get_object_or_404(NetworkRule, pk=pk)
    obj.enable = not obj.enable
    obj.save()
    write_networks_file()
    return redirect(reverse("proxy_app:index"))