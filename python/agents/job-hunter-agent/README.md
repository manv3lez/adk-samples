# 🎯 Job Hunter Agent
ADK version: 1.14.1 | Owner: [@manv3lez](https://github.com/manv3lez)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK%201.14.1-4285F4?logo=google)](https://github.com/google/adk-samples)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

> **A comprehensive multi-agent AI system that guides you through every stage of your job search journey** — from career analysis and job discovery to interview preparation and long-term career strategy.

Built on the Google Agent Development Kit (ADK), this system orchestrates 5 specialized AI agents working together to provide personalized, actionable job hunting assistance.

## ✨ Key Features

- 🎓 **Career Profile Analysis** - Deep analysis of your skills, experience, and career goals
- 🔍 **Smart Job Discovery** - Google Search integration to find relevant opportunities
- 📝 **ATS-Optimized Applications** - Generate tailored resumes and cover letters that pass Applicant Tracking Systems
- 🎤 **Interview Preparation** - Company research, practice questions, and STAR method examples
- 🚀 **Career Strategy Planning** - Long-term career roadmaps with skills gap analysis and industry trends
- 💾 **State Management** - Track multiple job applications simultaneously
- 🧪 **Comprehensive Testing** - Full test suite with unit, property-based, and integration tests

## 🤖 The Agent Team

The system uses a **coordinator pattern** where a Career Coordinator orchestrates 5 specialized sub-agents:

| Agent | Role | Key Capabilities |
|-------|------|------------------|
| 🎓 **Career Profile Analyst** | Analyzes your background | Skills extraction, experience analysis, strengths/gaps identification |
| 🔍 **Job Market Researcher** | Finds opportunities | Google Search integration, company research, salary data |
| 📝 **Application Strategist** | Creates applications | ATS optimization, keyword matching, tailored resumes & cover letters |
| 🎤 **Interview Coach** | Prepares you for interviews | Company culture research, behavioral/technical questions, STAR examples |
| 🚀 **Career Strategy Advisor** | Plans your career path | Career trajectory analysis, skills roadmap, industry trend forecasting |

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/google/adk-samples.git
cd adk-samples/python/agents/job-hunter-agent

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your Google Cloud Project details

# Authenticate with Google Cloud
gcloud auth application-default login

# Run the agent (Web UI)
uv run adk web
# Open http://localhost:8000 in your browser
```

## 🏗️ Architecture

### Phase 2 Architecture (Current)

Phase 2 introduces flexible, conversational routing with persistent sessions:

```
┌─────────────────────────────────────────────────────────────┐
│              Managing Coordinator (Gemini 3 Pro)             │
│                  Flexible LLM-Based Routing                  │
│                                                              │
│  • Analyzes user questions with natural language             │
│  • Routes to 1-3 relevant specialists dynamically            │
│  • Synthesizes responses from multiple specialists           │
│  • Maintains conversation context across sessions            │
└──────────────────┬───────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐    ┌────────────────────────┐
│ Specialist    │    │  Infrastructure        │
│ Agents        │    │                        │
│ (Gemini 3 Pro)│    │  • PostgreSQL Database │
│               │    │  • User Authentication │
│ 1. Career     │    │  • Session Management  │
│    Profile    │    │  • Conversation History│
│    Analyst ✅ │    │  • Cached Analyses     │
│               │    │  • Google Search       │
│ 2. Job Market │    │  • ATS Analyzer        │
│    Researcher ✅│   └────────────────────────┘
│               │
│ 3. Application│
│    Strategist │
│               │
│ 4. Interview  │
│    Preparation│
│               │
│ 5. Strategic  │
│    Career     │
│    Advisor    │
└───────────────┘

✅ = Upgraded to Gemini 3 Pro
```

### Phase 1 Architecture (Legacy)

Phase 1 used a rigid pipeline approach (still available for backward compatibility):

```
┌─────────────────────────────────────────────────────────────┐
│                    Career Coordinator                        │
│                  (Pipeline Orchestrator)                     │
│                                                              │
│  - Enforces sequential workflow stages                       │
│  - Routes based on current stage                             │
│  - Maintains in-memory state                                 │
│  - Provides workflow guidance                                │
└──────────────────┬───────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐    ┌────────────────────┐
│ Sub-Agent     │    │ Sub-Agent Tools    │
│ Layer         │    │                    │
│               │    │ - Google Search    │
│ 1. Career     │    │ - ATS Analyzer     │
│    Profile    │    │                    │
│    Analyst    │    └────────────────────┘
│               │
│ 2. Job Market │
│    Researcher │
│               │
│ 3. Application│
│    Strategist │
│               │
│ 4. Interview  │
│    Coach      │
│               │
│ 5. Career     │
│    Strategy   │
│    Advisor    │
└───────────────┘
```

### Key Architectural Differences

| Aspect | Phase 1 (Legacy) | Phase 2 (Current) |
|--------|------------------|-------------------|
| **Routing** | Sequential pipeline | Flexible LLM-based |
| **Intent Detection** | Keyword matching | Natural language understanding |
| **Conversation** | Step-by-step form | Natural conversation |
| **State** | In-memory only | PostgreSQL database |
| **Sessions** | Single session | Persistent across logins |
| **Model** | Gemini 2.5 Pro | Gemini 3 Pro |
| **Authentication** | None | bcrypt + sessions |
| **Specialists** | Called in order | Called as needed |

## 💬 Example Interaction

```
You: I need help finding a software engineering job

Career Coordinator: Hello! I'm your Career Coordinator. I'll guide you through:
1. 📋 Career Profile Analysis
2. 🔍 Job Market Research  
3. 📝 Application Materials
4. 🎤 Interview Preparation
5. 🚀 Career Strategy

Let's start by analyzing your career profile...

[After providing your background]

Career Coordinator: ✅ Profile Analysis Complete!

Top Strengths: Cloud Architecture (AWS, GCP), Python (5 years), Team Leadership
Skills Gaps: Kubernetes, System Design at Scale
Recommendations: CKA certification, System design portfolio project

Ready to search for jobs? 🔍
```

## 🎯 Use Cases

- **Job Seekers**: Get personalized guidance through your entire job search
- **Career Changers**: Identify transferable skills and create transition strategies  
- **Interview Prep**: Practice with role-specific questions and company research
- **Career Planning**: Map out long-term career trajectories with actionable roadmaps

## 🛠️ Technical Highlights

- **Comprehensive Career Analysis**: Extracts and categorizes skills, analyzes experience, identifies strengths and gaps
- **ATS Optimization**: Creates application materials optimized for Applicant Tracking Systems with keyword matching
- **Job Market Research**: Uses Google Search to find relevant opportunities across multiple job boards
- **Interview Preparation** ✨: Company culture research, behavioral and technical questions, STAR method examples, study recommendations
- **Career Strategy Planning** ✨: Long-term career path analysis, skills gap identification, industry trend forecasting, development roadmaps
- **User-Friendly Interaction**: Clear workflow explanations, sub-agent activity notifications, and helpful guidance
- **State Management**: Maintains context across the job hunting journey with isolated state for multiple applications
- **Error Handling**: Provides user-friendly error messages with suggested next steps
- **Markdown Formatting**: Formats results as markdown for better readability

### Key Capabilities

- **ATS Keyword Analysis**: Extracts required, preferred, and technical keywords from job descriptions
- **Match Score Calculation**: Calculates keyword match percentage between resume and job description
- **Skills Gap Identification**: Identifies missing skills and provides development recommendations
- **Company Research**: Gathers information about company culture, recent news, and employee reviews
- **Interview Question Generation**: Creates role-specific behavioral and technical questions organized by difficulty
- **STAR Method Examples**: Generates personalized example responses based on user's actual career experience
- **Career Path Mapping**: Analyzes multiple potential career trajectories with progression steps and timeframes
- **Industry Trend Analysis**: Forecasts emerging skills, technologies, and market opportunities
- **Multi-Application Support**: Maintains separate state for concurrent job applications

## Setup

### Prerequisites

- **Python**: 3.10, 3.11, or 3.12
- **Google Cloud Project**: With Vertex AI API enabled
- **Google ADK**: Installed via uv
- **uv package manager**: [Installation instructions](https://docs.astral.sh/uv/getting-started/installation/)
- **gcloud CLI**: For authentication

### Installation

1. **Clone the repository** (if not already done):
```bash
cd python/agents/job-hunter-agent
```

2. **Install dependencies**:

**Option A: Using uv (Recommended)**
```bash
uv sync
```

**If you get "uv is not recognized" but have uv installed:**
```bash
# On Windows, if uv is not in PATH, use:
python -m uv sync
```

**Option B: Using pip (Alternative if uv is not available)**
```bash
python -m pip install google-adk google-genai google-cloud-aiplatform pydantic python-dotenv hypothesis pytest pytest-asyncio nest-asyncio
```

This will install all required dependencies including:
- google-adk
- google-cloud-aiplatform
- hypothesis (for property-based testing)
- pytest (for testing)

> **Note for Windows users:** If `uv` command is not recognized even though you have it installed, it's likely not in your PATH. You can either:
> - Use `python -m uv` instead of `uv` for all commands
> - Add uv to your PATH (typically `%USERPROFILE%\.local\bin` or `%APPDATA%\Python\Scripts`)
> - Use the pip installation method (Option B)

3. **Configure environment variables**:
```bash
cp .env.example .env
```

Edit `.env` with your Google Cloud Project details:
```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name  # Only for deployment

# Optional: For enhanced job search capabilities
GOOGLE_SEARCH_API_KEY=your-search-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id
```

4. **Authenticate with Google Cloud**:
```bash
gcloud auth application-default login
```

5. **Set up PostgreSQL database (Phase 2 - Optional)**:

If you want to use Phase 2 features (persistent sessions, authentication):

```bash
# Install PostgreSQL (if not already installed)
# On macOS: brew install postgresql
# On Ubuntu: sudo apt-get install postgresql
# On Windows: Download from postgresql.org

# Create database
createdb job_hunter_agent

# Run migrations
python -m job_hunter_agent.database.migrations
```

See [Database Quick Start](job_hunter_agent/database/QUICK_START.md) for detailed setup instructions.

6. **Verify installation**:
```bash
uv run pytest tests/test_project_structure.py
```

### Running the Agent

#### Option 1: ADK CLI (Recommended for testing)

**With uv:**
```bash
uv run adk run job_hunter_agent
```

**If uv is not in PATH:**
```bash
python -m uv run adk run job_hunter_agent
```

**With pip:**
```bash
python -m google.adk.cli run job_hunter_agent
```

This starts an interactive session in your terminal.

#### Option 2: ADK Web UI (Recommended for development)

**With uv:**
```bash
uv run adk web
```

**If uv is not in PATH:**
```bash
python -m uv run adk web
```

**With pip:**
```bash
python -m google.adk.cli web
```

This opens a web interface at `http://localhost:8000` (or `http://127.0.0.1:8000`) where you can interact with the agent.

#### Option 3: Python Script

**Phase 2 (Flexible Routing - Recommended):**
```python
from job_hunter_agent import root_agent

# root_agent is now the Managing Coordinator (Phase 2)
# Ask any question - no forced pipeline!
response = root_agent.run("What jobs should I apply to?")
print(response)

# Or with context
from job_hunter_agent.managing_coordinator import build_coordinator_context

context = build_coordinator_context(
    conversation_history=[
        {"role": "user", "content": "I'm a software engineer"},
    ],
    user_profile={
        "background": "5 years experience",
        "career_goals": "Senior role",
    },
)
response = root_agent.run("Help with my resume", context=context)
```

**Phase 1 (Pipeline - Legacy):**
```python
from job_hunter_agent.agent import career_coordinator

# Use Phase 1 coordinator if you need the sequential pipeline
response = career_coordinator.run("Help me find a software engineering job")
print(response)
```

#### Option 4: With Database & Authentication (Phase 2)

```python
from job_hunter_agent.auth import AuthManager
from job_hunter_agent.database import get_connection
from job_hunter_agent import root_agent

# Initialize database connection
conn = get_connection()

# Create auth manager
auth_manager = AuthManager(conn)

# Register user
user_id = auth_manager.register("user@example.com", "secure_password")

# Login
session_token = auth_manager.login("user@example.com", "secure_password")

# Load user context
user_context = auth_manager.load_user_context(session_token)

# Use agent with user context
response = root_agent.run(
    "What jobs should I apply to?",
    context=user_context
)
```

## State Management

The Job Hunter Agent uses a state management system to maintain data flow between sub-agents. Each sub-agent stores its output in a designated state key.

For complete details, see **[State Keys Reference](STATE_KEYS.md)**.

### State Keys Overview

| State Key | Producer | Consumers | Description |
|-----------|----------|-----------|-------------|
| `career_profile_output` | Career Profile Analyst | All other sub-agents | Comprehensive career profile including skills, experience, strengths, gaps, and recommendations |
| `job_opportunities_output` | Job Market Researcher | Application Strategist, Interview Coach | Curated list of job opportunities with match scores and company information |
| `application_materials_output` | Application Strategist | User | Tailored resume, cover letter, and ATS analysis |
| `interview_prep_output` ✨ | Interview Coach | User | Interview preparation guide with questions, STAR examples, and study topics |
| `career_strategy_output` ✨ | Career Strategy Advisor | User | Strategic career plan with paths, roadmap, and industry trends |
| `career_coordinator_output` | Career Coordinator | User | Workflow guidance and coordination messages |

### Using State Management

#### Basic Usage (Automatic)

State keys are automatically managed by the ADK framework. Sub-agents store their output using the `output_key` parameter:

```python
career_profile_analyst = LlmAgent(
    name="career_profile_analyst",
    output_key="career_profile_output",  # Automatically stored
    # ...
)
```

#### Advanced Usage (Manual)

For advanced features like multi-application isolation:

```python
from job_hunter_agent.state_manager import get_state_manager

# Get the state manager instance
state_manager = get_state_manager()

# Store state for a specific application
state_manager.store_state(
    key="career_profile_output",
    value=profile_data,
    application_id="app_123"
)

# Retrieve state for a specific application
profile = state_manager.retrieve_state(
    key="career_profile_output",
    application_id="app_123"
)

# List all applications
applications = state_manager.list_applications()
```

See **[State Keys Reference](STATE_KEYS.md)** for complete documentation and `job_hunter_agent/state_integration_example.py` for usage examples.

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run Specific Test Categories

**Unit tests only**:
```bash
uv run pytest tests/ -k "not property"
```

**Property-based tests only**:
```bash
uv run pytest tests/ -k property
```

**Specific test file**:
```bash
uv run pytest tests/test_ats_analyzer.py -v
```

**Integration tests**:
```bash
uv run pytest tests/test_mvp_integration.py -v
```

### Test Coverage

The test suite includes:
- **Unit tests**: Test individual components and functions
- **Property-based tests**: Test universal properties using Hypothesis (100+ iterations per property)
- **Integration tests**: Test complete workflows across multiple sub-agents

## Documentation

### User Guides
- **[README](README.md)** (this file) - Overview, setup, and usage
- **[User Interaction Features](USER_INTERACTION_FEATURES.md)** - Details on workflow explanations, notifications, and help system
- **[Example Interactions](#example-interactions)** - See below for detailed examples

### Technical Documentation
- **[Architecture](ARCHITECTURE.md)** - System architecture, diagrams, and component details
- **[Deployment Guide](DEPLOYMENT.md)** - Detailed deployment instructions for all environments
- **[State Keys Reference](STATE_KEYS.md)** - Complete reference for all state keys and data structures
- **[Project Structure](STRUCTURE.md)** - Directory structure and module organization

### Specification Documents
- **[Design Document](.kiro/specs/job-hunter-agent/design.md)** - Complete system design and correctness properties
- **[Requirements](.kiro/specs/job-hunter-agent/requirements.md)** - Detailed requirements and acceptance criteria
- **[Tasks](.kiro/specs/job-hunter-agent/tasks.md)** - Implementation task list and progress

## Example Interactions

### Example 1: Complete Job Application Workflow

```
User: I need help finding a software engineering job

Career Coordinator: Hello! I'm your Career Coordinator, here to guide you through 
your job hunting journey. I'll help you through these stages:

1. 📋 Career Profile Analysis - Understanding your background and goals
2. 🔍 Job Market Research - Finding relevant opportunities
3. 📝 Application Materials - Creating tailored resumes and cover letters
4. 🎯 Interview Preparation - Preparing for interviews (coming soon)

Let's start by analyzing your career profile. Please share:
- Your work history and experience
- Your technical and soft skills
- Your career goals and preferences
- Your target roles and industries

---

User: I have 5 years of experience as a Python developer, worked on cloud 
infrastructure with AWS and GCP, led a team of 3 developers, and I'm looking 
for senior engineering roles in fintech companies.

Career Coordinator: 🔄 Activating Career Profile Analyst...

[Processing...]

Career Coordinator: ✅ Completed: Career Profile Analysis

Great news! I've analyzed your background and identified:

**Top Strengths:**
- Cloud Architecture (AWS, GCP)
- Python Development (5 years)
- Team Leadership (3 direct reports)
- Infrastructure Engineering

**Skills Gaps for Senior Roles:**
- Kubernetes/container orchestration
- CI/CD pipeline design
- System design at scale

**Recommendations:**
1. Obtain Kubernetes certification (CKA)
2. Build portfolio project demonstrating system design
3. Highlight leadership experience in applications

Would you like me to search for relevant job opportunities now?

---

User: Yes, please search for jobs in San Francisco

Career Coordinator: 🔄 Activating Job Market Researcher...

[Searching job boards and company sites...]

Career Coordinator: ✅ Completed: Job Market Research

I found 12 relevant opportunities! Here are the top 3 matches:

**1. Senior Software Engineer - Stripe (Match: 92%)**
- Location: San Francisco, CA
- Salary: $180K-$250K
- Key Requirements: Python, Cloud Infrastructure, Team Leadership
- Company Culture: Engineering-driven, high autonomy
- [View Job](https://stripe.com/jobs/...)

**2. Staff Engineer - Plaid (Match: 88%)**
- Location: San Francisco, CA (Hybrid)
- Salary: $200K-$280K
- Key Requirements: Python, AWS, Distributed Systems
- Company Culture: Collaborative, fintech focus
- [View Job](https://plaid.com/careers/...)

**3. Senior Backend Engineer - Robinhood (Match: 85%)**
- Location: San Francisco, CA
- Salary: $170K-$240K
- Key Requirements: Python, Microservices, Leadership
- Company Culture: Fast-paced, mission-driven
- [View Job](https://robinhood.com/careers/...)

Which position would you like to apply to?

---

User: I'd like to apply to the Stripe position

Career Coordinator: 🔄 Activating Application Strategist...

[Analyzing job requirements and optimizing application materials...]

Career Coordinator: ✅ Completed: Application Materials

I've created tailored application materials for the Stripe Senior Software 
Engineer position!

**ATS Match Score: 94%** ✅

**Resume Highlights:**
- Optimized for ATS with all required keywords
- Emphasized cloud infrastructure experience
- Highlighted team leadership achievements
- Quantified impact (e.g., "Reduced deployment time by 60%")

**Cover Letter:**
- Tailored to Stripe's engineering culture
- Connected your experience to their requirements
- Demonstrated knowledge of their products

**Missing Keywords (Recommendations):**
- "Kubernetes" - Consider adding if you have experience
- "GraphQL" - Mention if you've worked with it

Would you like me to show you the full resume and cover letter in markdown format?
```

### Example 2: ATS Optimization

```
User: Can you analyze this job description and tell me how well my resume matches?

[User provides job description]

Career Coordinator: 🔄 Activating Application Strategist for ATS analysis...

Career Coordinator: ✅ ATS Analysis Complete

**Match Score: 76%** ⚠️

**Found Keywords (18/24):**
✅ Python, AWS, Docker, REST APIs, Microservices, Git, CI/CD, Agile, 
   Team Leadership, Code Review, Testing, PostgreSQL, Redis, Linux,
   Problem Solving, Communication, Collaboration, Bachelor's Degree

**Missing Keywords (6/24):**
❌ Kubernetes, Terraform, GraphQL, Monitoring (Datadog/Prometheus), 
   Service Mesh, gRPC

**Recommendations:**
1. Add "Kubernetes" if you have container orchestration experience
2. Include "Terraform" or "Infrastructure as Code" if applicable
3. Mention "GraphQL" if you've worked with it
4. Add monitoring tools you've used (even if not Datadog/Prometheus)
5. Include "gRPC" if you've built RPC services

**Optimization Tips:**
- Use exact keyword phrases from the job description
- Place keywords in context (don't just list them)
- Include keywords in your summary, experience, and skills sections

Would you like me to generate an optimized resume incorporating these keywords?
```

### Example 3: Skills Gap Analysis

```
User: What skills do I need to develop to become a senior engineer?

Career Coordinator: Based on your career profile analysis, here are the key 
skills gaps for senior engineering roles:

**Technical Skills:**
1. **System Design** - Design scalable distributed systems
   - Recommendation: Study "Designing Data-Intensive Applications"
   - Practice: Design systems on paper, review architecture docs

2. **Kubernetes** - Container orchestration at scale
   - Recommendation: Complete CKA certification
   - Practice: Deploy personal projects on K8s

3. **Observability** - Monitoring, logging, tracing
   - Recommendation: Learn Prometheus, Grafana, Jaeger
   - Practice: Add observability to existing projects

**Leadership Skills:**
1. **Technical Mentorship** - Guide junior engineers
   - Recommendation: Volunteer to mentor at your current company
   - Practice: Write technical documentation and guides

2. **Cross-Team Collaboration** - Work across organizational boundaries
   - Recommendation: Participate in architecture review meetings
   - Practice: Lead a cross-team initiative

**Timeline:** 6-12 months to develop these skills to senior level

Would you like me to create a detailed development roadmap?
```

### Example 4: Interview Preparation ✨

```
User: I have an interview with Stripe next week for the Senior Software Engineer 
position. Can you help me prepare?

Career Coordinator: 🔄 Activating Interview Preparation Coach...

[Researching Stripe's culture and interview process...]

Career Coordinator: ✅ Completed: Interview Preparation

Excellent! I've created a comprehensive interview preparation guide for your 
Stripe Senior Software Engineer interview.

**Company Research:**
- Engineering-driven culture with high autonomy
- Strong focus on API design and developer experience
- Recent expansion into embedded finance and crypto
- Known for rigorous technical interviews with emphasis on system design

**Interview Preparation Overview:**
- Estimated prep time: 15-20 hours
- Focus areas: System design, API design, distributed systems, behavioral leadership

**Behavioral Questions (15 questions organized by competency):**

*Leadership & Teamwork:*
1. "Tell me about a time you had to influence a team decision without formal authority"
   - Difficulty: Advanced
   - Tip: Stripe values collaborative decision-making

2. "Describe a situation where you had to balance technical debt with feature delivery"
   - Difficulty: Intermediate
   - Tip: Show pragmatic thinking and business awareness

**Technical Questions (12 questions organized by difficulty):**

*System Design (Advanced):*
1. "Design a rate limiting system for Stripe's API that handles millions of requests per second"
   - Key concepts: Token bucket, distributed rate limiting, Redis
   - Hint: Consider multi-region deployment and consistency requirements

2. "How would you design a payment reconciliation system?"
   - Key concepts: Idempotency, eventual consistency, audit trails
   - Hint: Think about handling failures and ensuring financial accuracy

**STAR Method Examples (Based on Your Experience):**

*Example 1: Technical Leadership*
- Situation: Led cloud migration project at previous company
- Task: Migrate 50+ microservices from AWS to GCP with zero downtime
- Action: Created phased migration plan, established monitoring, trained team
- Result: Completed migration 2 weeks ahead of schedule, reduced costs by 30%
- Applicable to: Leadership questions, technical decision-making

*Example 2: Problem Solving*
- Situation: Production incident affecting payment processing
- Task: Identify root cause and implement fix within SLA
- Action: Used distributed tracing to isolate issue, implemented circuit breaker
- Result: Reduced incident from 45min to 12min, prevented $200K in lost revenue
- Applicable to: Problem-solving, system reliability questions

**Study Topics (Prioritized):**

*Critical (Study First):*
1. **Distributed Systems Fundamentals**
   - Why: Core to Stripe's infrastructure
   - Resources: 
     * "Designing Data-Intensive Applications" (Chapters 5-9)
     * MIT 6.824 Distributed Systems lectures
   - Time: 8-10 hours
   - Key concepts: Consistency, replication, partitioning

2. **API Design Best Practices**
   - Why: Central to Stripe's product
   - Resources:
     * Stripe API documentation (study their design patterns)
     * "REST API Design Rulebook"
   - Time: 4-6 hours
   - Key concepts: Versioning, idempotency, pagination

**Interview Tips:**

*General:*
- Structure system design answers: Requirements → High-level → Deep dive → Trade-offs
- Ask clarifying questions before diving into solutions
- Think out loud to show your reasoning process

*Stripe-Specific:*
- Emphasize API design and developer experience in your answers
- Show awareness of financial systems requirements (accuracy, auditability)
- Demonstrate understanding of Stripe's products and mission

**Questions to Ask the Interviewer:**
1. "How does Stripe approach technical debt management at scale?"
2. "What's the team's approach to API versioning and backwards compatibility?"
3. "How do you balance innovation with the reliability requirements of financial infrastructure?"

**Preparation Checklist:**
- [ ] Review all STAR examples and practice delivering them (2 hours)
- [ ] Study distributed systems fundamentals (8 hours)
- [ ] Practice 3-4 system design problems (6 hours)
- [ ] Research Stripe's recent product launches and engineering blog (2 hours)
- [ ] Prepare questions for the interviewer (1 hour)
- [ ] Mock interview with a friend or mentor (2 hours)

Good luck with your interview! Remember to be yourself and let your experience shine through.

Would you like me to dive deeper into any specific area?
```

### Example 5: Career Strategy Planning ✨

```
User: I want to become a Principal Engineer in the next 5 years. What's my path?

Career Coordinator: 🔄 Activating Career Strategy Advisor...

[Analyzing career paths and industry trends...]

Career Coordinator: ✅ Completed: Strategic Career Plan

Great ambition! I've created a comprehensive 5-year strategic plan to help you 
reach Principal Engineer level.

**Executive Summary:**
- Current Position: Senior Software Engineer with 5 years experience
- Strategic Vision: Principal Engineer (Staff → Senior Staff → Principal)
- Timeline: 4-6 years with focused development
- Key Opportunity: Growing demand for distributed systems expertise
- Primary Challenge: Developing organizational influence and technical leadership

**Career Path Analysis:**

I've identified two viable paths to Principal Engineer:

**Path 1: Technical Leadership Track (Recommended)**
- Viability: High (aligns with your background)
- Progression: Senior → Staff → Senior Staff → Principal
- Timeline: 4-6 years

*Progression Steps:*
1. **Staff Engineer** (2-3 years)
   - Requirements: Lead major technical initiatives, mentor senior engineers
   - Responsibilities: Architecture decisions, cross-team technical leadership
   - Typical scope: Team-level impact (10-20 engineers)

2. **Senior Staff Engineer** (2-3 years)
   - Requirements: Drive org-level technical strategy, establish best practices
   - Responsibilities: Multi-team architecture, technical vision
   - Typical scope: Organization-level impact (50-100 engineers)

3. **Principal Engineer** (Ongoing)
   - Requirements: Company-wide technical influence, industry recognition
   - Responsibilities: Company technical strategy, external thought leadership
   - Typical scope: Company-level impact (100+ engineers)

*Pros:*
- Leverages your strong technical foundation
- Clear progression path in most tech companies
- Maintains hands-on technical work

*Cons:*
- Requires developing influence skills beyond pure technical expertise
- Competitive at higher levels
- May require company changes for advancement

**Path 2: Domain Specialist Track**
- Viability: Medium (requires deeper specialization)
- Focus: Become recognized expert in specific domain (e.g., distributed systems, ML infrastructure)
- Timeline: 5-7 years
- Better for: Those who want to go very deep in one area

**Long-Term Skills Gaps:**

*Foundation Skills (Develop in Year 1-2):*
1. **System Design at Scale**
   - Current: Intermediate | Target: Expert
   - Importance: Core requirement for Staff+ roles
   - Development: 12-18 months of focused practice
   - Priority: HIGH

2. **Technical Writing & Communication**
   - Current: Intermediate | Target: Advanced
   - Importance: Essential for organizational influence
   - Development: 6-12 months of consistent practice
   - Priority: HIGH

*Progressive Skills (Develop in Year 2-4):*
1. **Organizational Influence**
   - Current: Beginner | Target: Advanced
   - Importance: Critical for Senior Staff+ roles
   - Development: 18-24 months of active practice
   - Priority: HIGH

2. **Technical Strategy & Vision**
   - Current: Beginner | Target: Advanced
   - Importance: Defines Principal-level work
   - Development: 24-36 months
   - Priority: MEDIUM

**Industry Trends:**

*Emerging Trends:*
1. **AI/ML Infrastructure**
   - Impact: High demand for engineers who can build scalable ML systems
   - Timeline: Already mature, growing rapidly
   - Action: Gain experience with ML infrastructure, LLM deployment

2. **Platform Engineering**
   - Impact: Companies investing heavily in internal developer platforms
   - Timeline: Next 2-3 years
   - Action: Learn platform engineering patterns, developer experience design

*Growing Skills:*
- Distributed systems (High growth, High relevance) ✅ Invest heavily
- Kubernetes/Cloud Native (High growth, High relevance) ✅ Invest
- AI/ML Infrastructure (Very high growth, Medium relevance) ✅ Consider

*Market Outlook:*
- Overall Health: Strong
- Job Growth: 15-20% growth for Staff+ roles over next 5 years
- Salary Trends: Principal Engineers: $300K-$500K+ total comp at top companies
- Stability: High demand for experienced technical leaders

**5-Year Development Roadmap:**

**Phase 1: Foundation Building (Year 1)**
*Objectives:*
- Establish Staff Engineer credibility
- Develop system design expertise
- Build technical writing habit

*Skills to Develop:*
- System Design: Study 2 hours/week, practice 1 design/week
- Technical Writing: Write 1 technical doc/month, start blog
- Distributed Systems: Complete MIT 6.824 course

*Certifications:*
- AWS Solutions Architect Professional (demonstrates cloud expertise)
- Cost: $300 | Time: 40-60 hours

*Experience Goals:*
- Lead a major technical initiative (e.g., system redesign, migration)
- Mentor 2-3 senior engineers
- Present at internal tech talks (monthly)

*Milestones:*
- Q2: Complete first major technical design doc
- Q4: Lead project affecting 3+ teams

**Phase 2: Staff Engineer Transition (Year 2-3)**
*Objectives:*
- Achieve Staff Engineer promotion
- Expand influence across organization
- Develop technical strategy skills

*Skills to Develop:*
- Organizational Influence: Lead cross-team initiatives
- Technical Strategy: Participate in architecture reviews
- Public Speaking: Present at external conferences

*Experience Goals:*
- Drive architecture decisions for 2-3 teams
- Establish technical standards or best practices
- Contribute to open source (build industry reputation)

*Milestones:*
- Year 2 Q2: Staff Engineer promotion
- Year 3 Q1: First external conference talk

**Phase 3: Senior Staff Preparation (Year 4-5)**
*Objectives:*
- Build company-wide technical influence
- Develop technical vision capabilities
- Establish industry presence

*Skills to Develop:*
- Technical Vision: Define multi-year technical roadmaps
- Executive Communication: Present to leadership
- Industry Thought Leadership: Write, speak, contribute

*Experience Goals:*
- Drive technical strategy for entire organization
- Mentor Staff engineers
- Build industry reputation (blog, talks, open source)

*Milestones:*
- Year 4 Q4: Senior Staff Engineer promotion
- Year 5 Q2: Recognized industry expert in your domain

**Success Metrics:**

1. **Technical Impact**
   - Target: Lead initiatives affecting 50+ engineers by Year 3
   - Measure: Track scope of projects and teams impacted

2. **Organizational Influence**
   - Target: Architecture decisions adopted by 5+ teams by Year 4
   - Measure: Count teams using your designs/standards

3. **Industry Recognition**
   - Target: 3+ conference talks, 20+ technical blog posts by Year 5
   - Measure: Speaking engagements, blog traffic, social media following

4. **Mentorship Impact**
   - Target: Mentor 10+ engineers to senior+ levels by Year 5
   - Measure: Track mentee promotions and growth

**Resources:**

*Learning Platforms:*
- educative.io: System design courses (Subscription: $20/month)
- StaffEng.com: Staff+ career guidance (Free)

*Professional Organizations:*
- ACM: Access to research and networking ($99/year)

*Networking:*
- Attend QCon, Strange Loop, or similar conferences annually
- Join local tech meetups in your specialization
- Participate in online communities (Reddit r/ExperiencedDevs, Blind)

**Contingency Plans:**

*Scenario: Market Downturn*
- Focus on cost-saving initiatives and efficiency improvements
- Build skills that are recession-proof (infrastructure, reliability)
- Consider consulting or fractional work to maintain income

*Scenario: Company Lacks Growth Opportunities*
- Target companies with established Staff+ career ladders (FAANG, unicorns)
- Build external reputation to attract opportunities
- Consider strategic company change at Staff level

---

**Important Disclaimer:**
This strategic plan is AI-generated guidance based on your career profile and 
general industry trends. Please:
- Validate recommendations with experienced Principal Engineers in your network
- Adjust timeline based on your personal circumstances and company opportunities
- Research specific opportunities in your target companies
- Consider working with a human career coach for personalized guidance

This is a roadmap, not a rigid plan. Stay flexible and adapt as opportunities arise!

Would you like me to dive deeper into any specific phase or skill area?
```

## Deployment

### MVP Deployment (Local/Development)

The MVP is designed to run locally or in development environments. For production deployment, see Phase 2 deployment instructions.

#### Prerequisites

- Google Cloud Project with Vertex AI API enabled
- Service account with appropriate permissions
- Cloud Storage bucket (for Agent Engine deployment)

#### Local Deployment

1. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your project details
```

2. **Run the agent**:
```bash
uv run adk web
```

The agent will be available at `http://localhost:8000`.

#### Agent Engine Deployment (Google Cloud)

For deploying to Google Cloud's Agent Engine:

1. **Configure deployment settings**:

Edit `.env` to include:
```bash
GOOGLE_CLOUD_STORAGE_BUCKET=your-deployment-bucket
```

2. **Deploy using ADK**:
```bash
uv run adk deploy job_hunter_agent \
  --project-id=your-project-id \
  --location=us-central1
```

3. **Verify deployment**:
```bash
uv run adk list-deployments
```

4. **Test deployed agent**:
```bash
uv run adk test-deployment job_hunter_agent
```

#### Deployment Checklist

- [ ] Vertex AI API enabled in GCP project
- [ ] Service account created with necessary permissions
- [ ] Environment variables configured
- [ ] Dependencies installed (`uv sync`)
- [ ] Tests passing (`uv run pytest`)
- [ ] Cloud Storage bucket created (for Agent Engine)
- [ ] Authentication configured (`gcloud auth application-default login`)

### Production Deployment

The complete system (Phase 1 + Phase 2) is ready for production deployment with all 5 sub-agents operational.

**Current Capabilities:**
- All 5 sub-agents fully implemented and tested
- Complete end-to-end workflow from career analysis to interview prep and strategy
- State management across all workflow stages
- Error handling and user guidance
- Integration testing validated

**Production Enhancements (Future):**
- Cloud SQL for persistent state storage
- Redis for session caching
- Load balancing for scalability
- User authentication and authorization
- Monitoring and logging
- Rate limiting and quota management

## Troubleshooting

### Common Issues

**Issue: "uv is not recognized" but you have uv installed**
```bash
# Solution: uv is installed but not in your PATH
# Use python -m uv instead:
python -m uv sync
python -m uv run adk web

# Or add uv to PATH (Windows):
# Add %USERPROFILE%\.local\bin to your PATH environment variable

# Or use pip instead:
python -m pip install google-adk google-genai google-cloud-aiplatform pydantic python-dotenv hypothesis pytest pytest-asyncio nest-asyncio
```

**Issue: "Module not found" errors**
```bash
# Solution: Ensure dependencies are installed
# With uv:
uv sync
# Or if uv not in PATH:
python -m uv sync

# With pip:
python -m pip install google-adk google-genai google-cloud-aiplatform pydantic python-dotenv hypothesis pytest pytest-asyncio nest-asyncio
```

**Issue: "Authentication failed" errors**
```bash
# Solution: Re-authenticate with Google Cloud
gcloud auth application-default login
```

**Issue: "Vertex AI API not enabled"**
```bash
# Solution: Enable the API
gcloud services enable aiplatform.googleapis.com --project=your-project-id
```

**Issue: State keys not persisting between sessions**
```
# Solution: This is expected in MVP (in-memory state)
# For persistent state, use the state_manager with a database backend (Phase 2)
```

**Issue: Google Search not working**
```
# Solution: Configure Google Search API credentials in .env
GOOGLE_SEARCH_API_KEY=your-api-key
GOOGLE_SEARCH_ENGINE_ID=your-engine-id
```

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

- Check the [Design Document](.kiro/specs/job-hunter-agent/design.md) for architecture details
- Review [Requirements](.kiro/specs/job-hunter-agent/requirements.md) for expected behavior
- See [User Interaction Features](USER_INTERACTION_FEATURES.md) for interaction patterns
- Open an issue in the repository

## Current Limitations

The system has the following limitations:

1. **In-Memory State**: State is not persisted between sessions (future enhancement: database persistence)
2. **No Authentication**: No user authentication or authorization (future enhancement)
3. **Limited Search**: Google Search integration is basic (can be enhanced with job board APIs)
4. **No Resume Parsing**: Cannot parse uploaded PDF/DOCX resumes (future enhancement)
5. **Manual LinkedIn Updates**: LinkedIn profile optimization provides copy-paste text rather than direct API updates (LinkedIn API limitation)

## Roadmap

### ✅ Current MVP (Complete)
- [x] **5 Specialized AI Agents** — Career Profile Analyst, Job Market Researcher, Application Strategist, Interview Coach, Career Strategy Advisor
- [x] **Career Coordinator** — Orchestrates all sub-agents through workflow stages
- [x] **ATS Optimization** — Keyword analysis and match scoring (90%+ typical)
- [x] **Cover Letter Generation** — Tailored cover letters for each application
- [x] **Interview Preparation** — Company research, STAR examples, study plans
- [x] **Career Strategy Planning** — 5-year roadmaps, skills gap analysis, industry trends
- [x] **State Management** — Track multiple job applications
- [x] **Error Handling** — Graceful degradation and user-friendly messages
- [x] **Comprehensive Testing** — Unit, property-based, and integration tests

### 🚧 Phase 2: Flexible Architecture & Gemini 3 Pro (In Progress)

Phase 2 transforms the Job Hunter Agent from a rigid pipeline into a flexible, conversational advisor with persistent sessions and advanced AI capabilities.

#### ✅ Completed Features

**Core Infrastructure:**
- [x] **PostgreSQL database integration** — Complete schema with connection pooling, migrations, and indexes
  - Users, profiles, experiences, skills, education tables
  - Conversations and cached analyses storage
  - Applications and resume versions tracking
  - Optimized indexes for fast queries
  - See: `job_hunter_agent/database/` for implementation

- [x] **User authentication & session management** — Secure authentication system
  - bcrypt password hashing (12 rounds)
  - Session token generation and validation
  - User registration and login/logout
  - Session storage with expiration
  - See: `job_hunter_agent/auth/` for implementation

**AI & Routing:**
- [x] **Managing Coordinator with flexible routing** — LLM-based intelligent routing
  - Natural language intent understanding (no hardcoded keywords)
  - Routes to 1-3 specialists based on question content
  - Synthesizes responses from multiple specialists
  - Maintains conversation context across turns
  - See: `job_hunter_agent/managing_coordinator.py` and `MANAGING_COORDINATOR_README.md`

- [x] **Gemini 3 Pro model upgrade** — Advanced reasoning capabilities
  - Career Profile Analyst upgraded to `gemini-3-pro-preview`
  - Job Market Researcher upgraded to `gemini-3-pro-preview`
  - Configured with high thinking level for complex analysis
  - Thought Signatures handled automatically by ADK
  - See: `GEMINI3_UPGRADE_SUMMARY.md` and `JOB_MARKET_RESEARCHER_UPGRADE.md`

**Documentation & Testing:**
- [x] **Comprehensive Phase 2 documentation** — Complete technical docs
  - Managing Coordinator usage guide
  - Database setup and migration guides
  - Authentication implementation details
  - Gemini 3 Pro upgrade documentation
  - Verification scripts for all upgrades

- [x] **Phase 2 integration tests** — Validated all components
  - Managing Coordinator configuration tests (18/18 passing)
  - Database connection and schema tests
  - Authentication flow tests
  - Model upgrade verification tests
  - Backward compatibility tests

#### 🔄 In Progress

- [ ] **Application Strategist Gemini 3 Pro upgrade** — Strategic resume optimization
- [ ] **Interview Preparation specialist upgrade** — Enhanced interview prep with Gemini 3 Pro
- [ ] **Strategic Career Advisor upgrade** — Advanced career planning capabilities
- [ ] **Conversation history management** — Database-backed conversation persistence
- [ ] **Career profile CRUD operations** — Full profile management with caching
- [ ] **Application tracking CRUD** — Complete application lifecycle tracking

#### 📋 Planned Features

- [ ] **Performance optimization** — Parallel specialist execution, caching, streaming responses
- [ ] **Resume parsing** — Upload PDF/DOCX resumes for analysis
- [ ] **Enhanced job board integration** — Direct APIs for Indeed, Glassdoor
- [ ] **Salary negotiation guidance** — Negotiation strategies and scripts
- [ ] **Mock interview practice** — Voice-based interview simulation
- [ ] **Skills assessment tracking** — Track certifications and skill development
- [ ] **Follow-up automation** — Automated reminders and follow-up scheduling

#### 📚 Phase 2 Documentation

- **[Phase 2 Progress Summary](PHASE2_PROGRESS.md)** — Complete Phase 2 status and progress ⭐
- **[Managing Coordinator README](job_hunter_agent/MANAGING_COORDINATOR_README.md)** — Flexible routing guide
- **[Gemini 3 Pro Upgrade Summary](GEMINI3_UPGRADE_SUMMARY.md)** — Career Profile Analyst upgrade
- **[Job Market Researcher Upgrade](JOB_MARKET_RESEARCHER_UPGRADE.md)** — Job Market Researcher upgrade
- **[Database Quick Start](job_hunter_agent/database/QUICK_START.md)** — Database setup guide
- **[Authentication README](job_hunter_agent/auth/README.md)** — Authentication implementation
- **[Phase 2 Design](../.kiro/specs/job-hunter-agent/phase2-flexible-design.md)** — Complete Phase 2 design
- **[Phase 2 Requirements](../.kiro/specs/job-hunter-agent/phase2-flexible-requirements.md)** — Detailed requirements

#### 🔍 Key Phase 2 Improvements

**Flexible Conversation Flow:**
```python
# Phase 1: Rigid pipeline - must complete steps in order
User: "Help with my resume"
Agent: "First, let's analyze your career profile..."

# Phase 2: Flexible routing - answer what's asked
User: "Help with my resume"
Agent: "I'll help you create a tailored resume. What job are you applying to?"
```

**Advanced AI Reasoning:**
- Gemini 3 Pro provides sophisticated job matching algorithms
- Deep career analysis with nuanced understanding
- Strategic market insights and trend forecasting
- Natural language intent detection without keywords

**Persistent Sessions:**
- User profiles stored in PostgreSQL
- Conversation history maintained across sessions
- Cached analyses avoid re-computation
- Multi-device access with session synchronization

**Production-Ready Infrastructure:**
- Secure authentication with bcrypt hashing
- Database connection pooling for performance
- Comprehensive error handling and logging
- Full test coverage with integration tests

**Note**: LinkedIn direct integration (OAuth) is not planned due to LinkedIn API limitations. LinkedIn profile optimization is provided as copy-paste text instead.

## Future Enhancements

### Authentication & Security
- **OAuth Integration** — Support for Google/LinkedIn OAuth for easier sign-up
- **Two-Factor Authentication** — SMS or authenticator app support for enhanced security
- **Password Reset** — Email-based password reset flow
- **Session Refresh** — Automatic token refresh before expiration
- **Rate Limiting** — Prevent brute force attacks on authentication endpoints
- **Audit Logging** — Track authentication events and security-related activities
- **Redis Session Storage** — Faster session validation for multi-server deployments
- **JWT Tokens** — Stateless authentication option for API access

### Data & Storage
- **Cloud SQL Integration** — Persistent state storage across sessions
- **Redis Caching** — Session and analysis result caching for improved performance
- **Data Export** — Export user data in machine-readable formats (JSON, CSV)
- **Data Backup** — Automated backup and recovery procedures
- **Data Retention Policies** — Configurable data retention and automatic cleanup

### Job Search & Applications
- **Resume Parsing** — Upload and parse PDF/DOCX resumes automatically
- **LinkedIn Integration** — Import profile data from LinkedIn (if API access available)
- **Job Board APIs** — Direct integration with Indeed, LinkedIn Jobs, Glassdoor
- **Application Status Tracking** — Track application progress through hiring pipeline
- **Company Alerts** — Notifications when target companies post new positions
- **Salary Comparison Tools** — Compare offers across multiple dimensions
- **Application Analytics** — Track response rates by resume version, company type, etc.

### Interview & Preparation
- **Mock Interview Practice** — Voice-based mock interview with real-time feedback
- **Video Interview Prep** — Practice with video recording and playback
- **Interview Recording** — Record practice sessions for self-review
- **Performance Analytics** — Track improvement over multiple practice sessions
- **Company-Specific Prep** — Tailored preparation based on company interview patterns
- **Peer Practice Matching** — Connect with other users for mock interviews

### Career Development
- **Skills Assessment Tests** — Interactive skills tests and certifications tracking
- **Learning Path Recommendations** — Personalized course and certification recommendations
- **Mentorship Matching** — Connect with mentors in target roles/companies
- **Career Milestone Tracking** — Visual timeline of career progress and achievements
- **Salary Negotiation Simulator** — Practice negotiation scenarios with AI
- **Onboarding Preparation** — Guidance for first 90 days at new job

### Communication & Networking
- **Email Drafting** — Generate networking emails and follow-ups
- **LinkedIn Message Templates** — Templates for reaching out to recruiters and hiring managers
- **Thank You Note Generator** — Post-interview thank you notes
- **Follow-up Scheduler** — Automated reminders for application follow-ups
- **Networking Event Finder** — Discover relevant networking events and conferences
- **Cold Outreach Campaigns** — Manage outreach to target companies

### User Experience
- **Mobile App** — Native iOS and Android applications
- **Browser Extension** — Quick access to job analysis and application tools
- **Email Integration** — Parse job postings from email and auto-create applications
- **Calendar Integration** — Sync interview schedules with Google Calendar/Outlook
- **Notification System** — Email and push notifications for important events
- **Dark Mode** — Dark theme for better viewing experience
- **Multi-language Support** — Support for non-English job searches

### Analytics & Insights
- **Job Market Trends** — Visualize hiring trends in your target market
- **Salary Trends** — Track salary changes over time for target roles
- **Skills Demand Analysis** — Identify which skills are most in-demand
- **Success Metrics Dashboard** — Track your job search effectiveness
- **Competitive Analysis** — Compare your profile against successful candidates
- **Industry Reports** — Generate reports on industry hiring patterns

### Collaboration & Sharing
- **Profile Sharing** — Share your profile with career coaches or mentors
- **Application Review** — Request feedback on application materials from peers
- **Success Stories** — Share and learn from other users' success stories
- **Community Forum** — Connect with other job seekers
- **Referral Network** — Connect with employees at target companies

### Enterprise Features
- **Team Accounts** — Support for career coaches managing multiple clients
- **White-Label Solution** — Customizable branding for career services organizations
- **API Access** — RESTful API for integration with other career tools
- **Bulk Operations** — Process multiple applications or profiles simultaneously
- **Admin Dashboard** — Manage users, monitor usage, and generate reports
- **Custom Workflows** — Configurable workflows for different career services

### AI & Model Improvements
- **Fine-tuned Models** — Custom models trained on successful job applications
- **Multi-modal Analysis** — Analyze video resumes and portfolio projects
- **Sentiment Analysis** — Analyze job descriptions for company culture signals
- **Predictive Analytics** — Predict application success probability
- **Personalized Recommendations** — ML-based job and skill recommendations
- **Continuous Learning** — Model improves based on user feedback and outcomes

### Infrastructure & Operations
- **Load Balancing** — Distribute traffic across multiple servers
- **Auto-scaling** — Automatically scale based on demand
- **Monitoring & Alerting** — Comprehensive monitoring with Prometheus/Grafana
- **Error Tracking** — Sentry or similar for error tracking and debugging
- **Performance Optimization** — Query optimization, caching strategies
- **CDN Integration** — Faster content delivery globally
- **Disaster Recovery** — Automated failover and recovery procedures

### Compliance & Privacy
- **GDPR Compliance** — Full compliance with EU data protection regulations
- **CCPA Compliance** — California Consumer Privacy Act compliance
- **SOC 2 Certification** — Security and compliance certification
- **Data Encryption** — End-to-end encryption for sensitive data
- **Privacy Controls** — Granular user control over data sharing and visibility
- **Compliance Reporting** — Automated compliance reports and audits

**Note**: These enhancements are prioritized based on user feedback and market demand. Implementation timeline will be determined based on resource availability and strategic priorities.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Run linting: `uv run ruff check .`
6. Submit a pull request

## Disclaimer

**Important Notice: For Guidance and Informational Purposes Only**

The career guidance, application materials, and interview preparation provided by this tool are generated by an AI model and are for informational and guidance purposes only. They do not constitute professional career counseling or guarantee job placement.

All generated materials should be reviewed, personalized, and verified by you before use. This tool makes no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, or suitability of the information provided.

You should ensure all application materials authentically represent your actual experience and qualifications. Always conduct your own research and consult with qualified career professionals before making important career decisions.

This agent sample is provided for illustrative purposes only and is not intended for production use. It serves as a basic example of an agent and a foundational starting point for individuals or teams to develop their own agents.

## License

Apache-2.0

---

**Built with ❤️ using Google ADK**
