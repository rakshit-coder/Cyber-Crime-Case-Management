#!/usr/bin/env python
"""
Compile .po files to .mo files using polib (doesn't require msgfmt)
"""
import os
import sys
from pathlib import Path

# Add the backend directory to path
backend_dir = Path('d:\\secure-case-connect-main\\backend')
sys.path.insert(0, str(backend_dir))

os.chdir(backend_dir)

print("🔄 Compiling messages for Hindi using polib...")

try:
    from polib import pofile, mofile
    
    po_file = backend_dir / 'locale' / 'hi' / 'LC_MESSAGES' / 'django.po'
    mo_file = backend_dir / 'locale' / 'hi' / 'LC_MESSAGES' / 'django.mo'
    
    print(f"📖 Reading PO file: {po_file}")
    catalog = pofile(str(po_file))
    
    # Count translations
    translated = sum(1 for entry in catalog if entry.string)
    untranslated = sum(1 for entry in catalog if not entry.string)
    
    print(f"📊 Translations found:")
    print(f"  ✓ Translated: {translated}")
    print(f"  ✗ Untranslated: {untranslated}")
    
    print(f"\n💾 Writing MO file: {mo_file}")
    with open(mo_file, 'wb') as f:
        mofile.write(f, catalog)
    
    size = mo_file.stat().st_size
    print(f"✅ MO file created successfully!")
    print(f"✅ File size: {size} bytes")
    
    if size > 5000:
        print("\n✅ Translation compilation SUCCESSFUL! Translations are ready.")
    else:
        print("\n⚠️  WARNING: File size is small. Some translations may be missing.")
        
except ImportError:
    print("❌ Error: polib not installed. Installing...")
    os.system('pip install polib')
    print("🔄 Retrying compilation...")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
