# Automation Apps Setup - No ADB/Root/Developer Options Needed

Since your device doesn't allow ADB access, we'll use automation apps that can be controlled via HTTP.

---

## Option 1: MacroDroid Webhook (Recommended - Free)

### Step 1: Install MacroDroid
1. Install **MacroDroid** from Google Play Store (free)
2. Open the app

### Step 2: Create Call Macro with Webhook Trigger

1. In MacroDroid, tap **+** to create new macro
2. **Trigger**: Select **Webhook**
   - MacroDroid will generate a webhook URL
   - **Copy this URL** - you'll need it!
   - Format: `https://trigger.macrodroid.com/xxxxx/your-webhook-id`
3. **Action**: Select **Phone** → **Make Call**
   - For phone number, you can:
     - Use a variable from webhook: `%webhook_data` or `%webhook_number`
     - Or use a fixed number for testing
4. **Save** the macro

### Step 3: Get Webhook URL

1. In MacroDroid, go to your macro
2. Tap on the **Webhook trigger**
3. **Copy the webhook URL** shown
4. It looks like: `https://trigger.macrodroid.com/xxxxx/abc123`

### Step 4: Update Script Settings

Edit `src/call_sender_automation.py`:
```python
MACRODROID_WEBHOOK_URL = "https://trigger.macrodroid.com/xxxxx/your-webhook-id"  # Paste your webhook URL here
```

### Step 5: Configure Macro to Receive Number

In your MacroDroid macro:
- The webhook can receive data via query parameters
- Use `%webhook_data` or configure to read from URL parameters
- Or set up the macro to read the `number` parameter from the webhook URL

### Step 5: Test

```bash
python3 -m src.call_sender_automation
```

---

## Option 2: Automate (Free Alternative)

### Step 1: Install Automate
1. Install **Automate** from Play Store (free)
2. Open the app

### Step 2: Create Call Flow

1. Create new flow
2. Add block: **HTTP Server** → **Listen**
   - Set path: `/make_call`
3. Add block: **Phone** → **Call**
   - Use variable from HTTP request for number
4. Save and start flow

### Step 3: Enable HTTP Server

1. Automate → Settings → HTTP Server
2. Enable HTTP Server
3. Note IP and port

### Step 4: Update Script

Edit `src/call_sender_automation.py`:
```python
AUTOMATE_IP = "192.168.1.102"
AUTOMATE_PORT = 8080
```

---

## Option 3: Use Existing SMS Gateway (If It Supports Calls)

If your SMS Gateway app also supports calls:

1. Check SMS Gateway API documentation
2. Modify `call_sender_automation.py` to use SMS Gateway API
3. Use the same credentials from `settings.py`

---

## Option 4: Webhook Services (Advanced)

### Using IFTTT / Zapier

1. Create webhook on IFTTT/Zapier
2. Connect to Android automation (if available)
3. Use webhook URL in script

---

## Quick Setup: MacroDroid

**Fastest method:**

1. **Install MacroDroid** (Play Store)
2. **Create macro:**
   - Trigger: HTTP Trigger (`make_call`)
   - Action: Make Call (use `%http_number`)
3. **Enable HTTP Server** in settings
4. **Update script** with your device IP
5. **Run:** `python3 -m src.call_sender_automation`

---

## Testing Connection

Test if automation app is reachable:

```bash
# Test MacroDroid
curl http://192.168.1.102:8080/trigger?trigger=make_call&number=0712345678

# Should return success if working
```

---

## Advantages

✅ **No ADB needed**
✅ **No root required**
✅ **No Developer Options needed**
✅ **Works on restricted devices**
✅ **Free apps available**

---

## Limitations

⚠ **Call ending**: Automation apps may not be able to end calls programmatically
⚠ **Requires app setup**: Need to configure macro/flow
⚠ **Network required**: Device and computer must be on same WiFi

---

## Next Steps

1. Choose an automation app (MacroDroid recommended)
2. Follow setup steps above
3. Test connection
4. Run: `python3 -m src.call_sender_automation`

