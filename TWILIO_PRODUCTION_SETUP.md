# Twilio WhatsApp Production Setup Guide

This guide explains how to configure Twilio WhatsApp for production environment.

## Overview

Twilio supports two modes for WhatsApp messaging:
1. **Sandbox Mode** (Testing) - Limited to pre-approved numbers
2. **Production Mode** - Full WhatsApp Business API with your own number

## Current Configuration

The system uses environment variables to configure Twilio. Check your `.env` file for these settings:

```env
TWILIO_WHATSAPP_ENABLED=True
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_ENVIRONMENT=sandbox  # or 'production'
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

## Switching from Sandbox to Production

### Step 1: Get Your WhatsApp Business Number Approved

1. **Log in to Twilio Console**
   - Go to https://www.twilio.com/console
   - Navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**

2. **Request WhatsApp Business API Access**
   - Click on "Request Access" or "Get Started with WhatsApp"
   - Fill out the WhatsApp Business API application form
   - Provide business information:
     - Business name and description
     - Business website
     - Use case description
     - Expected message volume
   - Submit for approval (approval can take 1-3 business days)

3. **Get Your WhatsApp Business Number**
   - Once approved, Twilio will assign you a WhatsApp Business number
   - This number will be in format: `+1234567890` (with country code)
   - Note this number down

### Step 2: Update Environment Variables

Update your `.env` file (or production environment variables):

```env
# Enable WhatsApp
TWILIO_WHATSAPP_ENABLED=True

# Your Twilio credentials (same for sandbox and production)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-auth-token-here

# Switch to production mode
TWILIO_ENVIRONMENT=production

# Use your approved WhatsApp Business number
# Format: whatsapp:+1234567890 (replace with your actual number)
TWILIO_WHATSAPP_FROM=whatsapp:+1234567890
```

**Important Notes:**
- Replace `+1234567890` with your actual approved WhatsApp Business number
- The number must include the country code (e.g., `+94771234567` for Sri Lanka)
- Keep the `whatsapp:` prefix in the `TWILIO_WHATSAPP_FROM` value

### Step 3: Restart Your Application

After updating environment variables, restart your Django application:

```bash
# If using systemd
sudo systemctl restart your-app-name

# If using supervisor
supervisorctl restart your-app-name

# If running manually
# Stop and restart your Django server
```

### Step 4: Verify Production Setup

1. **Check Logs**
   - Monitor application logs to ensure Twilio client initializes correctly
   - Look for any error messages about invalid numbers

2. **Test Sending**
   - Try sending a WhatsApp message through your application
   - Verify it's sent from your production number (not sandbox number)

3. **Verify in Twilio Console**
   - Check your Twilio Console → Messaging → Logs
   - Messages should show as sent from your WhatsApp Business number

## Sandbox vs Production Comparison

| Feature | Sandbox | Production |
|---------|---------|------------|
| **Number** | `+14155238886` (Twilio's sandbox) | Your approved WhatsApp Business number |
| **Recipients** | Only pre-approved numbers | Any valid WhatsApp number |
| **Approval** | Instant (join sandbox) | Requires Twilio approval (1-3 days) |
| **Cost** | Free (limited) | Pay per message |
| **Use Case** | Testing & Development | Production & Live Users |
| **Message Templates** | Not required | Required for initial messages |

## Troubleshooting

### Error: "Invalid WhatsApp From number"

**For Sandbox:**
- Ensure `TWILIO_WHATSAPP_FROM=whatsapp:+14155238886`
- Verify recipient has joined your sandbox (send "join <keyword>" to +1 415 523 8886)

**For Production:**
- Verify your WhatsApp Business number is correct in `TWILIO_WHATSAPP_FROM`
- Ensure your WhatsApp Business API is approved and active
- Check Twilio Console → Messaging → Senders to see your approved numbers
- Format must be: `whatsapp:+1234567890` (with country code)

### Error: "WhatsApp messaging is not enabled"

- Set `TWILIO_WHATSAPP_ENABLED=True` in your `.env` file
- Restart your application after changing this setting

### Messages Not Sending in Production

1. **Check Approval Status**
   - Verify your WhatsApp Business API is fully approved in Twilio Console
   - Check for any pending approvals or restrictions

2. **Verify Number Format**
   - Production number must be in E.164 format: `+1234567890`
   - Include country code (e.g., `+94` for Sri Lanka)

3. **Check Message Templates**
   - Production requires message templates for initial messages
   - Create templates in Twilio Console → Messaging → Content Templates
   - Use template name in your message if required

4. **Review Twilio Logs**
   - Check Twilio Console → Monitor → Logs → Errors
   - Look for specific error codes and messages

## Environment-Specific Configuration

### Development/Testing (.env)
```env
TWILIO_ENVIRONMENT=sandbox
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### Production (.env.production or production environment)
```env
TWILIO_ENVIRONMENT=production
TWILIO_WHATSAPP_FROM=whatsapp:+94771234567  # Your actual WhatsApp Business number
```

## Additional Resources

- [Twilio WhatsApp Documentation](https://www.twilio.com/docs/whatsapp)
- [Twilio WhatsApp Business API Setup](https://www.twilio.com/docs/whatsapp/quickstart)
- [Twilio Console](https://www.twilio.com/console)
- [WhatsApp Business API Requirements](https://www.twilio.com/docs/whatsapp/requirements)

## Support

If you encounter issues:
1. Check Twilio Console for error messages
2. Review application logs
3. Verify all environment variables are set correctly
4. Contact Twilio Support if issues persist

