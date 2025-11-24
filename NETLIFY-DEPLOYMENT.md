# Netlify Deployment Instructions

## Quick Start

Your MK Philatelic website is ready to deploy to Netlify and connect to mkphilatelic.com!

### Step 1: Deploy to Netlify

1. **Go to Netlify**: https://www.netlify.com/
2. **Sign in** (or create account if needed)
3. **Click "Add new site" → "Import an existing project"**
4. **Choose GitHub** as your Git provider
5. **Select the repository**: `michaelkernaghan/mkphilatelic`
6. **Configure build settings**:
   - Branch to deploy: `main`
   - Build command: (leave empty or use provided in netlify.toml)
   - Publish directory: `.` (root directory)
7. **Click "Deploy site"**

Your site will be live at a temporary URL like: `random-name-12345.netlify.app`

### Step 2: Connect Custom Domain (mkphilatelic.com)

#### Option A: If you own mkphilatelic.com

1. **In Netlify Dashboard**:
   - Go to your site settings
   - Click "Domain management"
   - Click "Add custom domain"
   - Enter: `mkphilatelic.com`
   - Click "Verify"

2. **Update DNS Records**:

   Netlify will provide DNS settings. Go to your domain registrar and add:

   **A Record:**
   ```
   Type: A
   Name: @
   Value: 75.2.60.5 (Netlify's IP)
   TTL: 3600
   ```

   **CNAME Record (for www):**
   ```
   Type: CNAME
   Name: www
   Value: random-name-12345.netlify.app
   TTL: 3600
   ```

3. **Add both domains in Netlify**:
   - `mkphilatelic.com` (primary)
   - `www.mkphilatelic.com` (redirect to primary)

4. **Enable HTTPS**:
   - Netlify will automatically provision SSL certificate
   - Usually takes 5-15 minutes after DNS propagates

#### Option B: If you don't own mkphilatelic.com yet

1. **Purchase the domain** from:
   - Namecheap (https://www.namecheap.com/)
   - Google Domains (https://domains.google/)
   - Or any registrar

2. **Then follow Option A steps above**

#### Option C: Use Netlify Subdomain (Free)

If you just want to test or don't want a custom domain yet:
1. Your site is already live at: `[random-name].netlify.app`
2. You can customize the subdomain:
   - Go to "Site settings" → "Site details"
   - Click "Change site name"
   - Enter: `mkphilatelic`
   - New URL: `mkphilatelic.netlify.app`

### Step 3: Verify Deployment

Once deployed, check:
- [ ] Homepage loads correctly
- [ ] Navigation works on all pages
- [ ] All links are functioning
- [ ] Responsive design works on mobile
- [ ] Contact email links work

### Automatic Updates

Every time you push to the `main` branch on GitHub, Netlify will automatically rebuild and deploy your site!

## Troubleshooting

**Site not updating?**
- Check Netlify deploy logs
- Ensure you pushed to `main` branch
- Clear browser cache

**Custom domain not working?**
- DNS can take up to 48 hours to propagate (usually 15 minutes)
- Use https://dnschecker.org/ to verify DNS propagation
- Ensure you added both A record and CNAME

**HTTPS not working?**
- Wait 15-30 minutes after DNS setup
- Netlify automatically provisions Let's Encrypt certificates
- Check "Domain management" in Netlify for status

## Current Status

✅ GitHub Repository: https://github.com/michaelkernaghan/mkphilatelic
✅ Website Structure: Complete
✅ Netlify Config: Ready
⏳ Netlify Deployment: Pending
⏳ Custom Domain: Pending

## Need Help?

- Netlify Docs: https://docs.netlify.com/
- Custom domains: https://docs.netlify.com/domains-https/custom-domains/
- Support: https://www.netlify.com/support/
