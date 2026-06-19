# ⚡ AUTOMATIC FORM FILLING - 5 MINUTE SETUP

**SKIP EVERYTHING ELSE AND DO THIS!**

---

## **MINUTE 1-2: Start Backend**

### Terminal 1:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

Wait for: `✅ Application startup complete`

---

## **MINUTE 3: Upload Resume**

1. Open in browser: `http://localhost:3000/job-application-form.html`
2. Scroll down to **"📄 Upload Your Resume"**
3. Click **"Upload Resume"**
4. Select your resume file (PDF or TXT)
5. Click **"📤 Upload & Fill Form"**
6. Wait for green message: `✅ Resume uploaded successfully!`

**Done with step 1!** ✅

---

## **MINUTE 4: Get Your Profile ID**

### Terminal 2:
```bash
python cli.py list
```

**Copy the ID** you see (looks like: `abc123xyz`)

---

## **MINUTE 5: Test Auto-Fill**

### Terminal 2:
```bash
python cli.py fill abc123xyz https://www.linkedin.com
```

Replace `abc123xyz` with YOUR ID from step 4.

Browser opens → Form fills automatically → Done! ✅

---

## **NOW: Fill Real Job Forms!**

### For LinkedIn:
```bash
python cli.py fill abc123xyz https://www.linkedin.com/jobs/view/1234567
```

### For Indeed:
```bash
python cli.py fill abc123xyz https://www.indeed.com/jobs?q=python
```

### For ANY Website:
```bash
python cli.py fill abc123xyz <PASTE_JOB_URL_HERE>
```

---

## **THAT'S IT!** 🎉

```
✅ Resume uploaded
✅ Profile created
✅ Auto-fill working
✅ Ready to apply!
```

---

## **WHAT HAPPENS NEXT?**

1. **Browser opens** with the job form
2. **Form fills automatically** with your data
3. **You review** the filled fields
4. **You click Submit**
5. **Form sent!** 🚀

---

## **TROUBLESHOOTING**

| Problem | Solution |
|---------|----------|
| "No profiles found" | Go to step 3, upload resume |
| "Cannot connect to server" | Restart backend (Terminal 1) |
| "Form doesn't fill" | Check profile ID is correct |
| "Browser won't open" | Make sure backend is running |

---

## **KEEP THIS HANDY!** 📋

### Always needed:
```bash
# Terminal 1 - Always running
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Fill forms with
python cli.py fill <ID> <URL>
```

### Get profile ID:
```bash
python cli.py list
```

---

## **BONUS: Chrome Extension (Even Easier)** 🧩

1. Go to: `chrome://extensions/`
2. Turn on: **Developer mode** (top right)
3. Click: **Load unpacked**
4. Select: `Auto filling form\extension`
5. Go to any job site
6. Click extension icon
7. Click "Auto-Fill Form"
8. Done! ✅

---

## **YOUR NEXT 10 JOB APPLICATIONS**

Just repeat:
```bash
python cli.py fill abc123xyz <JOB_URL>
```

For each job URL you find!

---

**Questions? Check AUTOMATIC_GUIDE.md for full details!** 📖

**Ready to get hired?** 🚀
