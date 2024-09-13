from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import json
from django.conf import settings
import time

# Initialize the OpenAI client correctly
# client = OpenAI(api_key="your api key")

# Your assistant ID here
# ASSISTANT_ID = "your model id"

@csrf_exempt
def gpt4_risk_assessment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('input', '')

            # Create a new thread
            thread = client.beta.threads.create()

            # Add a message to the thread
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )

            # Run the assistant
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSISTANT_ID
            )

            # Wait for the run to complete
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

            # Retrieve the messages
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            # Get the last assistant message
            for message in messages:
                if message.role == "assistant":
                    gpt_response = message.content[0].text.value
                    break

            return JsonResponse({'response': gpt_response}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def index(request):
    return render(request, 'API/index.html')