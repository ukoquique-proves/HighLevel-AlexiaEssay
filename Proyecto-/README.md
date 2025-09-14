# CRM Automation Project - PROYECTO

## Overview
This project implements an automated CRM workflow system using n8n, ChatGPT, and HighLevel CRM. The system captures leads from forms, validates data, generates personalized advertisements using AI, and stores everything in a CRM system.

For a detailed explanation of the business and technical strategy, see [STRATEGY.md](./STRATEGY.md).

## Project Architecture

### Core Workflow
```
Form Submission → Data Validation → ChatGPT Ad Generation → HighLevel CRM Storage → Response
```

### Technology Stack
- **n8n**: Workflow automation platform (version 1.108.2)
- **OpenAI ChatGPT**: AI-powered advertisement generation
- **HighLevel CRM**: Lead management and storage
- **HTML/JavaScript**: Test form interface
- **Docker**: Containerized n8n deployment

## Project Structure

### GitHub Upload Status
This project was successfully uploaded to GitHub on 2025-09-08 using:
- Git repository initialized and committed locally
- Secure token-based push to https://github.com/ukoquique-proves/n8n-API-usage
- All workflow files, documentation, and configuration uploaded

### Directory Layout

See also: [STRATEGY.md](./STRATEGY.md) for the project's strategic context and documentation map.

```
PROYECTO/
├── README.md                           # This file - project overview
├── STRATEGY.md                         # Strategic context and documentation map
├── FIRST_STEPS.md                      # Getting started guide
├── N8N_SETUP.md                        # N8N configuration and best practices
├── API_SETUP_GUIDE.md                  # API credentials and setup
├── HIGHLEVEL_SETUP_GUIDE.md            # HighLevel CRM configuration
├── BUSINESS_STRATEGY_UPDATE.md         # Historical pivots and commercialization
├── COMPETITIVE_ANALYSIS.md             # Market analysis and positioning
├── PYTHON_INCLUSION.md                 # Python integration considerations
├── CHANGELOG.md                        # Version history and updates
├── test-form.html                      # Web form for testing workflows
├── hector-test-dashboard.html          # Comprehensive API & N8N testing dashboard
├── highlevel_token_manager.py          # HighLevel API token management
└── workflows/
    ├── crm-lead-processing-mock-highlevel.json  # Main workflow with extensible business logic
    ├── examples/
    └── archive/
```

## Current Implementation Status

### ✅ Completed (Phase 1 - Foundation)
- **Step 1**: Reference materials copied from CRM-00 project
- **Step 2**: Test environment created in n8n
  - Webhook endpoint active: `http://localhost:5678/webhook/crm-lead`
  - Basic data validation workflow imported and running
  - Test form configured and ready

### 🔄 In Progress
- **Step 3**: Basic data validation testing
- **Step 4**: OpenAI integration (planned)
- **Step 5**: HighLevel CRM integration (planned)

### 📋 Planned (Phase 2 & 3)
- Advanced automation features
- Anti-spam validation
- Personalization based on demographics
- Reporting dashboard
- Performance optimization
- Team documentation

## Quick Start

### Prerequisites
- n8n instance running at `http://localhost:5678`
- API credentials for OpenAI and HighLevel (see API_SETUP_GUIDE.md)

### Testing the Current Setup
1. **Verify n8n is running**:
   ```bash
   curl -X POST "http://localhost:5678/webhook/crm-lead" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test", "email": "test@example.com", "phone": "+1234567890", "service": "Test"}'
   ```

2. **Use the test form**:
   - Open `test-form.html` in a web browser
   - Fill out the form with test data
   - Submit and verify webhook processing

### Current Workflow Features
- **Data Validation**: Validates required fields (name, email, phone, service)
- **Email Validation**: Checks email format using regex
- **Phone Validation**: Basic phone number format validation
- **Data Cleaning**: Trims whitespace and standardizes formats
- **Error Handling**: Returns appropriate error messages for invalid data
- **JSON Response**: Structured success/error responses

## API Endpoints

### Webhook Endpoint
- **URL**: `http://localhost:5678/webhook/crm-lead`
- **Method**: POST
- **Content-Type**: application/json

### Required Fields
```json
{
  "name": "string (required)",
  "email": "string (required, valid email format)",
  "phone": "string (required, valid phone format)",
  "service": "string (required)"
}
```

### Optional Fields
```json
{
  "company": "string",
  "budget": "string",
  "message": "string"
}
```

### Response Format
**Success Response:**
```json
{
  "success": true,
  "message": "Lead processed successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error description",
  "message": "Failed to process lead"
}
```

## Implementation Approach

### Safety-First Strategy
This project follows a **phased, incremental implementation** approach to minimize risks:

1. **Phase 1**: Foundation Setup (Safe & Simple)
2. **Phase 2**: API Integration (Controlled)
3. **Phase 3**: Complete Workflow (Gradual)

Each step is tested independently before proceeding to ensure system stability.

## Configuration

### Environment Variables
Credentials are stored securely in the parent directory's `.env` file:
- `N8N_USERNAME`: n8n login username
- `N8N_PASSWORD`: n8n login password
- `N8N_API_KEY`: n8n API authentication key

### n8n Instance
- **URL**: http://localhost:5678
- **Version**: 1.108.2 (chosen for API compatibility)
- **API Enabled**: Yes
- **Authentication**: Basic auth + API key

## Development Guidelines

### Testing
- Always use test data, never production data
- Test each component in isolation before integration
- Verify webhook responses before proceeding

### Safety Measures
- Create backups before major changes
- Test new components separately
- Use incremental implementation approach
- Monitor execution logs for errors

## Troubleshooting

### Common Issues
- **404 Webhook Error**: Ensure workflow is active in n8n
- **Validation Errors**: Check required fields in form submission
- **Connection Issues**: Verify n8n instance is running

### Debug Steps
1. Check n8n execution logs
2. Test webhook with curl
3. Verify form data format
4. Check network connectivity

## Related Documentation
- **Parent Project**: `/home/uko/COLOMBIA/OLD_N8N/README.md`
- **Reference Implementation**: `/home/uko/COLOMBIA/CRM-00/`
- **Implementation Plan**: `FIRST_STEPS.md`
- **API Setup**: `API_SETUP_GUIDE.md`
- **Change History**: `CHANGELOG.md`

## License
This project is for internal use. See parent project license for details.

---

**Last Updated**: 2025-09-07  
**Current Version**: 0.2.0  
**Implementation Status**: Phase 1 - Foundation Setup (2/3 steps completed)
