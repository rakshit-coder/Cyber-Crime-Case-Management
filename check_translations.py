from babel.messages import pofile

po_file = 'backend/locale/hi/LC_MESSAGES/django.po'
catalog = pofile.read_po(po_file, ignore_obsolete=True)

total = 0
translated = 0
untranslated = 0
untranslated_msgs = []

for message in catalog:
    if message.id and message.id.strip():  # Skip header
        total += 1
        if message.string and message.string.strip():
            translated += 1
        else:
            untranslated += 1
            if untranslated <= 15:  # Show first 15 untranslated
                untranslated_msgs.append(message.id)

print(f'📊 Translation Statistics for Hindi (hi):')
print(f'━' * 50)
print(f'Total strings: {total}')
print(f'Translated: {translated} ✓')
print(f'Untranslated: {untranslated}')
if total > 0:
    pct = (translated/total)*100
    print(f'Completion: {pct:.1f}%')
    print(f'')
    if pct >= 80:
        print('Status: ✅ EXCELLENT')
    elif pct >= 60:
        print('Status: ⚠️  GOOD BUT NEEDS MORE')
    elif pct >= 40:
        print('Status: ⚠️  FAIR - NEEDS WORK')
    else:
        print('Status: ❌ INCOMPLETE')

if untranslated_msgs:
    print(f'\n⚠️  Sample untranslated strings ({len(untranslated_msgs)} shown):')
    for msg in untranslated_msgs:
        if len(msg) > 70:
            print(f'  - {msg[:67]}...')
        else:
            print(f'  - {msg}')
