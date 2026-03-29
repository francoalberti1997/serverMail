from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage


@csrf_exempt
def receive_and_send_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST"}, status=405)
    print("Enviando mail desde server remoto.")
    try:
        to = request.POST.get("to")
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        file = request.FILES.get("file")

        if not all([to, subject, body, file]):
            return JsonResponse({"error": "Missing data"}, status=400)

        email = EmailMessage(
            subject,
            body,
            None,  # usa DEFAULT_FROM_EMAIL
            [to],
        )

        email.attach(file.name, file.read(), file.content_type)

        email.send()

        return JsonResponse({"ok": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)