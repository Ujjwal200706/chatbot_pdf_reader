# 🚀 Deployment Guide - Streamlit App

This guide will help you deploy your PDF QA System using Streamlit Cloud.

## 📋 Prerequisites

Before you start, make sure you have:
- ✅ A GitHub account
- ✅ Your repository pushed to GitHub (Ujjwal200706/chatbot_pdf_reader)
- ✅ A Streamlit Cloud account

---

## Step 1: Create a Streamlit Cloud Account

1. Visit **[Streamlit Cloud](https://streamlit.io/cloud)** 
2. Click **"Sign up"** or **"Sign in"** if you already have an account
3. **Authenticate with GitHub** when prompted
4. Grant Streamlit access to your GitHub repositories

---

## Step 2: Deploy Your App

1. After logging in to Streamlit Cloud, click **"Create app"** button
2. You'll see a form with three fields:

   **Fill in the following:**
   - **Repository**: `Ujjwal200706/chatbot_pdf_reader`
   - **Branch**: `master`
   - **Main file path**: `app_streamlit.py`

3. Click **"Deploy"**

---

## Step 3: Wait for Deployment

The deployment process typically takes **2-5 minutes**. You'll see:
- 🔄 "Building..."
- 📦 Installing dependencies
- ✅ "Your app is running!"

Once complete, your app will be accessible at a URL like:
```
https://[app-name]-[random-id].streamlit.app
```

---

## Step 4: Get Your App URL

After deployment completes:
1. Copy the URL from the browser address bar
2. Test the app by uploading a PDF and asking questions
3. Share this URL with others!

---

## 🎯 How to Test Your App

1. **Upload a PDF**: Click the "Select PDF file" button and choose a PDF from your computer
2. **Wait for Processing**: The app will process the PDF and create an index
3. **Ask Questions**: Type your question in the text area
4. **Get Answers**: Click "🔍 Ask Question" to get instant answers from your PDF

---

## ⚙️ Configuration & Customization

### Restart/Redeploy
If you make changes to your code:
1. Push changes to GitHub
2. Go to **Streamlit Cloud Dashboard**
3. Click on your app
4. Click **"Rerun"** or changes will auto-deploy

### Change Theme
Edit `.streamlit/config.toml` to customize colors:
```toml
[theme]
primaryColor = "#FF6B6B"      # Change this hex code
backgroundColor = "#FFFFFF"
```

---

## 📊 Monitoring Your App

- **View Logs**: Click "Settings" → "View logs"
- **Check Status**: Green dot = running, Red dot = error
- **Monitor Usage**: Dashboard shows app analytics

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Make sure `requirements.txt` is in the repository root and contains all dependencies

### Issue: "App is loading forever"
**Solution**: Check the logs - wait 5+ minutes on first run as models are downloading

### Issue: "FAISS index not found"
**Solution**: Upload a PDF first to create the index before asking questions

### Issue: "Memory error"
**Solution**: This might happen with large PDFs. Try using smaller PDFs (< 50MB)

---

## 📱 Sharing Your App

Once deployed, share the URL with:
- Team members
- Friends
- On social media
- In your portfolio

**Example URL**: `https://chatbot-pdf-reader-ujjwal.streamlit.app`

---

## 💡 Tips & Best Practices

1. **First-time load is slow**: Models are downloaded on first use (one-time only)
2. **Use smaller PDFs**: Faster processing and better user experience
3. **Monitor costs**: Streamlit Cloud free tier includes reasonable usage limits
4. **Update frequently**: Improve your app based on user feedback

---

## 🔐 Security Notes

- ✅ All processing is done server-side
- ✅ PDFs are not stored permanently
- ✅ User questions are not logged
- ✅ No data is sent to external APIs

---

## 📞 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Community**: https://discuss.streamlit.io
- **GitHub Issues**: https://github.com/Ujjwal200706/chatbot_pdf_reader/issues

---

## 🎉 Congratulations!

Your PDF QA System is now live on the internet! 🚀

Share your link and let people ask questions from PDFs without any LLM!

---

**Created with ❤️ | Happy Deploying!**
