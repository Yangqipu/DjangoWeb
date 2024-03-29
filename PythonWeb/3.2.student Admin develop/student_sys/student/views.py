from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Student
from .form import StudentForm

from django.views import View


# Create your views here.


def index(request):
    words = "World"
    # students = Student.objects.all()
    students = Student.get_all()
    if request.method == "POST":
        print("POST")
        form = StudentForm(request.POST)
        if form.is_valid():
            # cleaned_data = form.cleaned_data
            # student = Student()
            # student.name = cleaned_data["name"]
            # student.sex = cleaned_data["sex"]
            # student.email = cleaned_data["email"]
            # student.profession = cleaned_data["profession"]
            # student.qq = cleaned_data["qq"]
            # student.phone = cleaned_data["phone"]
            # student.save()
            form.save()
            print(1234444444)
            return HttpResponseRedirect(reverse("index"))

    else:
        form = StudentForm()
    context = {
        "students": students,
        "form": form,
    }

    return render(request, "index.html", context=context)
    # return HttpResponse("hello")


class IndexView(View):
    template_name = "index.html"

    def get_context(self):
        students = Student.get_all()
        context = {
            "students": students
        }
        return context

    def get(self, request):
        context = self.get_context()
        form = StudentForm()
        context.update({
            "form": form
        })
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        context = self.get_context()
        context.update({
            "form": form
        })

        return render(request, self.template_name, context=context)
