import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from .models import Document
from .forms import DocumentUploadForm, DocumentEditForm


@login_required
def document_list(request):
    doc_type = request.GET.get('type')
    queryset = Document.objects.filter(user=request.user).prefetch_related('applications_as_resume')

    if doc_type:
        queryset = queryset.filter(document_type=doc_type)

    resumes = [d for d in queryset if d.document_type == 'Resume']
    cover_letters = [d for d in queryset if d.document_type == 'Cover Letter']
    others = [d for d in queryset if d.document_type not in ('Resume', 'Cover Letter')]

    return render(request, 'documents/list.html', {
        'documents': queryset,
        'resumes': resumes,
        'cover_letters': cover_letters,
        'others': others,
        'current_type': doc_type,
        'types': Document.DOCUMENT_TYPES,
        'total_docs': len(queryset)
    })


@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            messages.success(request, f"Document '{doc.title}' uploaded successfully.")
            return redirect('documents:list')
        else:
            messages.error(request, "Failed to upload document. Please check the file requirements (max 5MB).")
    else:
        form = DocumentUploadForm()

    return render(request, 'documents/form.html', {
        'form': form,
        'title': 'Upload Resume or Career Document'
    })


@login_required
def document_edit(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DocumentEditForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, f"Document '{doc.title}' updated.")
            return redirect('documents:list')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = DocumentEditForm(instance=doc)

    return render(request, 'documents/form.html', {
        'form': form,
        'doc': doc,
        'title': f"Edit Document Metadata: {doc.title}"
    })


@login_required
def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        title = doc.title
        # Delete underlying storage file if exists
        if doc.file and os.path.isfile(doc.file.path):
            try:
                os.remove(doc.file.path)
            except OSError:
                pass
        doc.delete()
        messages.success(request, f"Document '{title}' was deleted.")
        return redirect('documents:list')

    return render(request, 'documents/confirm_delete.html', {'doc': doc})


@login_required
def document_download(request, pk):
    """Secure document download endpoint ensuring strict user isolation."""
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if not doc.file or not os.path.exists(doc.file.path):
        raise Http404("Document file was not found on server.")
    
    filename = os.path.basename(doc.file.name)
    response = FileResponse(open(doc.file.path, 'rb'), as_attachment=True, filename=filename)
    return response
