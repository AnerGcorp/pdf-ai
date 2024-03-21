from celery import shared_task

from app.web.db.models import Pdf
from app.web.files import download
from app.chat import create_embeddings_for_pdf
import logging

logger = logging.getLogger(__name__)

@shared_task()
def process_document(pdf_id: int):
    try:
        # Your existing code for retrieving Pdf object, downloading PDF, and creating embeddings
        pdf = Pdf.find_by(id=pdf_id)
        with download(pdf.id) as pdf_path:
            create_embeddings_for_pdf(pdf.id, pdf_path)
        return "PDF processing successful!"  # Return a success message on success
    except Exception as e:
        # Handle the exception here
        logger.error(f"Error processing PDF {pdf_id}: {e}")