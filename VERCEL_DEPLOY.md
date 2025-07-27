# 🚀 Deploy StudySprint to Vercel (FREE!)

Deploy your StudySprint app to Vercel with Supabase database - both 100% FREE!

## 🌟 Why Vercel + Supabase?

- ✅ **100% FREE** - No credit card required
- ✅ **Global CDN** - Lightning fast worldwide
- ✅ **Auto HTTPS** - Secure by default  
- ✅ **Git integration** - Deploy on every push
- ✅ **Custom domains** - Professional URLs
- ✅ **Serverless** - Scales automatically

---

## 🛠️ Step-by-Step Deployment

### 1. Set Up Supabase Database (2 minutes)

1. **Go to [supabase.com](https://supabase.com)**
2. **Sign up with GitHub**
3. **Create new project**:
   - Name: `StudySprint`
   - Password: `studysprint123!` (save this!)
   - Region: Choose closest to you
4. **Wait 2 minutes** for setup

### 2. Get Database Connection String

1. **In Supabase** → **Settings** → **Database**
2. **Copy "URI" connection string**
3. **Replace `[YOUR-PASSWORD]`** with `studysprint123!`
4. **Should look like**:
   ```
   postgresql://postgres:studysprint123!@db.abc123.supabase.co:5432/postgres
   ```

### 3. Prepare Your Code for Vercel

Your StudySprint is already Vercel-ready! The files are created:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/app.py` - Serverless entry point
- ✅ Updated models with scoring/timing

### 4. Deploy to Vercel (3 minutes)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy StudySprint to Vercel"
   git push origin main
   ```

2. **Go to [vercel.com](https://vercel.com)**
3. **Sign up with GitHub**
4. **Click "New Project"**
5. **Import your StudySprint repository**
6. **Set Environment Variables**:
   - `DATABASE_URL` = your Supabase connection string
   - `SECRET_KEY` = `super-secret-production-key-123`
7. **Click "Deploy"**
8. **Wait 2 minutes** for deployment

### 5. Seed Your Cloud Database

```bash
# Set your Supabase URL locally
export DATABASE_URL="postgresql://postgres:studysprint123!@db.abc123.supabase.co:5432/postgres"

# Seed with problems
python seed_data.py

# (Optional) Migrate local data
python migrate_to_cloud.py
```

---

## 🎯 What You Get

### **Your Live URLs**
- **Main app**: `https://studysprint-username.vercel.app`
- **Custom domain**: `studysprint.yourname.com` (optional)

### **Features**
- 🏆 **Leaderboard** - Global rankings and fastest solves
- ⏱️ **Time tracking** - Solve times and points system
- 📊 **Scoring system** - Points based on difficulty + speed
- 🗃️ **Cloud database** - Never lose user data
- 🌍 **Global access** - Available worldwide
- 📱 **Mobile friendly** - Works on all devices

---

## 📊 **NEW! Scoring System**

### **How Points Work:**
- **Base points**: 100 per problem
- **Difficulty multiplier**: 
  - Easy: 1x (100 points)
  - Medium: 1.5x (150 points)  
  - Hard: 2x (200 points)
- **Speed bonus**:
  - Under 1 minute: +50 points
  - Under 5 minutes: +25 points
  - Under 15 minutes: +10 points

### **Example Scoring:**
- Easy problem solved in 30 seconds: `(100 + 50) × 1.0 = 150 points`
- Medium problem solved in 8 minutes: `(100 + 10) × 1.5 = 165 points`
- Hard problem solved in 3 minutes: `(100 + 25) × 2.0 = 250 points`

---

## 🏆 **NEW! Leaderboard Features**

### **Global Leaderboard** (`/leaderboard`)
- 👑 **Top performers** by total score
- ⚡ **Speed records** for each problem
- 🥇 **Medal system** (gold, silver, bronze)

### **Problem Leaderboards** (`/problem/1/leaderboard`)
- 🏁 **Fastest solves** per problem
- 📈 **Rankings** with solve times
- 💫 **Achievement badges** based on speed

---

## 🔧 Managing Your Deployment

### **Update Your App**
```bash
# Make changes locally
git add .
git commit -m "Update StudySprint"
git push

# Vercel auto-deploys on every push!
```

### **View Logs**
- **Vercel Dashboard** → Your Project → **Functions** → **View Logs**

### **Monitor Database**
- **Supabase Dashboard** → **Table Editor** 
- View users, submissions, leaderboards in real-time

### **Custom Domain** (Optional)
1. **Vercel Dashboard** → **Settings** → **Domains**
2. **Add your domain** → Follow DNS instructions
3. **Get free SSL** automatically

---

## 💰 **Costs: 100% FREE!**

### **Vercel Free Tier:**
- ✅ **100GB bandwidth/month**
- ✅ **100 deployments/day** 
- ✅ **Serverless functions**
- ✅ **Global CDN**
- ✅ **Custom domains**
- ✅ **Automatic HTTPS**

### **Supabase Free Tier:**
- ✅ **500MB PostgreSQL storage**
- ✅ **50,000 API requests/month**
- ✅ **2GB bandwidth/month**
- ✅ **Unlimited users**

**This is MORE than enough for StudySprint!**

---

## 🚀 **Post-Deployment Checklist**

- [ ] ✅ App deployed to Vercel
- [ ] ✅ Database connected to Supabase
- [ ] ✅ Problems seeded (10 coding challenges)
- [ ] ✅ Leaderboard working
- [ ] ✅ User registration/login working
- [ ] ✅ Timer and code editor working
- [ ] ✅ Points and scoring system active

---

## 🔥 **Show It Off!**

Your StudySprint is now **production-ready** with:
- **Professional URL** - `studysprint-you.vercel.app`
- **Global leaderboards** - Competitive coding fun
- **Speed tracking** - Gamified learning
- **Mobile responsive** - Code anywhere
- **Enterprise database** - Supabase backing

**Perfect for:**
- 📝 **CS50 final project** presentation
- 💼 **Portfolio showcase** 
- 👥 **Friend competitions**
- 🎓 **Coding bootcamp demo**
- 🏢 **Job interviews**

## 🎉 **You Did It!**

**Your LeetCode-meets-Pomodoro platform is live on the internet for FREE!** 

Users worldwide can now:
- ⏱️ **Practice coding** in focused 25-minute sprints
- 🏆 **Compete on leaderboards** 
- 📊 **Track their progress** with detailed stats
- 🚀 **Earn points** for fast, accurate solutions

**Share your creation!** 🌟 