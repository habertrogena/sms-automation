# Fixing MacroDroid Number Accumulation Issue

## Problem
MacroDroid is concatenating phone numbers instead of using each number separately.

## Solution Applied in Code
1. Added unique timestamp to each webhook request
2. Added delay between calls (0.5s)
3. Clean URL construction for each request

## Additional Fix Required in MacroDroid

You need to update your MacroDroid macro to prevent variable accumulation:

### Step 1: Clear Variable Before Reading
In your MacroDroid macro:
1. Add action: **Variables** → **Set Variable**
2. Set variable (e.g., `%phone_number`) to empty string `""`
3. **Before** reading from webhook

### Step 2: Read Webhook Parameter Correctly
1. In your macro, when reading webhook data:
2. Use: **Variables** → **Get Variable from Webhook**
3. Variable name: `phone_number` (exact match)
4. Store in: `%phone_number` (local variable)

### Step 3: Use Variable Immediately
1. After reading, immediately use `%phone_number` for the call
2. Don't store it in a global variable that persists

### Alternative: Use Webhook Data Directly
Instead of storing in a variable:
1. In **Make Call** action
2. Use webhook parameter directly: `%webhook_phone_number`
3. Or configure to read from webhook data directly

## Testing
After updating MacroDroid macro, test with:
```bash
python3 -m src.call_sender_automation
```

Each call should now use only the current number, not accumulated numbers.


