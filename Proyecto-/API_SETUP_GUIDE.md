# API Credentials Setup Guide

### [2025-09-07] API-driven Workflow Patch
- Used n8n API to patch validation logic and fix webhook response.
- Environment is now stable for further CRM automation.

## 0. n8n API Setup and Usage

### Generate n8n API Key:
1. Open n8n at http://localhost:5678
2. Click your user profile (top right)
3. Go to "Settings" → "API Keys"
4. Click "Create API Key"
5. Copy the generated key (starts with `eyJ...`)

### n8n API Authentication:
All n8n API requests require the `X-N8N-API-KEY` header:
```bash
curl -H "X-N8N-API-KEY: your_api_key_here" "http://localhost:5678/api/v1/workflows"
```

### Common n8n API Operations:

#### List All Workflows:
```bash
curl -s -H "X-N8N-API-KEY: your_key" "http://localhost:5678/api/v1/workflows"
```

#### Get Specific Workflow:
```bash
curl -s -H "X-N8N-API-KEY: your_key" "http://localhost:5678/api/v1/workflows/WORKFLOW_ID"
```

#### Update Workflow (Patch Logic):
```bash
curl -X PUT "http://localhost:5678/api/v1/workflows/WORKFLOW_ID" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: your_key" \
  --data-binary @workflow.json
```

#### Test Webhook Directly:
```bash
curl -v -X POST "http://localhost:5678/webhook/crm-lead" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com"}'
```

### Workflow Management via API:
- **Download workflows** for backup/version control
- **Patch validation logic** without UI interaction
- **Bulk update workflows** across environments
- **Automate deployment** of workflow changes

### API Limitations Encountered:
- `/execute` endpoint not available in all n8n versions
- Workflow `active` property is read-only via API
- Some node parameters require specific formatting
- Webhook registration requires workflow activation

## 1. OpenAI / GPT-4

### Get API Key:
1. Go to https://platform.openai.com/
2. Create account or login
3. Go to API Keys section
4. Create new secret key
5. Copy the key (starts with sk-...)

### Usage Limits:
- Free tier: $5 credit (expires after 3 months)
- Pay-as-you-go: $0.03 per 1K tokens (GPT-4)
- Rate limits: 3 requests/minute (free tier)

### N8N Configuration:
```
API Key: sk-your-key-here
Model: gpt-4 or gpt-3.5-turbo
Base URL: https://api.openai.com/v1 (default)
```

---

## Groq (Free OpenAI-Compatible Alternative)

### Get API Key:
1. Go to https://console.groq.com
2. Sign up for free account (Google/GitHub login available)
3. Navigate to API Keys section
4. Create new API key
5. Copy the key (starts with gsk-...)

### Usage Limits:
- **Free tier**: Very generous limits
- **Speed**: Extremely fast inference (great for demos)
- **Models**: Llama 3, Mixtral, Gemma
- **Rate limits**: Much higher than OpenAI free tier

### N8N Configuration:
```
API Key: gsk-your-key-here
Model: llama3-8b-8192 or mixtral-8x7b-32768
Base URL: https://api.groq.com/openai/v1
```

### Recommended Models:
- **llama3-8b-8192**: Fast, good for general tasks
- **mixtral-8x7b-32768**: Better quality, larger context
- **llama3-70b-8192**: Highest quality (slower)

### Benefits for Development:
- OpenAI-compatible format (easy migration later)
- No credit card required
- Very fast responses
- Perfect for testing and development

## 2. HighLevel CRM Setup

### Get API Key:
1. Login to your HighLevel account
2. Go to Settings → Integrations → API
3. Create new API key
4. Copy the API key

### Get Location ID:
1. In HighLevel, go to Settings → Company
2. Copy your Location ID

### Add to n8n:
1. In n8n Settings → Credentials
2. Click "Add Credential"
3. Select "HighLevel"
4. Enter API key and Location ID
5. Test connection

## 3. Import Workflow to n8n

### Steps:
1. Open n8n dashboard
2. Click "Import from File"
3. Select `workflows/crm-lead-workflow.json`
4. Assign credentials to nodes:
   - OpenAI node → Your OpenAI credential
   - HighLevel nodes → Your HighLevel credential
5. Save workflow
6. Activate workflow

## 4. Test the Integration

### Using Test Form:
1. Open `test-form.html` in browser
2. Update WEBHOOK_URL in the form to your n8n webhook URL
3. Fill out and submit form
4. Check n8n execution log
5. Verify contact created in HighLevel

### Webhook URL Format:
```
http://localhost:5678/webhook/crm-lead
```

## 5. Troubleshooting

### Common Issues:
- **401 Unauthorized**: Check API keys are correct
- **Webhook not triggering**: Verify webhook URL and method (POST)
- **Validation errors**: Check required fields in form
- **HighLevel errors**: Verify Location ID and permissions

### Debug Steps:
1. Check n8n execution logs
2. Test each node individually
3. Verify API credentials
4. Check network connectivity

## 6. n8n Version Analysis and Troubleshooting

### Current Version: n8n:1.108.2

#### ✅ **Pros of n8n:1.108.2:**
- **API Key Authentication**: Fully supported and working
- **Workflow Upload/Download**: Complete API support for workflow management
- **Webhook Registration**: Works reliably once activated in UI
- **Code Nodes**: Full JavaScript support with console logging
- **Docker Stability**: Stable containerized deployment
- **JSON Workflow Format**: Consistent and well-documented

#### ❌ **Cons and Limitations Encountered:**

**1. Workflow Activation API Issues:**
```bash
# These methods don't work reliably in 1.108.2:
curl -X PATCH "/api/v1/workflows/ID/activate"     # Method not allowed
curl -X POST "/api/v1/workflows/ID/activate"      # Endpoint not found
```
**Workaround**: Manual activation in n8n UI required

**2. Webhook Registration Delays:**
- Webhooks sometimes don't register immediately after workflow activation
- UI shows "active" but API shows "inactive" (sync issues)
**Workaround**: Deactivate/reactivate workflow in UI, or restart container

**3. Direct Workflow Execution API:**
```bash
# Not available in this version:
curl -X POST "/api/v1/workflows/ID/execute"       # Endpoint missing
```
**Workaround**: Use webhook endpoints for testing

**4. Bulk Operations:**
- No bulk activate/deactivate endpoints
- Must handle workflows individually
**Workaround**: Script individual API calls

### Alternative n8n Versions Analysis

#### **n8n:latest (1.70.x+)**
**Pros:**
- Enhanced API endpoints for workflow management
- Better webhook registration reliability
- Improved bulk operations support
- More consistent UI/API synchronization

**Cons:**
- Potential breaking changes in workflow format
- May require migration of existing workflows
- Different authentication mechanisms in newer versions
- Less stable for production (bleeding edge)

**Migration Risk**: Medium - Workflow JSON format changes possible

#### **n8n:1.120.x - 1.130.x (Recommended Upgrade)**
**Pros:**
- Maintains API key authentication compatibility
- Fixes workflow activation API endpoints
- Improved webhook registration
- Better error handling in API responses
- Maintains backward compatibility with 1.108.2 workflows

**Cons:**
- Requires testing of existing workflows
- Minor configuration changes may be needed

**Migration Risk**: Low - High compatibility with current setup

#### **n8n:2.x.x (Future)**
**Pros:**
- Complete API overhaul with better endpoints
- Enhanced workflow management capabilities
- Improved performance and reliability

**Cons:**
- Major breaking changes expected
- Complete workflow migration required
- Authentication system changes likely

**Migration Risk**: High - Major version upgrade

### Recommended Upgrade Path

#### **Phase 1: Stay on 1.108.2 (Current)**
**When to use**: Production stability is priority
```yaml
# docker-compose.yml
services:
  n8n:
    image: n8nio/n8n:1.108.2  # Pin current stable version
```

**Workarounds for limitations**:
- Manual workflow activation in UI
- Container restart for webhook registration issues
- Use webhook endpoints instead of direct execution API

#### **Phase 2: Upgrade to 1.120.x-1.130.x (Recommended)**
**When to use**: Need better API functionality without major risks
```yaml
# docker-compose.yml
services:
  n8n:
    image: n8nio/n8n:1.125.0  # Stable with improved API
```

**Before upgrading**:
1. **Backup current workflows**: Export all via API
2. **Test in development**: Spin up new version in parallel
3. **Validate API endpoints**: Test activation/deactivation APIs
4. **Check webhook registration**: Ensure immediate registration works

#### **Phase 3: Monitor n8n:latest (Future)**
**When to use**: After thorough testing and when new features are needed

### API Limitations Workaround Scripts

#### **Workflow Activation Script** (for current version):
```bash
#!/bin/bash
# activate_workflow.sh - Manual activation helper

WORKFLOW_ID=$1
API_KEY="your_api_key_here"

echo "⚠️  Manual activation required for workflow: $WORKFLOW_ID"
echo "1. Open n8n UI: http://localhost:5678"
echo "2. Find workflow: $WORKFLOW_ID"
echo "3. Click the toggle to activate"
echo "4. Verify webhook registration with:"
echo "   curl -X POST http://localhost:5678/webhook/your-path -d '{}'"
```

#### **Workflow Status Checker**:
```bash
#!/bin/bash
# check_workflows.sh - Status verification

API_KEY="your_api_key_here"

echo "🔍 Active Workflows:"
curl -s -H "X-N8N-API-KEY: $API_KEY" \
  "http://localhost:5678/api/v1/workflows" | \
  jq -r '.data[] | select(.active==true) | "\(.name) (ID: \(.id))"'

echo -e "\n⏸️  Inactive Workflows:"
curl -s -H "X-N8N-API-KEY: $API_KEY" \
  "http://localhost:5678/api/v1/workflows" | \
  jq -r '.data[] | select(.active==false) | "\(.name) (ID: \(.id))"'
```

### Version-Specific API Endpoints

#### **n8n:1.108.2 (Current) - Working Endpoints:**
```bash
# ✅ Reliable endpoints:
GET    /api/v1/workflows              # List workflows
GET    /api/v1/workflows/:id          # Get workflow
POST   /api/v1/workflows              # Create workflow
PUT    /api/v1/workflows/:id          # Update workflow
DELETE /api/v1/workflows/:id          # Delete workflow

# ❌ Problematic endpoints:
PATCH  /api/v1/workflows/:id/activate # Not reliable
POST   /api/v1/workflows/:id/execute  # Not available
```

#### **n8n:1.120+ - Enhanced Endpoints:**
```bash
# ✅ All 1.108.2 endpoints PLUS:
PATCH  /api/v1/workflows/:id/activate   # Fixed activation
PATCH  /api/v1/workflows/:id/deactivate # Fixed deactivation
POST   /api/v1/workflows/:id/execute    # Direct execution
GET    /api/v1/executions              # Enhanced execution logs
```

### Upgrade Decision Matrix

| Feature Needed | Stay 1.108.2 | Upgrade 1.120+ | Wait for 2.x |
|----------------|---------------|----------------|---------------|
| API Key Auth | ✅ | ✅ | ❓ |
| Workflow Upload | ✅ | ✅ | ✅ |
| Auto Activation | ❌ | ✅ | ✅ |
| Direct Execution | ❌ | ✅ | ✅ |
| Bulk Operations | ❌ | ✅ | ✅ |
| Production Stability | ✅ | ✅ | ❌ |
| Migration Risk | None | Low | High |

### Recommendation

**For Current Project**: Stay on **n8n:1.108.2** until Phase 2/3 completion
- Proven stability with current workflows
- Known workarounds for limitations
- No migration risks during active development

**For Future Projects**: Consider **n8n:1.125.0** or similar
- Better API functionality
- Reduced manual intervention needed
- Maintains compatibility with current approach

### Custom n8n Modification (Advanced Option)

#### **Option 4: Download and Modify n8n Source Code**

For complete control over n8n functionality, you can download the source code and create a custom build with exactly the features you need.

#### **Pros of Custom n8n Build:**
- **Complete Control**: Fix API limitations exactly as needed
- **Custom Features**: Add workflow activation endpoints that work reliably
- **Performance Optimization**: Remove unused features, optimize for your use case
- **Security Hardening**: Implement custom authentication or security measures
- **API Extensions**: Add custom endpoints for bulk operations or advanced features
- **No Version Dependencies**: Not tied to n8n release cycles

#### **Cons of Custom n8n Build:**
- **Development Overhead**: Requires Node.js/TypeScript expertise
- **Maintenance Burden**: Must merge upstream updates manually
- **Testing Complexity**: Need comprehensive testing for custom changes
- **Deployment Complexity**: Custom Docker builds and CI/CD pipelines
- **Support Isolation**: No official support for custom modifications
- **Security Responsibility**: Must monitor and patch security issues independently

#### **Custom Build Process:**

**1. Source Code Setup:**
```bash
# Clone n8n repository
git clone https://github.com/n8n-io/n8n.git
cd n8n
git checkout tags/n8n@1.108.2  # Start from stable version

# Create custom branch
git checkout -b custom-api-fixes
```

**2. Key Files to Modify:**
```bash
# API endpoint definitions
packages/cli/src/api/
├── workflows.api.ts           # Add reliable activation endpoints
├── executions.api.ts          # Add direct execution endpoints
└── auth.middleware.ts         # Enhance API key handling

# Workflow management
packages/cli/src/workflows/
├── workflows.service.ts       # Fix activation/deactivation logic
└── workflow.runner.ts         # Add bulk operations

# Webhook registration
packages/cli/src/webhooks/
└── webhook.service.ts         # Fix immediate registration issues
```

**3. Example Custom API Endpoint:**
```typescript
// packages/cli/src/api/workflows.api.ts
// Add reliable workflow activation endpoint

@Patch('/:id/activate-reliable')
async activateWorkflowReliable(
  @Param('id') workflowId: string,
  @Req() req: WorkflowRequest.Activate,
): Promise<WorkflowActivateResponse> {
  
  // Custom activation logic that actually works
  const workflow = await this.workflowService.get(workflowId);
  
  // Force webhook registration
  await this.webhookService.registerWorkflowWebhooks(workflow);
  
  // Update database with proper transaction
  await this.workflowRepository.update(workflowId, { active: true });
  
  // Verify activation worked
  const activated = await this.workflowService.get(workflowId);
  
  return {
    success: true,
    active: activated.active,
    webhooksRegistered: true,
    message: 'Workflow activated reliably'
  };
}
```

**4. Custom Docker Build:**
```dockerfile
# Dockerfile.custom
FROM node:18-alpine

WORKDIR /app
COPY . .

# Install dependencies and build custom n8n
RUN npm ci --only=production
RUN npm run build

# Custom configuration
ENV N8N_CUSTOM_BUILD=true
ENV N8N_API_ENHANCED=true

EXPOSE 5678
CMD ["npm", "start"]
```

**5. Docker Compose for Custom Build:**
```yaml
# docker-compose.custom.yml
version: '3.8'
services:
  n8n-custom:
    build:
      context: ./n8n-custom
      dockerfile: Dockerfile.custom
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_CUSTOM_API_ENDPOINTS=true
    volumes:
      - n8n_custom_data:/home/node/.n8n
    ports:
      - "5678:5678"
```

#### **Specific Fixes for Current Issues:**

**1. Fix Workflow Activation API:**
```typescript
// Add to workflows.api.ts
@Patch('/:id/force-activate')
async forceActivateWorkflow(@Param('id') id: string) {
  // Force activation with immediate webhook registration
  // No UI dependency, works via API
}
```

**2. Add Bulk Operations:**
```typescript
// Add to workflows.api.ts
@Post('/bulk-activate')
async bulkActivateWorkflows(@Body() workflowIds: string[]) {
  // Activate multiple workflows in one API call
}
```

**3. Fix Webhook Registration:**
```typescript
// Modify webhook.service.ts
async registerWebhookImmediate(workflow: Workflow) {
  // Force immediate registration without delays
  // Add retry logic and verification
}
```

#### **Development Workflow:**

**1. Local Development:**
```bash
# Set up development environment
npm install
npm run dev

# Test custom changes
curl -X PATCH "http://localhost:5678/api/v1/workflows/ID/force-activate"
```

**2. Testing Strategy:**
```bash
# Create test suite for custom endpoints
npm run test:custom-api

# Integration tests with existing workflows
npm run test:integration
```

**3. Deployment:**
```bash
# Build custom Docker image
docker build -f Dockerfile.custom -t n8n-custom:latest .

# Deploy with custom image
docker-compose -f docker-compose.custom.yml up -d
```

#### **Maintenance Strategy:**

**1. Upstream Monitoring:**
- Monitor n8n releases for security patches
- Evaluate new features for potential integration
- Track API changes that might affect custom code

**2. Update Process:**
```bash
# Merge upstream changes
git fetch upstream
git merge upstream/master

# Resolve conflicts in custom code
# Test thoroughly before deployment
```

**3. Documentation:**
- Document all custom changes and reasoning
- Maintain API documentation for custom endpoints
- Keep deployment and build instructions updated

#### **When to Consider Custom Build:**

**✅ Good Fit When:**
- You have Node.js/TypeScript development expertise
- API limitations significantly impact your workflow
- You need specific features not available in any version
- You have resources for ongoing maintenance
- Security/compliance requires custom modifications

**❌ Not Recommended When:**
- Limited development resources
- Standard n8n versions meet most needs
- Rapid deployment is priority
- Maintenance overhead is a concern
- Team lacks Node.js expertise

#### **Risk Assessment:**

| Risk Level | Factor | Mitigation |
|------------|--------|------------|
| **High** | Security vulnerabilities | Regular security audits, upstream monitoring |
| **Medium** | Breaking changes | Comprehensive test suite, staged deployments |
| **Medium** | Maintenance overhead | Dedicated development resources, documentation |
| **Low** | Performance issues | Load testing, monitoring, optimization |

#### **Recommendation for Current Project:**

**Stay with n8n:1.108.2** for now because:
- Current workarounds are functional
- Project is in active development phase
- Custom build adds complexity without immediate necessity

**Consider custom build for future projects** when:
- API limitations become critical bottlenecks
- You have dedicated DevOps resources
- Long-term maintenance is planned and resourced

## 7. Production Deployment

### Security Considerations:
- Use environment variables for API keys
- Enable HTTPS for webhooks
- Add rate limiting
- Implement proper error logging

### Monitoring:
- Set up execution monitoring in n8n
- Monitor API usage limits
- Track success/failure rates
- Monitor HighLevel contact creation
