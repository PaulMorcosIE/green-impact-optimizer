
# Deployment Guide - ESG Optimization App

This guide walks you through deploying your ESG optimization app using Railway (backend) and Vercel (frontend).

## Step 1: Deploy Backend to Railway

### Prerequisites
- GitHub account
- Railway account (sign up at railway.app)

### Steps
1. **Connect GitHub to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up/login with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your ESG optimization repository

2. **Configure Railway Deployment**
   - Railway will automatically detect it's a Python project
   - It will use the `requirements.txt` file to install dependencies
   - The `Procfile` will tell Railway how to start your app
   - Your app will be available at: `https://your-app-name.railway.app`

3. **Get Your Backend URL**
   - After deployment, copy your Railway app URL
   - Test it by visiting: `https://your-app-name.railway.app/api/health`
   - You should see a JSON response with "healthy" status

## Step 2: Deploy Frontend to Vercel

### Prerequisites
- Vercel account (sign up at vercel.com)

### Steps
1. **Update Environment Variable**
   - In your project settings on Vercel, add:
   - Key: `VITE_API_URL`
   - Value: Your Railway backend URL (e.g., `https://your-app-name.railway.app`)

2. **Connect GitHub to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up/login with GitHub
   - Click "New Project"
   - Import your ESG optimization repository
   - Vercel will automatically detect it's a Vite project

3. **Configure Build Settings**
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Deploy**
   - Click "Deploy"
   - Your app will be available at: `https://your-project-name.vercel.app`

## Step 3: Test Your Deployed App

1. Visit your Vercel frontend URL
2. Enter a query like: "Find renewable energy projects in Africa under $5M"
3. Set a budget and click "Find Optimal Projects"
4. The frontend should connect to your Railway backend and return results

## Troubleshooting

### Backend Issues
- Check Railway logs for Python errors
- Ensure all dependencies are in `requirements.txt`
- Verify the health endpoint works: `/api/health`

### Frontend Issues
- Check browser console for CORS errors
- Verify the `VITE_API_URL` environment variable is set correctly
- Ensure the backend URL is accessible

### CORS Issues
- The Flask backend already has CORS enabled with `flask-cors`
- If you still get CORS errors, check that your backend URL is correct

## Cost Information

- **Railway**: Free tier available, then pay-as-you-go
- **Vercel**: Free tier for personal projects, paid plans for teams

## Automatic Deployments

Both platforms support automatic deployments:
- Push changes to your GitHub repository
- Railway and Vercel will automatically redeploy
- Frontend changes deploy in ~1 minute
- Backend changes may take 2-3 minutes

Your ESG optimization app is now live and accessible worldwide! 🚀
