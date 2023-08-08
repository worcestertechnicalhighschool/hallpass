from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .forms import ContactForm
from django.core.mail import send_mail

def privacy(request):
    return render(request, "pages/privacy.html")

def help(request):
    return render(request, "pages/help.html")

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    form = ContactForm()
    if request.method=='POST':
        form = ContactForm(request.POST)
        
        if form.isValid():
            txt_content = get_template("email/contact_message.txt")
            ctx = {
                "message": form.cleaned_data
            }
            send_mail(
                subject=f"HallPass message from: {form.cleaned_data['email']}",
                message=txt_content.render(ctx),
                from_email="info@hallpass@tech",
                recipient_list=["jeff@hallpass.tech"]
            )
    return render(request, "pages/contact.html", { "form":form })

def terms(request):
    return render(request, "pages/terms.html")

@require_http_methods(["GET"])
def robots(request):
    x = render(request, "robots.txt")
    x.headers["Content-Type"] = "text/plain; charset=utf-8"
    return x