import io
from fastapi.testclient import TestClient


def test_upload_pdf_success(client: TestClient):
    # Create realistic PDF content
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n0\n%%EOF"

    file_buffer = io.BytesIO(pdf_content)
    file_buffer.seek(0)

    files = {"file": ("test.pdf", file_buffer, "application/pdf")}
    response = client.post("/api/v1/documents", files=files)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "test.pdf"


def test_upload_non_pdf_fail(client: TestClient):
    txt_content = b"Hello, this is not a PDF"
    files = {"file": ("test.txt", io.BytesIO(txt_content), "text/plain")}

    response = client.post("/api/v1/documents", files=files)

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid file type"
