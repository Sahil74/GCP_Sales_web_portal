from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FileUploadForm
from google.cloud import storage
import os
# Create your views here.
def upload_to_gcs(file, filename):
    # Initialize a storage client
    client = storage.Client()
    # Get the bucket
    bucket = client.get_bucket('sales_portal')
    # Create a new blob and upload the file's content.
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    return blob.public_url

def home(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            filename = file.name
            public_url = upload_to_gcs(file, filename)
            return render(request, 'index.html', {'form': form, 'public_url': public_url,'filename':filename})
    else:
        form = FileUploadForm()
    return render(request, 'index.html', {'form': form})