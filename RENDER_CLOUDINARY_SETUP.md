# Cloudinary Setup for Render Deployment

## Why Cloudinary?
Render's filesystem is **ephemeral** - uploaded files get deleted on each deploy. We use Cloudinary (free tier) to store media files permanently.

## Step 1: Create Free Cloudinary Account

1. Go to: https://cloudinary.com/users/register/free
2. Sign up with your email (free account includes 25GB storage)
3. After signup, go to **Dashboard**

## Step 2: Get Your Cloudinary Credentials

From your Cloudinary Dashboard, copy these values:
- **Cloud Name** (e.g., `dnxq8k8m3`)
- **API Key** (e.g., `123456789012345`)
- **API Secret** (e.g., `abcdefghijklmnopqrstuvwxyz`)

## Step 3: Add Environment Variables to Render

1. Go to your Render dashboard
2. Select your **Web Service**
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add these 3 variables:

```
CLOUDINARY_CLOUD_NAME = your_cloud_name_here
CLOUDINARY_API_KEY = your_api_key_here
CLOUDINARY_API_SECRET = your_api_secret_here
```

## Step 4: Deploy

1. Commit and push your changes to GitHub
2. Render will automatically rebuild with Cloudinary
3. After deployment, test uploading an article - it should now persist!

## Alternative: AWS S3 (If you prefer)

If you'd rather use AWS S3 instead of Cloudinary, let me know and I can configure that instead.

## Testing

After deployment:
1. Upload an article
2. View the article
3. The file should persist even after redeploy!

