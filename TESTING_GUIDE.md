# Quick Testing Guide - Legal Information System

## How to Test the New Features

### Prerequisites
- Django development server running on `http://localhost:8000`
- Database migrated and populated
- Test user account created (or use existing)

### Test Case 1: File Complaint and See Legal Info

**Steps:**
1. Login as a regular user (role='user')
2. Navigate to `/complaints/new/`
3. Fill in complaint form:
   - Title: "Received phishing email"
   - Description: "Got suspicious email asking for bank details"
   - Category: **"Phishing"** ← Important
   - Priority: "High"
   - Incident Date: Today's date
   - Incident Location: "Online"
4. Click "Submit Complaint"
5. **Expected Result**: Redirected to legal info page showing:
   - ✅ Case number (e.g., "C-202602-00001")
   - ✅ "Complaint Filed Successfully!" message
   - ✅ Complaint summary card
   - ✅ Applicable laws (IT Act 2000, IPC)
   - ✅ All sections (66, 66C, 66D, 420, 406, 409)
   - ✅ Punishment details
   - ✅ Government resources (cybercrime.gov.in, etc.)
   - ✅ "What to Do Next" section

### Test Case 2: Browse Laws Index

**Steps:**
1. Click "Laws" in main navigation bar (visible to all users)
2. **Expected Result**: Lands on `/laws/`
   - ✅ See all 8 crime categories
   - ✅ See introduction and key acts section
   - ✅ See punishment guidelines
   - ✅ See government resources
   - ✅ Search box works
3. Try searching: Type "phishing" in search
   - ✅ Only phishing card shows
   - ✅ Other cards hidden

### Test Case 3: View Law Details

**Steps:**
1. From laws index page, click any law card (e.g., "Phishing")
2. OR Navigate directly to `/laws/phishing/`
3. **Expected Result**: Detailed law page showing:
   - ✅ Law category header with icon
   - ✅ Description of category
   - ✅ All applicable laws
   - ✅ Each law with sections and details
   - ✅ Section title, description, punishment
   - ✅ Government resources for that category
   - ✅ "What to Do Next" steps
   - ✅ Important disclaimer
   - ✅ "File a Complaint" button links to `/complaints/new/`

### Test Case 4: All Crime Categories

**Try filing complaints with these categories and verify laws appear:**

1. **Phishing**: IT Act 66, 66C, 66D + IPC 420, 406
2. **Identity Theft**: IT Act 66C, 66E + IPC 406, 420, 468 + Aadhaar Act
3. **Online Fraud**: IT Act 66, 66D + IPC 420, 511
4. **Hacking**: IT Act 43, 66 + IPC 420, 379, 405
5. **Ransomware**: IT Act 66, 66B + IPC 383, 384
6. **Data Breach**: IT Act 43A, 66, 72 + Digital Personal Data Protection Act 2023
7. **Cyberbullying**: IT Act 66A, 67, 67A + IPC 294, 354, 509 + BNS 2023
8. **Malware**: IT Act 66, 66B

### Test Case 5: Permission Checks

**Steps for Regular User:**
1. Login as User A
2. File a complaint
3. Get the case number (e.g., C-202602-00001)
4. Logout
5. Login as User B
6. Try to access `/complaints/C-202602-00001/legal-info/`
7. **Expected Result**: Error message "You do not have permission to view this page."
8. Redirected to complaints list

**Steps for Officer/Admin:**
1. Login as Officer or Admin
2. Try to access any user's complaint legal info
3. **Expected Result**: ✅ Can access without permission error

### Test Case 6: Navigation Links

**Check all links work:**

From Base Navigation:
- ✅ "Laws" → `/laws/`
- ✅ "Awareness" → `/awareness/`
- ✅ "Dashboard" → User's dashboard
- ✅ "My Complaints" → `/complaints/`

From Footer:
- ✅ "Cyber Awareness" → `/awareness/`
- ✅ "Cyber Crime Laws" → `/laws/`
- ✅ "Home" → `/`

From Legal Info Pages:
- ✅ "View Complaint Details" → `/complaints/<case_number>/`
- ✅ "View All Complaints" → `/complaints/`
- ✅ "Report on cybercrime.gov.in" → External link opens in new tab
- ✅ Government resource links open in new tabs

### Test Case 7: Invalid Law Category

**Steps:**
1. Navigate to `/laws/invalid_category/`
2. **Expected Result**: 
   - ✅ 404 Not Found page displays
   - ✅ Shows available law categories
   - ✅ Provides links to browse laws or go home

### Test Case 8: Responsive Design

**Test on:**
- ✅ Desktop (1920x1080)
- ✅ Tablet (768px width)
- ✅ Mobile (375px width)

**Check:**
- ✅ Laws grid adapts to screen size
- ✅ Cards stack properly on mobile
- ✅ Text readable on all sizes
- ✅ Buttons accessible on touch devices
- ✅ Navigation collapses on mobile (if hamburger menu)

### Test Case 9: Government Resources

**Verify all links:**
1. ✅ cybercrime.gov.in - National Cyber Crime Portal
2. ✅ cert-in.org.in - CERT-In
3. ✅ rbi.org.in - Reserve Bank of India
4. ✅ meity.gov.in - Ministry of Electronics & IT
5. ✅ uidai.gov.in - Aadhaar Authority
6. ✅ nciipc.gov.in - National Center for Crime Info

All links should:
- ✅ Open in new tab (`target="_blank"`)
- ✅ Work without SSL errors
- ✅ Load successfully

### Test Case 10: Search Functionality

**On `/laws/`:**
1. Clear search box
2. Type "fraud"
3. **Expected**: Only "Online Fraud" card shows
4. Type "theft"
5. **Expected**: Only "Identity Theft" and "Data Breach" cards show
6. Type "xyz123"
7. **Expected**: No cards show (no matches)
8. Clear search
9. **Expected**: All 8 cards reappear

## URL Endpoints to Test

```
# Complaint Legal Info (After filing a complaint)
GET  /complaints/<case_number>/legal-info/
POST /complaints/new/  (submit form redirects to legal-info)

# Laws Index
GET  /laws/

# Law Details
GET  /laws/phishing/
GET  /laws/identity_theft/
GET  /laws/online_fraud/
GET  /laws/hacking/
GET  /laws/ransomware/
GET  /laws/data_breach/
GET  /laws/cyberbullying/
GET  /laws/malware/
GET  /laws/other/

# Invalid Category (404)
GET  /laws/invalid/
GET  /laws/random/
```

## Expected Response Codes

```
✅ 200 OK - Valid pages (legal-info, laws index, law details)
✅ 302 Redirect - After complaint submission → legal-info
✅ 403 Forbidden - User accessing another's complaint legal info
✅ 404 Not Found - Invalid law category
✅ 405 Method Not Allowed - POST to GET-only endpoints
```

## Database Checks

**After filing a complaint:**
1. Check `Complaint` table:
   ```sql
   SELECT * FROM complaints_complaint 
   WHERE case_number = 'C-202602-00001'
   ```
   - ✅ category field has correct value
   - ✅ complainant_id matches logged-in user

2. Check that `Evidence`, `Remark`, `ComplaintAttachment` created if data provided

## Django Admin Checks

Login to `/django-admin/`:
1. Navigate to Complaints
2. ✅ See all filed complaints
3. ✅ Can see category field
4. ✅ Case numbers are unique
5. ✅ Can filter by category

## Common Issues & Fixes

### Issue: Page shows blank/404
**Fix**: Ensure laws app in INSTALLED_APPS in settings.py

### Issue: Laws link in navigation gives 404
**Fix**: Check URL routing in secure_case_connect/urls.py includes laws app

### Issue: Permission error for own complaint
**Fix**: Ensure user's role is set to 'user' (not 'officer' or 'admin')

### Issue: Government links don't open
**Fix**: Check internet connectivity and link URLs are correct

### Issue: Search not working
**Fix**: Ensure JavaScript is enabled in browser

## Performance Checks

**Page Load Times:**
- `/laws/` should load in <1 second
- `/laws/<category>/` should load in <1 second
- `/complaints/<id>/legal-info/` should load in <1 second

**Database Queries:**
- Complaint legal-info: 1 query (get complaint)
- Law index: 0 queries (in-memory data)
- Law detail: 0 queries (in-memory data)

## Browser Compatibility

Test in:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (if available)
- ✅ Mobile browsers

## Console Checks

Open browser DevTools Console (F12):
- ✅ No JavaScript errors
- ✅ No 404 errors in Resources
- ✅ No CORS errors
- ✅ No mixed content warnings

## Final Verification Checklist

- [ ] Can file complaint and get redirected to legal-info
- [ ] Legal info shows correct laws for category
- [ ] All government links work
- [ ] Can browse laws index
- [ ] Can view law details
- [ ] Invalid categories show 404
- [ ] Permissions work correctly
- [ ] Responsive on mobile
- [ ] Search works
- [ ] Navigation links all correct
- [ ] No console errors
- [ ] Performance acceptable
- [ ] External links open in new tabs

## Success Criteria

✅ **All of the above tests pass** → Legal Information System is working correctly!

User can now:
1. File a complaint about any cyber crime
2. Instantly see applicable laws
3. Understand legal sections and punishments
4. Access government resources
5. Know the steps to take next
6. Anytime browse all cyber crime laws
