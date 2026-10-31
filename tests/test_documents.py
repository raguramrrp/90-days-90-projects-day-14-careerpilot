import tempfile
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from documents.models import Document


class DocumentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            email='u1@example.com',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)

    def test_document_upload_and_download(self):
        dummy_file = SimpleUploadedFile("test_resume.pdf", b"%PDF-1.4 sample resume bytes", content_type="application/pdf")
        res = self.client.post(reverse('documents:upload'), {
            'title': 'Core Backend Resume',
            'document_type': 'Resume',
            'resume_category': 'Python Developer',
            'file': dummy_file,
            'description': 'Targeted for Django / FastAPI roles'
        })
        self.assertEqual(res.status_code, 302)
        doc = Document.objects.get(user=self.user)
        self.assertEqual(doc.title, 'Core Backend Resume')
        self.assertEqual(doc.resume_category, 'Python Developer')

        # Download
        dl_res = self.client.get(reverse('documents:download', args=[doc.pk]))
        self.assertEqual(dl_res.status_code, 200)

    def test_invalid_file_extension_rejected(self):
        bad_file = SimpleUploadedFile("danger.exe", b"executable bytes", content_type="application/x-msdownload")
        res = self.client.post(reverse('documents:upload'), {
            'title': 'Malicious file',
            'document_type': 'Resume',
            'file': bad_file,
        })
        # Should not create document
        self.assertFalse(Document.objects.filter(title='Malicious file').exists())
