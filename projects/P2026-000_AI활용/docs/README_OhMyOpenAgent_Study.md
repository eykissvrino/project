# OhMyOpenAgent Reference Architecture Study

**Date**: 2026-03-24  
**Status**: ✅ Complete  
**Repository Analyzed**: https://github.com/code-yeongyu/oh-my-openagent (v3.11.0)

---

## 📋 Deliverables

### 1. **OhMyOpenAgent_Architecture_Analysis.md** (13 KB, 367 lines)
Comprehensive technical analysis covering:
- Executive summary and core innovation
- 3-layer architecture overview
- 11 agents, 26 tools, 19 features, 48 hooks
- Design patterns and philosophy
- Developer-focused features
- What needs to change for non-developers
- Directory structure and dependencies
- Working modes and verification strategies

### 2. **summary.txt** (5.6 KB, 178 lines)
Executive summary with:
- Key findings
- 8 design patterns to adopt
- Adaptations needed for non-developers
- Business-specific adaptations
- 5-phase implementation roadmap
- Critical success factors
- Risks and mitigations

---

## 🎯 Key Findings

### Architecture
- **3-Layer System**: Planning (Prometheus, Metis, Momus) → Orchestration (Atlas) → Workers (11 agents)
- **Scale**: 1,427 TypeScript files, ~40,000 LOC
- **Components**: 26 tools, 48 hooks, 19 feature modules, 11 specialized agents

### Core Innovation
**Intent-Based Delegation**: Classify work by intent, auto-route to specialists
```
User Request → Intent Gate → Category Classification → Model Assignment → Execution
```

Instead of users saying "use tool X with model Y", the system understands intent and automatically selects the right agent/skill.

### Developer Focus
- CLI-first interface (ultrawork, /start-work, /init-deep)
- Code-centric tools (LSP, AST-Grep, hash-anchored edits)
- Technical configuration (JSONC, Zod validation)
- Extensibility (skills, commands, MCPs, hooks)

---

## 🏗️ Design Patterns to Adopt

### 1. Intent-Based Delegation
**What**: Classify work by intent, auto-route to specialists  
**Why**: Users don't need to know which tool/agent to use  
**How**: User says "do job analysis" → system auto-selects job-analysis skill

### 2. Planning-Execution Separation
**What**: Separate planning phase from execution phase  
**Why**: Prevents cognitive drift, enables verification, creates audit trail  
**How**: Collaborate on plan with user, then AI executes automatically

### 3. Parallel Background Work
**What**: Fire 5+ agents in parallel while main agent continues  
**Why**: Context stays lean, results available on-demand, no blocking  
**How**: While generating proposal, collect related data in background

### 4. Multi-Level Configuration
**What**: Project → User → Defaults with automatic deep merge  
**Why**: Flexible, no conflicts, sensible defaults  
**How**: Project settings override user settings override system defaults

### 5. Skill System
**What**: Domain-tuned instructions + embedded tools/MCPs + scoped permissions  
**Why**: Reusable, composable, context-efficient  
**How**: HR consulting skill, project management skill, document generation skill

### 6. Dynamic Prompt Building
**What**: Generate agent prompts dynamically based on available agents/tools/skills  
**Why**: No hardcoded prompts, adapts to setup, model-specific variants  
**How**: Sisyphus-like orchestrator generates prompts based on available skills

### 7. Three-Tier Hook System
**What**: Session → Tool-Guard → Transform → Continuation → Skill hooks  
**Why**: Prevents hook conflicts, clear responsibilities  
**How**: Hook system for custom business logic injection

### 8. Hash-Anchored Edits
**What**: Every line tagged with content hash, edits by hash not content  
**Why**: Zero stale-line errors, safe changes  
**How**: For document/file modifications - ensure safe, verifiable changes

---

## 🔄 What to Adapt for Non-Developers

| Aspect | FROM | TO | HOW |
|--------|------|----|----|
| **Interface** | CLI commands | Natural language | Conversational triggers |
| **Terminology** | Technical terms | Business terms | Translate concepts |
| **Workflow** | Plan → Execute → Verify | Just "Do it" | Hide orchestration |
| **Output** | JSON/YAML/Markdown | Forms/Dashboards | Transform output |
| **Errors** | Explicit errors | Implicit recovery | Auto-retry |
| **Config** | JSONC files | UI wizard | Hide config files |

---

## 💼 Business-Specific Adaptations

### Agents
- **Sisyphus** → Project Manager (orchestrates work)
- **Oracle** → Expert Advisor (strategic advice)
- **Librarian** → Knowledge Assistant (documentation search)
- **Prometheus** → Planning Assistant (interviews, plans)
- **Explore** → Research Assistant (quick information)

### Skills
1. **HR Consulting** - job analysis, org design, competency mapping
2. **Project Management** - planning, tracking, risk management
3. **Document Generation** - proposals, reports, presentations
4. **Data Analysis** - Excel, charts, insights
5. **Strategic Planning** - SWOT, BSC, scenario planning

### Workflows
1. **Job Analysis**: interview → analysis → report
2. **Org Design**: assessment → design → implementation plan
3. **Project Planning**: scope → plan → tracking
4. **Proposal Generation**: research → draft → review → finalize
5. **Data Analysis**: collect → analyze → visualize → insights

---

## 📊 Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- Adapt intent-based delegation for HR/business domain
- Build simplified orchestrator
- Create multi-level configuration system
- Implement planning-execution separation

### Phase 2: Skills & Tools (Weeks 3-4)
- Build HR consulting skill
- Build project management skill
- Build document generation skill
- Build data analysis skill

### Phase 3: Interface (Weeks 5-6)
- Replace CLI with natural language
- Build UI-based setup wizard
- Create progress dashboard
- Implement conversational triggers

### Phase 4: Integration (Weeks 7-8)
- Integrate with business tools (Excel, PowerPoint)
- Build output formatters
- Implement automatic error recovery
- Add business-specific workflows

### Phase 5: Polish (Weeks 9-10)
- User testing and feedback
- Performance optimization
- Documentation and training
- Deployment and monitoring

---

## ⚠️ Critical Success Factors

1. **Intent-based delegation must work seamlessly** - users shouldn't need to know which tool to use
2. **Planning-execution separation must feel natural** - not like extra steps
3. **Error recovery must be automatic** - users shouldn't see technical errors
4. **Output must be business-friendly** - no JSON/YAML/code diffs
5. **Configuration must be hidden** - sensible defaults for all workflows
6. **Skills must be composable** - combine multiple skills for complex tasks

---

## 🚨 Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Over-engineering | Focus on core patterns, adapt others as needed |
| Complexity hidden from users | Provide transparency through dashboards and explanations |
| Model lock-in | Implement fallback chains like OmO does |
| Configuration complexity | Sensible defaults, UI-based setup, minimal configuration |

---

## 📚 How to Use This Analysis

### For Architects
- Read **OhMyOpenAgent_Architecture_Analysis.md** for deep technical understanding
- Focus on design patterns section for architectural decisions
- Review directory structure for component organization

### For Product Managers
- Read **summary.txt** for business-specific adaptations
- Review implementation roadmap for timeline and phases
- Check critical success factors and risks

### For Developers
- Read **OhMyOpenAgent_Architecture_Analysis.md** for implementation details
- Study design patterns for code organization
- Review tool and hook systems for extensibility

### For Project Planning
- Use implementation roadmap as baseline
- Identify which patterns are most applicable to your domain
- Start with intent-based delegation as foundation
- Build HR consulting skill as first proof-of-concept

---

## 🔗 References

- **OhMyOpenAgent Repository**: https://github.com/code-yeongyu/oh-my-openagent
- **Documentation**: https://github.com/code-yeongyu/oh-my-openagent/tree/dev/docs
- **AGENTS.md**: https://github.com/code-yeongyu/oh-my-openagent/blob/dev/AGENTS.md
- *
