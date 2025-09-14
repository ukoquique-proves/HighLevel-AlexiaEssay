# HighLevel API Token Generation Guide (OAuth 2.0)

This guide provides the step-by-step instructions to manually generate an Access Token for the HighLevel API, following the current OAuth 2.0 standards. This token can be used for immediate testing of the n8n workflow.

**Note**: The Access Token generated via this manual process is temporary and will expire (e.g., in 24 hours). For a permanent solution, we will create a Python script to automatically refresh the token (see `PYTHON_INCLUSION.md`).

---

## Step 1: Create a Private App in HighLevel

First, you need to register a private application within your HighLevel account to get your credentials.

1.  Log in to your HighLevel account.
2.  Go to the **Agency** view.
3.  In the left-hand menu, click on **Settings**.
4.  Look for **"Labs"** or **"Labs Features"** in the settings menu and click it. If you don't see it, ensure you are in the **Agency** view, not a sub-account.
5.  Within the **Labs** section, find **"Private Integrations"** or **"Developer Apps"** and enable it.
6.  After enabling, a new menu item **"Private Integrations"** or **"API"** should appear in the main settings menu. Click on it.
7.  Click **"Create New Private App"** (or similar button).
8.  Give your app a name like "n8n Automation Project".
9.  Once created, HighLevel will provide you with a **Client ID** and a **Client Secret**. Copy these immediately and save them somewhere secure. You will need them in the next steps.

## Step 2: Construct the Authorization URL

Now, you need to build a special URL to authorize your app. This URL will ask you to grant permission for your app to access your HighLevel data.

-   **Base URL**: `https://marketplace.gohighlevel.com/oauth/chooselocation`

-   **Parameters needed**:
    -   `response_type=code`
    -   `redirect_uri=https://www.google.com` (For this manual process, using Google is fine).
    -   `client_id=YOUR_CLIENT_ID` (Paste the Client ID from Step 1).
    -   `scope=contacts.write opportunities.write` (The permissions we need).

**Your final URL will look like this (replace with your actual Client ID):**
```
https://marketplace.gohighlevel.com/oauth/chooselocation?response_type=code&redirect_uri=https://www.google.com&client_id=YOUR_CLIENT_ID&scope=contacts.write opportunities.write
```

## Step 3: Get the Authorization Code

1.  Paste the complete URL from Step 2 into your web browser and press Enter.
2.  You will be prompted to log in to HighLevel (if you aren't already).
3.  You will see a screen asking you to select your account/location and authorize the app. Select your location and click **"Proceed"**.
4.  After you approve, the browser will redirect to Google. **Look at the URL in your browser's address bar.** It will look something like this:
    ```
    https://www.google.com/?code=A_VERY_LONG_STRING_OF_CHARACTERS
    ```
5.  **Immediately copy the `code` value**. This is your temporary Authorization Code. It is only valid for a few minutes.

## Step 4: Exchange the Code for an Access Token

Now, we will use the `code` you just copied to get the actual Access Token. We'll do this with a `curl` command in your terminal.

Prepare the following command. Replace `YOUR_CLIENT_ID`, `YOUR_CLIENT_SECRET`, and `THE_CODE_YOU_COPIED` with your actual values.

```bash
curl -X POST 'https://api.gohighlevel.com/OAuth/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'grant_type=authorization_code' \
-d 'client_id=YOUR_CLIENT_ID' \
-d 'client_secret=YOUR_CLIENT_SECRET' \
-d 'code=THE_CODE_YOU_COPIED' \
-d 'redirect_uri=https://www.google.com'
```

## Step 5: Receive and Use Your Tokens

When you run the `curl` command, the terminal will return a JSON object containing your tokens. It will look like this:

```json
{
  "access_token": "A_VERY_LONG_ACCESS_TOKEN_STRING",
  "token_type": "Bearer",
  "expires_in": 86400,
  "refresh_token": "A_VERY_LONG_REFRESH_TOKEN_STRING",
  "scope": "contacts.write opportunities.write",
  "userType": "Location",
  "locationId": "YOUR_LOCATION_ID"
}
```

**Success!**

-   The `access_token` is what you will use for testing the n8n workflow.
-   **Save the `refresh_token` somewhere very safe.** We will need it for our Python script to automate this process later.

## Next Step: Testing the n8n Workflow

Now you have a valid `access_token`. You can proceed with testing the Phase 3 workflow. In the n8n "Create HighLevel Contact" and "Create HighLevel Opportunity" nodes, you will need to set the authentication header like this:

-   **Header Name**: `Authorization`
-   **Header Value**: `Bearer YOUR_ACCESS_TOKEN`
