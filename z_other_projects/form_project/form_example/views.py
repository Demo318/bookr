from django.shortcuts import render
from .forms import ExampleForm, OrderForm

def form_example(request):
    initial = {'email': 'user@example.com'}
    if request.method == "POST":
        # form = ExampleForm(request.POST)
        form = OrderForm(request.POST, initial=initial)
        if form.is_valid():
            for name, value in form.cleaned_data.items():
                print("{}: ({}) {}".format(name, type(value), value))
    else:
        # form = ExampleForm()
        form = OrderForm(initial=initial)

    

    return render(
        request,
        'form_example.html',
        {"method": request.method, "form": form}
    )
