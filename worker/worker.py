#!/usr/bin/env python3
"""
PDF Worker Service
Extracts text from PDF patterns and indexes them in Meilisearch
"""

import os
import sys
import time
import tempfile
import subprocess
from pathlib import Path

import requests
import meilisearch
from PyPDF2 import PdfReader


# Configuration from environment variables
DIRECTUS_URL = os.getenv("DIRECTUS_URL", "http://directus:8055")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")
MEILISEARCH_URL = os.getenv("MEILISEARCH_URL", "http://meilisearch:7700")
MEILISEARCH_KEY = os.getenv("MEILISEARCH_KEY")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))  # seconds

# Validate configuration
if not DIRECTUS_TOKEN:
    print("❌ ERROR: DIRECTUS_TOKEN not set!")
    sys.exit(1)

if not MEILISEARCH_KEY:
    print("❌ ERROR: MEILISEARCH_KEY not set!")
    sys.exit(1)


class PDFWorker:
    """Worker for extracting PDF text and indexing in Meilisearch"""
    
    def __init__(self):
        self.directus_headers = {
            "Authorization": f"Bearer {DIRECTUS_TOKEN}",
            "Content-Type": "application/json"
        }
        self.meili_client = meilisearch.Client(MEILISEARCH_URL, MEILISEARCH_KEY)
        self.setup_meilisearch_index()
    
    def setup_meilisearch_index(self):
        """Create and configure Meilisearch index for patterns"""
        try:
            # Create index if it doesn't exist
            try:
                self.patterns_index = self.meili_client.get_index("patterns_index")
                print("✅ Connected to existing patterns_index")
            except meilisearch.errors.MeilisearchApiError:
                self.meili_client.create_index("patterns_index", {"primaryKey": "id"})
                self.patterns_index = self.meili_client.get_index("patterns_index")
                print("✅ Created patterns_index")
            
            # Configure searchable attributes
            self.patterns_index.update_searchable_attributes([
                "title",
                "notes",
                "tags",
                "pdf_text"
            ])
            
            # Configure filterable attributes
            self.patterns_index.update_filterable_attributes([
                "visibility",
                "date_created"
            ])
            
            print("✅ Meilisearch index configured")
        except Exception as e:
            print(f"❌ Error setting up Meilisearch: {e}")
            raise
    
    def get_patterns_to_process(self):
        """Fetch patterns from Directus that need PDF processing"""
        try:
            url = f"{DIRECTUS_URL}/items/patterns"
            params = {
                "fields": "id,title,slug,visibility,notes,pdf_file,date_created,date_updated",
                "filter[pdf_file][_nnull]": "true"  # Has a PDF file
            }
            
            response = requests.get(url, headers=self.directus_headers, params=params)
            response.raise_for_status()
            
            patterns = response.json().get("data", [])
            print(f"📄 Found {len(patterns)} patterns with PDFs")
            return patterns
        except Exception as e:
            print(f"❌ Error fetching patterns: {e}")
            return []
    
    def download_pdf(self, file_id):
        """Download PDF file from Directus"""
        try:
            url = f"{DIRECTUS_URL}/assets/{file_id}"
            response = requests.get(url, headers=self.directus_headers)
            response.raise_for_status()
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file.write(response.content)
            temp_file.close()
            
            return temp_file.name
        except Exception as e:
            print(f"❌ Error downloading PDF {file_id}: {e}")
            return None
    
    def extract_text_pypdf2(self, pdf_path):
        """Extract text from PDF using PyPDF2"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"⚠️ PyPDF2 extraction failed: {e}")
            return None
    
    def extract_text_pdftotext(self, pdf_path):
        """Extract text from PDF using pdftotext (poppler)"""
        try:
            result = subprocess.run(
                ["pdftotext", pdf_path, "-"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"⚠️ pdftotext extraction failed: {e}")
            return None
    
    def extract_pdf_text(self, pdf_path):
        """Extract text from PDF using multiple methods"""
        # Try pdftotext first (usually better)
        text = self.extract_text_pdftotext(pdf_path)
        
        # Fallback to PyPDF2
        if not text or len(text) < 50:
            text = self.extract_text_pypdf2(pdf_path)
        
        return text or ""
    
    def index_pattern(self, pattern, pdf_text):
        """Index pattern in Meilisearch"""
        try:
            document = {
                "id": pattern["id"],
                "title": pattern["title"],
                "slug": pattern.get("slug", ""),
                "visibility": pattern.get("visibility", "private"),
                "notes": pattern.get("notes", ""),
                "pdf_file": pattern.get("pdf_file", ""),
                "content": pdf_text,
                "date_created": pattern.get("date_created", ""),
                "date_updated": pattern.get("date_updated", ""),
            }
            
            self.patterns_index.add_documents([document])
            print(f"✅ Indexed pattern: {pattern['title']}")
        except Exception as e:
            print(f"❌ Error indexing pattern {pattern['id']}: {e}")
    
    def process_pattern(self, pattern):
        """Process a single pattern: download PDF, extract text, index"""
        if not pattern.get("pdf_file"):
            return
        
        print(f"\n📖 Processing: {pattern['title']}")
        
        # Download PDF
        pdf_path = self.download_pdf(pattern["pdf_file"])
        if not pdf_path:
            return
        
        try:
            # Extract text
            print("  Extracting text...")
            pdf_text = self.extract_pdf_text(pdf_path)
            
            if pdf_text:
                print(f"  Extracted {len(pdf_text)} characters")
                # Index in Meilisearch
                self.index_pattern(pattern, pdf_text)
            else:
                print("  ⚠️ No text extracted from PDF")
        finally:
            # Clean up temporary file
            Path(pdf_path).unlink(missing_ok=True)
    
    def run(self):
        """Main worker loop"""
        print("🚀 PDF Worker started")
        print(f"   Directus: {DIRECTUS_URL}")
        print(f"   Meilisearch: {MEILISEARCH_URL}")
        print(f"   Poll interval: {POLL_INTERVAL}s\n")
        
        while True:
            try:
                patterns = self.get_patterns_to_process()
                
                for pattern in patterns:
                    self.process_pattern(pattern)
                
                print(f"\n💤 Sleeping for {POLL_INTERVAL}s...")
                time.sleep(POLL_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n👋 Worker stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print(f"   Retrying in {POLL_INTERVAL}s...")
                time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    worker = PDFWorker()
    worker.run()
