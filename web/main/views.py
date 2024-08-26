import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Certificate, Microblog, Portfolio, HomeSetting
from .forms import CertificateForm

import os
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key="AIzaSyClJozpl9aHpgYqwjOviSr4LMGQ64mq9oI") # os.environ.get("GEMINI_API_KEY")
GENERATION_CONFIG = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
chat_sessions = {}

def home(request):
    home_setting = HomeSetting.objects.all().first()
    context = {
        'home_setting': home_setting
    }
    return render(request, 'main/home.html', context)

def microblogging(request):
    microblogs = Microblog.objects.all().order_by('id')
    context = {
        'microblogs': microblogs
    }
    return render(request, 'main/microblogging.html', context)

def microblog_detail(request, pk):
    microblog = get_object_or_404(Microblog, pk=pk)
    return render(request, 'main/microblog_detail.html', {'microblog': microblog})

def microblog_list(request):
    microblogs = Microblog.objects.all().order_by('-created_at')
    return render(request, 'main/microblog_list.html', {'microblogs': microblogs})

def certificates(request):
    certificates = Certificate.objects.all()
    return render(request, 'main/certificates.html', {'certificates': certificates})

def certificate_detail(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    return render(request, 'main/certificate_detail.html', {'certificate': certificate})

def certificate_new(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save()
            return redirect('certificate_detail', pk=certificate.pk)
    else:
        form = CertificateForm()
    return render(request, 'main/certificate_edit.html', {'form': form})

def certificate_edit(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            certificate = form.save()
            return redirect('certificate_detail', pk=certificate.pk)
    else:
        form = CertificateForm(instance=certificate)
    return render(request, 'main/certificate_edit.html', {'form': form})

def certificate_delete(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        certificate.delete()
        return redirect('certificates')
    return render(request, 'main/certificate_delete.html', {'certificate': certificate})

def portfolio(request):
    portfolios = Portfolio.objects.all().order_by('id')
    context = {
        'portfolios': portfolios,
    }
    return render(request, 'main/portfolio.html', context)

def chatbot(request):
    return render(request, 'main/chatbot.html')

@csrf_exempt
def chat(request):
    if request.method == "POST":
        print("Request Body:", request.body)

        # Parse JSON from the request
        try:
            data = json.loads(request.body.decode('utf-8'))
            message = data.get('message')  # Get the message
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        session_id = request.session.get("session_id")

        print(f"message: `{message}`")

        if not session_id or session_id not in chat_sessions:
            # Start a new chat session
            chat_session = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                generation_config=GENERATION_CONFIG,
                safety_settings=SAFETY_SETTINGS,
            ).start_chat(history=[])
            session_id = str(id(chat_session))  # Simple session ID generation
            request.session["session_id"] = session_id
            chat_sessions[session_id] = chat_session
        else:
            print(">> get old session")
            chat_session = chat_sessions[session_id]

        response = chat_session.send_message(message)
        return JsonResponse({"response": response.text})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)