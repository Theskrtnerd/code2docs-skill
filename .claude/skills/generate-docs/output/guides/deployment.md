---
title: Deployment
slug: deployment
category:
  uri: Documentation
content:
  excerpt: Guide to deploying the AI service to production, including Render configuration, environment setup, PR testing with render-preview label, and Terraform infrastructure management.
---

# Deployment

This guide covers deploying the ReadMe AI service to production, including Render configuration, environment setup, PR testing with the render-preview label, and Terraform infrastructure management.

## Overview

The ReadMe AI service runs as a standalone Node.js application that powers AI features in ReadMe. Deployment involves:

- **Production hosting** on Render with automatic deployments
- **Preview deployments** for pull request testing
- **Infrastructure management** via Terraform for MongoDB Atlas
- **Environment configuration** across development, staging, and production

## Prerequisites

Before deploying, ensure you have:

- Access to the [Render dashboard](https://dashboard.render.com)
- Required API keys (see Environment Variables section)
- MongoDB Atlas connection string
- Terraform Cloud access for infrastructure changes

## Production Deployment

### Render Configuration

The AI service is deployed on Render with the following setup:

**Production Service:**
- URL: `https://readme-ai.onrender.com`
- Auto-deploy: Enabled on `main` branch
- Build command: `npm run build`
- Start command: `npm start`

**Staging Service:**
- URL: `https://readme-ai-stage.onrender.com`
- Auto-deploy: Enabled on `staging` branch

**Next Environment:**
- URL: `https://readme-ai-next.onrender.com`
- Auto-deploy: Enabled on `next` branch

### Deployment Process

Production deployments happen automatically when code is merged to the `main` branch:

1. **Merge to main** → Triggers automatic Render deployment
2. **Build phase** → Runs `npm install` and `npm run build`
3. **Health check** → Render verifies the service starts successfully
4. **Live deployment** → New version goes live automatically

**Manual deployment** can be triggered from the Render dashboard if needed.

### Monitoring Deployments

Monitor deployment status:

1. Navigate to [Render Dashboard](https://dashboard.render.com)
2. Select the `readme-ai` service
3. View deployment logs in real-time
4. Check health status and metrics

**Common deployment issues:**

- **Build failures**: Check build logs for TypeScript errors or missing dependencies
- **Startup failures**: Verify environment variables are set correctly
- **Health check failures**: Ensure the server starts on the correct port

## Environment Variables

### Required Variables

All environments require these API keys:

```bash
# AI Model Access
OPENAI_KEY=sk-...                          # OpenAI API key
GOOGLE_GENERATIVE_AI_API_KEY=...           # Google Gemini API key

# Authentication
AI_TOKEN=...                               # Service authentication token

# Database
AI_MONGO_URI=mongodb+srv://...             # MongoDB Atlas connection string
```

### Environment-Specific Variables

**Production:**
```bash
README_DOMAIN=https://dash.readme.com
AI_SERVER_URL=https://readme-ai.onrender.com
PORT=9563
```

**Staging:**
```bash
README_DOMAIN=https://dash.readmestaging.com
AI_SERVER_URL=https://readme-ai-stage.onrender.com
PORT=9563
```

**Next:**
```bash
README_DOMAIN=https://dash.next.readme.ninja
AI_SERVER_URL=https://readme-ai-next.onrender.com
PORT=9563
```

### Managing Environment Variables

**In Render:**

1. Go to service settings
2. Navigate to "Environment" section
3. Add or update variables
4. Click "Save Changes"
5. Redeploy if necessary

**Environment Groups:**

Render uses environment groups to share variables across services:

- [Production environment group](https://dashboard.render.com/env-group/evg-cusbkv3qf0us73af3dqg)
- [Staging/Next environment group](https://dashboard.render.com/env-group/evg-cusbmf3qf0us73af3pn0)

### Security Best Practices

- **Never commit** API keys or secrets to the repository
- **Rotate keys** regularly, especially after team member departures
- **Use environment groups** to maintain consistency across services
- **Audit access** to Render dashboard and environment variables

## PR Testing with render-preview

### Overview

Pull requests can be tested in isolated preview environments by adding the `render-preview` label. This creates a temporary deployment that mimics production.

### Creating a Preview Deployment

**Step 1: Add the label**

Add the `render-preview` label to your pull request. This triggers an automatic preview deployment.

**Step 2: Wait for deployment**

GitHub Actions will create a preview service on Render. You'll receive a deployment URL in the PR comments:

```
Preview deployment ready:
https://readme-ai-stage-pr-42.onrender.com
```

**Step 3: Test your changes**

Use the preview URL to test your changes in isolation. The preview environment includes:

- All environment variables from staging
- Isolated database (if configured)
- Full AI service functionality

### Linking with ReadMe PR Apps

To test the AI service with a ReadMe PR app:

**Step 1: Get your AI preview URL**

From the PR comment or Render dashboard:
```
https://readme-ai-stage-pr-42.onrender.com
```

**Step 2: Update ReadMe PR configuration**

In your ReadMe PR, update the AI service URL in the configuration to point to your preview deployment.

**Step 3: Test the integration**

Test MCP server, chat, vectorization, and other AI features through the ReadMe PR app.

### Preview Environment Lifecycle

**Creation:**
- Triggered by adding `render-preview` label
- Takes 5-10 minutes to build and deploy
- Uses staging environment variables by default

**Updates:**
- New commits to the PR trigger redeployment
- Preview URL remains the same

**Cleanup:**
- Preview deployments are automatically deleted when the PR is closed or merged
- Manual deletion available from Render dashboard

### Troubleshooting Preview Deployments

**Preview not created:**
- Verify `render-preview` label is applied
- Check GitHub Actions logs for errors
- Ensure Render integration is configured

**Preview deployment fails:**
- Check build logs in Render dashboard
- Verify all required environment variables are set
- Test build locally: `npm run build && npm test`

**Integration issues:**
- Verify AI service URL in ReadMe PR configuration
- Check CORS settings if making cross-origin requests
- Ensure authentication tokens match between services

## Infrastructure Management with Terraform

### Overview

MongoDB Atlas infrastructure is managed using Terraform Cloud. This ensures consistent, version-controlled infrastructure across environments.

### Terraform Workspace

**Workspace:** [ai workspace in Terraform Cloud](https://app.terraform.io/app/readmeio/workspaces/ai)

**Resources managed:**
- MongoDB Atlas clusters
- Database users and access controls
- Network access rules
- Backup policies

### Making Infrastructure Changes

**Step 1: Update Terraform configuration**

Edit files in the `terraform/` directory:

```hcl
# terraform/main.tf
resource "mongodbatlas_cluster" "ai_cluster" {
  project_id = var.project_id
  name       = "ai-production"
  
  # Update cluster configuration
  cluster_type = "REPLICASET"
  # ...
}
```

**Step 2: Plan changes locally**

```bash
cd terraform
terraform init
terraform plan
```

Review the planned changes carefully before applying.

**Step 3: Apply via Terraform Cloud**

1. Commit changes to a feature branch
2. Open a pull request
3. Terraform Cloud runs automatic plan
4. Review plan output in PR comments
5. Merge PR to apply changes

**Step 4: Verify in MongoDB Atlas**

Check the [MongoDB Atlas Dashboard](https://cloud.mongodb.com/v2/663135aaa5431d0ffae8e9bc) to verify changes were applied correctly.

### Common Infrastructure Tasks

**Scaling the cluster:**

Update `cluster_tier` in Terraform configuration:

```hcl
resource "mongodbatlas_cluster" "ai_cluster" {
  # ...
  provider_instance_size_name = "M30"  # Scale up
}
```

**Adding database users:**

```hcl
resource "mongodbatlas_database_user" "new_user" {
  username           = "ai-service"
  password           = var.db_password
  project_id         = var.project_id
  auth_database_name = "admin"
  
  roles {
    role_name     = "readWrite"
    database_name = "ai-production"
  }
}
```

**Updating network access:**

```hcl
resource "mongodbatlas_project_ip_access_list" "render" {
  project_id = var.project_id
  cidr_block = "0.0.0.0/0"  # Update as needed
  comment    = "Render services"
}
```

### Terraform Best Practices

- **Always run plan** before applying changes
- **Review changes** in pull requests before merging
- **Test in staging** before applying to production
- **Document changes** in commit messages
- **Keep secrets** in Terraform Cloud variables, never in code

## Database Setup and Initialization

### MongoDB Atlas Requirements

The AI service requires MongoDB Atlas (not regular MongoDB) for vector search capabilities.

**Required features:**
- Atlas Vector Search
- Minimum cluster tier: M10
- MongoDB version: 6.0 or higher

### Initial Database Setup

**For new MongoDB instances only:**

Initialize the database with required collections and indexes:

```bash
npm run cli:vectorize initdb
```

This creates:
- `readme-ai-vector-collection` (with vector search index)
- `vectorizeQueue` (for background jobs)

**Note:** Only run this once per database. Skip this step if connecting to an existing database.

### Connection String Format

```bash
AI_MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
```

**Example:**
```bash
AI_MONGO_URI=mongodb+srv://ai-service:password123@ai-cluster.mongodb.net/ai-production?retryWrites=true&w=majority
```

### Database Environments

**Production:**
- Managed via Terraform
- Connection string in Render environment variables
- Automatic backups enabled

**Staging:**
- Shared with Next environment
- Connection string in staging environment group

**Local Development:**

Options for local development:

1. **Use staging database** (recommended):
   ```bash
   AI_MONGO_URI=<staging-connection-string>
   ```

2. **Run local MongoDB Atlas container**:
   ```bash
   ./start-mongo.sh
   # Copy connection string from output
   AI_MONGO_URI=mongodb://127.0.0.1:55008
   npm run cli:vectorize initdb
   ```

3. **Skip database** (limited functionality):
   ```bash
   AI_MONGO_URI=""
   # DB operations will fail, but server will start
   ```

## Health Checks and Monitoring

### Service Health

The AI service exposes a health check endpoint:

```bash
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Render uses this endpoint to verify service health during deployments.

### Monitoring Deployment Health

**Check service status:**

```bash
# Production
curl https://readme-ai.onrender.com/health

# Staging
curl https://readme-ai-stage.onrender.com/health

# Preview
curl https://readme-ai-stage-pr-42.onrender.com/health
```

**Expected response time:** < 500ms

### Logs and Debugging

**Access logs in Render:**

1. Navigate to service in Render dashboard
2. Click "Logs" tab
3. Filter by log level (info, warn, error)
4. Search for specific errors or requests

**Common log patterns:**

```bash
# Successful startup
Server listening on port 9563

# Database connection
MongoDB connected successfully

# API requests
POST /chat/agentChat - 200 OK - 1234ms
```

## Rollback Procedures

### Rolling Back a Deployment

If a deployment causes issues, rollback to the previous version:

**Via Render Dashboard:**

1. Go to service in Render dashboard
2. Click "Rollback" button
3. Select previous deployment
4. Confirm rollback

**Via Git:**

```bash
# Revert the problematic commit
git revert <commit-hash>

# Push to trigger new deployment
git push origin main
```

### Emergency Procedures

**Service completely down:**

1. Check Render service status
2. Review recent deployment logs
3. Rollback to last known good deployment
4. Notify team in Slack

**Database connectivity issues:**

1. Verify MongoDB Atlas cluster status
2. Check network access rules in Atlas
3. Verify connection string in environment variables
4. Test connection manually

**API key issues:**

1. Verify API keys are set in environment variables
2. Check key validity with providers (OpenAI, Google)
3. Rotate keys if compromised
4. Update environment variables and redeploy

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing locally (`npm test`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] PR approved and merged
- [ ] Environment variables verified

### During Deployment

- [ ] Monitor deployment logs in Render
- [ ] Verify health check passes
- [ ] Check service starts successfully
- [ ] No errors in startup logs

### Post-Deployment

- [ ] Test health endpoint
- [ ] Verify MCP server connectivity
- [ ] Test chat functionality
- [ ] Check metrics and monitoring
- [ ] Notify team of successful deployment

## Troubleshooting Common Issues

### Build Failures

**Symptom:** Deployment fails during build phase

**Solutions:**
- Check build logs for TypeScript errors
- Verify all dependencies in `package.json`
- Test build locally: `npm run build`
- Clear Render build cache and retry

### Environment Variable Issues

**Symptom:** Service starts but features don't work

**Solutions:**
- Verify all required variables are set
- Check for typos in variable names
- Ensure values are properly formatted
- Test with dummy values locally first

### Database Connection Failures

**Symptom:** Service crashes on startup with MongoDB errors

**Solutions:**
- Verify MongoDB Atlas cluster is running
- Check connection string format
- Verify network access rules in Atlas
- Test connection string locally

### Performance Issues

**Symptom:** Slow response times or timeouts

**Solutions:**
- Check MongoDB Atlas cluster performance metrics
- Review API rate limits (OpenAI, Google)
- Monitor Render service metrics
- Consider scaling cluster tier in Terraform

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com)
- [Terraform Cloud Documentation](https://www.terraform.io/cloud-docs)
- [ReadMe AI Service README](../README.md)
- [Environment Configuration Guide](../config/README.md)
