# HighLevel CRM Integration Guide - Phase 3

> **CURRENT STATUS: ON HOLD**
> 
> This guide contains the instructions for integrating with the **real** HighLevel API. Due to limitations with the current free/trial HighLevel account, API access is not available.
> 
> Our current project strategy is to use a **mock integration** for testing and development. For the most up-to-date plan, please see:
> 
> **[STRATEGY.md](./STRATEGY.md)**
> 
> These instructions are being kept for future use when a full HighLevel subscription with API access is available.

---


This guide provides step-by-step instructions for integrating HighLevel CRM with your n8n workflow for complete lead management.

## Overview

Your Phase 3 workflow now includes:
- Enhanced data validation with additional fields
- ChatGPT ad generation
- **HighLevel Contact Creation**
- **HighLevel Opportunity Creation**
- Complete CRM integration with response tracking

## Prerequisites

1. **HighLevel Account**: Active HighLevel account with API access
2. **API Key**: HighLevel API key with appropriate permissions
3. **Pipeline Setup**: HighLevel pipeline and stage configured
4. **Custom Fields**: Optional custom fields configured in HighLevel

## 1. HighLevel API Setup

### Get API Key:
1. Login to your HighLevel account
2. Go to **Settings** → **Integrations** → **API**
3. Click **Create API Key**
4. Copy the API key (starts with `Bearer `)

### Get Location ID:
1. In HighLevel, go to **Settings** → **Company**
2. Copy your **Location ID**

### Get Pipeline and Stage IDs:
1. Go to **Opportunities** → **Pipelines**
2. Select your pipeline
3. Note the **Pipeline ID** from URL or settings
4. Note the **Stage ID** for the initial stage

## 2. Configure Environment Variables

Add these to your `.env` file:
```bash
# HighLevel CRM Configuration
HIGHLEVEL_API_KEY=your_api_key_here
HIGHLEVEL_LOCATION_ID=your_location_id_here
HIGHLEVEL_PIPELINE_ID=your_pipeline_id_here
HIGHLEVEL_STAGE_ID=your_stage_id_here
```

## 3. Update Workflow Configuration

### Update the Phase 3 Workflow:
1. Import `crm-lead-workflow-phase3.json` to n8n
2. Update the HTTP Request nodes with your actual IDs
3. Configure HighLevel credentials

### Required Updates:
- **Create HighLevel Contact** node:
  - URL: `https://rest.gohighlevel.com/v1/contacts/`
  - Headers: `Authorization: Bearer YOUR_API_KEY`

- **Create HighLevel Opportunity** node:
  - URL: `https://rest.gohighlevel.com/v1/pipelines/YOUR_PIPELINE_ID/opportunities`
  - Headers: `Authorization: Bearer YOUR_API_KEY`

## 4. HighLevel Configuration

### Create Custom Fields (Optional):
1. Go to **Settings** → **Custom Fields**
2. Create these custom fields for contacts:
   - `budget` (Text)
   - `service` (Text)
   - `source` (Text)
   - `generated_ad` (Text)

### Pipeline Setup:
1. Create a pipeline called "Web Form Leads"
2. Add stages like:
   - "New Lead" (initial stage)
   - "Contacted"
   - "Qualified"
   - "Proposal Sent"
   - "Closed Won/Lost"

## 5. Test the Integration

### Test with curl:
```bash
curl -X POST "http://localhost:5678/webhook/crm-lead-phase3" \
  -H "Content-Type: application/json" \
  -d '{\n    "name": "Test User",\n    "email": "test@example.com",\n    "phone": "555-123-4567",\n    "service": "web-design",\n    "company": "Test Corp",\n    "budget": "$5000-$10000",\n    "message": "Looking for website redesign"\n  }'
```

### Expected Response:
```json
{
  "success": true,
  "message": "Lead processed successfully and added to CRM!",
  "leadData": { ... },
  "generatedAd": "...",
  "crmContactId": "contact_123",
  "crmOpportunityId": "opportunity_456"
}
```

## 6. HighLevel Configuration Checklist

### ✅ **Before Going Live:**
- [ ] API key configured with proper permissions
- [ ] Pipeline and stage IDs identified
- [ ] Custom fields created (optional)
- [ ] Workflow imported and configured
- [ ] Test leads created successfully
- [ ] Contact and opportunity creation verified
- [ ] Error handling tested

### ✅ **Production Setup:**
- [ ] Environment variables configured
- [ ] HighLevel credentials added to n8n
- [ ] Webhook endpoints updated
- [ ] Monitoring alerts configured
- [ ] Backup procedures in place

## 7. Monitoring and Maintenance

### **HighLevel Monitoring:**
- Monitor API rate limits (1000 requests/hour)
- Track contact creation success rates
- Monitor opportunity pipeline movement
- Set up alerts for API failures

### **Error Handling:**
- Retry logic for API failures
- Graceful degradation if CRM is unavailable
- Logging for debugging purposes
- User-friendly error messages

## 8. Advanced Configuration

### **Custom Field Mapping:**
You can map additional fields by updating the HTTP request bodies:
```json
{
  "firstName": $json.name,
  "email": $json.email,
  "phone": $json.phone,
  "companyName": $json.company,
  "customField": {
    "budget": $json.budget,
    "service": $json.service,
    "source": "web-form",
    "generated_ad": $json.generatedAd,
    "message": $json.message
  }
}
```

### **Pipeline Customization:**
Update the opportunity creation to match your specific pipeline structure:
```json
{
  "name": "Lead: " + $json.name + " - " + $json.service,
  "pipelineId": "YOUR_PIPELINE_ID",
  "stageId": "YOUR_STAGE_ID",
  "value": 2500,  // Adjust based on service
  "notes": "Generated Ad: " + $json.generatedAd + "\\n\\nBudget: " + $json.budget
}
```

## 9. Troubleshooting

### **Common Issues:**
- **401 Unauthorized**: Check API key permissions
- **404 Not Found**: Verify pipeline/stage IDs
- **429 Rate Limit**: Reduce request frequency
- **Validation Errors**: Check field mapping

### **Debug Steps:**
1. Check n8n execution logs
2. Verify HighLevel API key permissions
3. Test API endpoints directly
4. Check custom field configuration
5. Validate JSON payloads

## 10. Next Steps After Setup

1. **Test with real data** using the test form
2. **Monitor HighLevel dashboard** for incoming leads
3. **Set up automation rules** in HighLevel
4. **Configure follow-up sequences** in HighLevel
5. **Track conversion rates** and optimize

## Environment Setup Summary

Add these to your `.env` file:
```bash
# HighLevel CRM Configuration
HIGHLEVEL_API_KEY=your_api_key_here
HIGHLEVEL_LOCATION_ID=your_location_id_here
HIGHLEVEL_PIPELINE_ID=your_pipeline_id_here
HIGHLEVEL_STAGE_ID=your_stage_id_here
```

Your Phase 3 workflow is now ready for HighLevel CRM integration!
