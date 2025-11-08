import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# --- Supabase Configuration ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"🔗 Connecting to Supabase...")
print(f"   URL: {SUPABASE_URL}")
print(f"   Key: {SUPABASE_KEY[:20]}...{SUPABASE_KEY[-10:]}\n")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Test Configuration ---
TEST_USER_ID = "test_user"
TEST_BUCKET = "user_documents"
TEST_FILE_NAME = "test_document.pdf"

# --- Create a test PDF ---
def create_test_pdf():
    from reportlab.pdfgen import canvas
    from io import BytesIO
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "🎉 Supabase Storage Test - SUCCESS!")
    c.drawString(100, 730, "This PDF was uploaded by your ImmigrationGPT app.")
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

print(f"📄 Creating test PDF...")
test_pdf_bytes = create_test_pdf()
print(f"   PDF size: {len(test_pdf_bytes)} bytes\n")

# --- SKIP bucket listing, go straight to upload ---
print(f"📤 Test: Uploading to Supabase Storage...")
print(f"   Bucket: {TEST_BUCKET}")
print(f"   Path: {TEST_USER_ID}/{TEST_FILE_NAME}\n")

storage_path = f"{TEST_USER_ID}/{TEST_FILE_NAME}"

try:
    # Attempt direct upload
    response = supabase.storage.from_(TEST_BUCKET).upload(
        path=storage_path,
        file=test_pdf_bytes,
        file_options={"content-type": "application/pdf", "upsert": "true"}
    )
    
    print(f"✅ Upload successful!")
    print(f"   Response: {response}\n")
    
    # Get public URL
    print(f"🔗 Getting public URL...")
    public_url = supabase.storage.from_(TEST_BUCKET).get_public_url(storage_path)
    print(f"   ✅ URL: {public_url}\n")
    
    print(f"👉 Open this URL in your browser:")
    print(f"   {public_url}\n")
    
    # List files in user folder
    print(f"📋 Listing files in '{TEST_USER_ID}/' folder...")
    files = supabase.storage.from_(TEST_BUCKET).list(TEST_USER_ID)
    if files:
        print(f"   ✅ Found {len(files)} file(s):")
        for f in files:
            print(f"      - {f['name']}")
    
    print(f"\n{'='*60}")
    print(f"🎉 SUCCESS! Your Supabase Storage is working perfectly!")
    print(f"{'='*60}")
    
except Exception as e:
    print(f"❌ Upload failed!")
    print(f"   Error: {e}\n")
    
    print(f"🔧 Troubleshooting:")
    print(f"   1. Verify your .env file:")
    print(f"      SUPABASE_URL=https://YOUR_PROJECT.supabase.co")
    print(f"      SUPABASE_KEY=your_anon_key_here")
    print(f"   ")
    print(f"   2. In Supabase Dashboard → Storage → user_documents:")
    print(f"      - Bucket should be marked as 'Public'")
    print(f"      - Policies tab should show INSERT and SELECT policies")
    print(f"   ")
    print(f"   3. Get your keys from:")
    print(f"      Supabase Dashboard → Settings → API")
    exit(1)
