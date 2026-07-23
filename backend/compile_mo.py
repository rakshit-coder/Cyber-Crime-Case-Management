#!/usr/bin/env python
"""
Compile .po files to .mo files using polib
"""
import polib
from pathlib import Path

# Paths
locale_dir = Path('locale/hi/LC_MESSAGES')
po_file = locale_dir / 'django.po'
mo_file = locale_dir / 'django.mo'

print("🔄 Loading PO file...")
po = polib.pofile(str(po_file))

# Stats
total = len(po)
translated = sum(1 for entry in po if entry.msgstr)

print(f"📊 File statistics:")
print(f"  Total strings: {total}")
print(f"  Translated: {translated}")
print(f"  Translation rate: {translated/total*100:.1f}%")

print("\n💾 Generating MO file...")
mo_data = po.to_binary()

with open(mo_file, 'wb') as f:
    f.write(mo_data)

size = mo_file.stat().st_size
print(f"✅ MO file created: {mo_file}")
print(f"✅ File size: {size} bytes")

if size > 5000:
    print("✅ Translation compilation SUCCESSFUL!")
else:
    print(f"⚠️  File seems small. Expected > 5000 bytes, got {size}")
