# N8N Setup and Best Practices Guide

This document contains essential guidelines and troubleshooting steps for working with n8n workflows, based on real-world experience and common obstacles encountered during development.

## Table of Contents
1. [Workflow Development Best Practices](#workflow-development-best-practices)
2. [Code Node Guidelines](#code-node-guidelines)
3. [Webhook Configuration](#webhook-configuration)
4. [API Management](#api-management)
5. [Common Issues and Solutions](#common-issues-and-solutions)
6. [Debugging Techniques](#debugging-techniques)

---

## Workflow Development Best Practices

### 1. Workflow Naming and Organization
- **Use descriptive names**: "CRM Lead Processing with Mock AI" not "My workflow"
- **Version your workflows**: Add version suffixes like "-v1", "-fixed", "-enhanced"
- **Organize in directories**: Use `workflows/` folder for better project structure
- **Clean up obsolete files**: Remove old/unused workflow files regularly

### 2. Workflow Structure
- **Always use error handling**: Connect error outputs to error response nodes
- **Validate early**: Put validation nodes immediately after webhook/trigger nodes
- **Use consistent node naming**: "Enhanced Data Validation", "Mock ChatGPT Ad Generator"
- **Document complex logic**: Add comments in code nodes explaining the purpose

---

## Code Node Guidelines

### 1. Data Access Patterns
**❌ WRONG - Assumes direct data access:**
```javascript
const name = data.name;
const email = data.email;
```

**✅ CORRECT - Robust data access:**
```javascript
const data = items[0].json;
const name = (data.name || data.body?.name || '').toString().trim();
const email = (data.email || data.body?.email || '').toString().trim().toLowerCase();
```

### 2. Error Handling in Code Nodes
**❌ WRONG - Silent failures:**
```javascript
if (!name) return [];
```

**✅ CORRECT - Explicit error throwing:**
```javascript
if (!name) {
  throw new Error('Name is required');
}
```

### 3. Data Validation Best Practices
```javascript
// Always validate and clean data
const errors = [];
const name = (data.name || '').toString().trim();
const email = (data.email || '').toString().trim().toLowerCase();

// Collect all validation errors
if (!name) errors.push('Name is required');
if (!email) errors.push('Email is required');

// Email format validation
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (email && !emailRegex.test(email)) {
  errors.push('Invalid email format');
}

// Throw all errors at once
if (errors.length > 0) {
  throw new Error('Validation failed: ' + errors.join(', '));
}
```

### 4. Return Data Structure
**❌ WRONG - Inconsistent return:**
```javascript
return response;
```

**✅ CORRECT - Always return array with json property:**
```javascript
return [{ json: response }];
```

### 5. Debugging in Code Nodes
```javascript
// Add console.log for debugging
console.log('Received data:', JSON.stringify(data, null, 2));
console.log('Parsed fields:', { name, email, phone, service });
console.log('Output data:', JSON.stringify(result, null, 2));
```

---

## Webhook Configuration

### 1. Webhook Path Naming
- **Use descriptive paths**: `/crm-lead-enhanced` not `/webhook1`
- **Avoid conflicts**: Check existing webhook paths before creating new ones
- **Use consistent naming**: Match workflow name with webhook path

### 2. Webhook Registration Issues
**Common Problem**: Webhook shows as active in UI but returns 404

**Solutions**:
1. **Deactivate and reactivate** the workflow in the UI
2. **Restart n8n Docker container** if webhook registration fails
3. **Check for path conflicts** with other workflows
4. **Use test webhook first**: `/webhook-test/path` before production `/webhook/path`

### 3. Response Mode Configuration
- **Always use `responseNode`** for custom responses
- **Connect all paths to response nodes** (success and error)
- **Set Response Body correctly**: `={{ $json }}` for dynamic content

---

## API Management

### 1. n8n API Authentication
```bash
# Always use X-N8N-API-KEY header
curl -H "X-N8N-API-KEY: your_key_here" "http://localhost:5678/api/v1/workflows"
```

### 2. Workflow JSON Format for API
**Required properties for workflow upload:**
```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {...},
  "settings": {},
  "staticData": null
}
```

**❌ AVOID - Additional properties that cause API errors:**
- `active` (read-only via API)
- `versionId` (auto-generated)
- `meta` (auto-generated)
- `tags` (optional, can cause issues)

### 3. Common API Operations
```bash
# List workflows
curl -s -H "X-N8N-API-KEY: key" "http://localhost:5678/api/v1/workflows"

# Get specific workflow
curl -s -H "X-N8N-API-KEY: key" "http://localhost:5678/api/v1/workflows/ID"

# Upload new workflow
curl -X POST -H "Content-Type: application/json" -H "X-N8N-API-KEY: key" \
  --data-binary @workflow.json "http://localhost:5678/api/v1/workflows"

# Update existing workflow
curl -X PUT -H "Content-Type: application/json" -H "X-N8N-API-KEY: key" \
  --data-binary @workflow.json "http://localhost:5678/api/v1/workflows/ID"
```

---

## Common Issues and Solutions

### 1. Empty Webhook Responses
**Symptoms**: HTTP 200 but empty response body

**Causes & Solutions**:
- **Respond to Webhook node not connected**: Connect success path to response node
- **Wrong Response Body configuration**: Use `={{ $json }}` not `=={{ $json }}`
- **Code node returning wrong format**: Return `[{ json: data }]` not just `data`
- **Workflow not properly activated**: Deactivate/reactivate in UI

### 2. Validation Errors
**Symptoms**: "Name is required, Email is required" even with valid data

**Causes & Solutions**:
- **Data access issues**: Use robust data access patterns (see Code Node Guidelines)
- **Type conversion problems**: Always convert to string with `.toString()`
- **Nested data structures**: Check both `data.field` and `data.body?.field`

### 3. Workflow Activation Issues
**Symptoms**: Workflow shows active in UI but webhook returns 404

**Solutions**:
1. Check the correct workflow is selected in UI
2. Verify webhook path matches the URL being tested
3. Restart n8n container: `docker compose restart`
4. Use API to verify active status: `GET /api/v1/workflows/ID`

### 4. API Upload Failures
**Common Error Messages & Solutions**:

- `"must have required property 'name'"`: Missing workflow name
- `"must NOT have additional properties"`: Remove read-only properties
- `"must have required property 'settings'"`: Add `"settings": {}` to JSON

---

## Debugging Techniques

### 1. Workflow Execution Debugging
1. **Check Executions List**: View recent workflow runs
2. **Click on execution**: See data flow between nodes
3. **Check node outputs**: Verify each node produces expected data
4. **Look for error messages**: Red nodes indicate failures

### 2. Console Logging in Code Nodes
```javascript
// Log input data
console.log('Input:', JSON.stringify(items[0].json, null, 2));

// Log processing steps
console.log('Validation result:', { isValid, errors });

// Log output data
console.log('Output:', JSON.stringify(result, null, 2));
```

### 3. Test Webhook Debugging
```bash
# Test with verbose output
curl -v -X POST "http://localhost:5678/webhook/path" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Test with headers visible
curl -i -X POST "http://localhost:5678/webhook/path" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### 4. API Debugging
```bash
# Check workflow status
curl -s -H "X-N8N-API-KEY: key" \
  "http://localhost:5678/api/v1/workflows/ID" | grep '"active"'

# List all active workflows
curl -s -H "X-N8N-API-KEY: key" \
  "http://localhost:5678/api/v1/workflows" | grep -E '"name"|"active"'
```

---

## Workflow Management Policy

### 1. File Organization Strategy
```
workflows/
├── crm-lead-workflow.json              # PRODUCTION VERSION (current)
├── archive/
│   ├── crm-lead-workflow-v1-minimal.json    # Historical versions
│   ├── crm-lead-workflow-v2-enhanced.json
│   ├── crm-lead-workflow-v3-enhanced-clean.json
│   └── crm-lead-workflow-v4-enhanced-fixed.json
└── examples/
    ├── crm-lead-workflow-mock-example.json      # Mock/teaching version
    └── crm-lead-workflow-simplified-example.json # Basic example
```

### 2. Production Workflow Rules
- **ONE workflow per business process** - Never create multiple similar workflows
- **Stable webhook paths** - Use `/webhook/crm-lead` not `/webhook/crm-lead-v2`
- **Descriptive but consistent naming** - `{process-name}-workflow.json`
- **Version via git commits** - Not via filename suffixes

### 3. Development Process
1. **Make changes to existing workflow** via n8n UI
2. **Export and overwrite** the production workflow file
3. **Commit to git** with descriptive commit message
4. **Never create new workflow files** for minor changes
5. **Use git branches** for major workflow redesigns

### 4. Avoiding Workflow Proliferation
**❌ DON'T CREATE:**
- `workflow-v2.json`, `workflow-fixed.json`, `workflow-enhanced.json`
- Multiple similar webhook endpoints
- Test workflows that stay in production

**✅ DO INSTEAD:**
- Update existing workflow in n8n UI
- Use git history for version tracking
- Archive old versions only when major redesign occurs
- Use examples/ for teaching/reference workflows

### 5. Webhook Endpoint Management
- **Production**: `/webhook/crm-lead` (stable, never changes)
- **Development**: Use `/webhook-test/crm-lead` for testing
- **Avoid**: `/webhook/crm-lead-v2`, `/webhook/crm-lead-fixed`, etc.

### 6. n8n Instance Cleanup
Before major changes:
1. **Deactivate old workflows** in n8n UI
2. **Delete unused workflows** from n8n instance
3. **Keep only current production workflow active**
4. **Document which workflow is production** in README

---

## Environment Setup Best Practices

### 1. Docker Configuration
```yaml
# docker-compose.yml
services:
  n8n:
    image: n8nio/n8n:1.108.2  # Pin specific version
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_SECURE_COOKIE=false  # For local development
      - DB_SQLITE_POOL_SIZE=10   # Improve performance
    volumes:
      - n8n_data:/home/node/.n8n
    ports:
      - "5678:5678"
```

### 2. Environment Variables (.env)
```bash
# Never commit to git - add to .gitignore
N8N_USER=admin
N8N_PASSWORD=secure_password_here
N8N_API_KEY=generated_api_key_here
```

### 3. Git Best Practices
```bash
# .gitignore
.env
*.log
node_modules/
.n8n/
```

---

## Quick Reference Checklist

### Before Creating a Workflow:
- [ ] Plan the data flow and validation requirements
- [ ] Choose descriptive names for workflow and nodes
- [ ] Design error handling paths

### When Writing Code Nodes:
- [ ] Use robust data access patterns
- [ ] Add console.log statements for debugging
- [ ] Validate all input data
- [ ] Return data in correct format: `[{ json: data }]`
- [ ] Handle errors explicitly with throw statements

### When Configuring Webhooks:
- [ ] Use descriptive webhook paths
- [ ] Set responseMode to "responseNode"
- [ ] Connect all paths to response nodes
- [ ] Test with `/webhook-test/` first

### When Using n8n API:
- [ ] Include X-N8N-API-KEY header
- [ ] Remove read-only properties from JSON
- [ ] Include required properties (name, settings, staticData)
- [ ] Test API calls with curl before automation

### When Debugging Issues:
- [ ] Check workflow executions list
- [ ] Verify webhook activation status
- [ ] Test with simple data first
- [ ] Check console logs in code nodes
- [ ] Use verbose curl commands for webhook testing

---

## Additional Resources

- **n8n Documentation**: https://docs.n8n.io/
- **n8n API Reference**: https://docs.n8n.io/api/
- **Docker Compose Guide**: https://docs.docker.com/compose/
- **Webhook Testing Tools**: curl, Postman, Insomnia

---

*This guide is based on real-world experience developing CRM automation workflows with n8n. Keep it updated as you encounter new issues and solutions.*
