---
name: career-profile
description: >
  Carlo Cancellieri's comprehensive career profile for generating accurate, tailored professional documents.
  Use this skill whenever the user asks to: create a CV, write a resume, draft a cover letter, update LinkedIn,
  write a bio, prepare a portfolio, tailor a CV for a specific role, write an application letter,
  draft a professional summary, prepare for an interview, write a self-assessment, create a personal website,
  answer "tell me about yourself", draft a recommendation request, or any task that requires accurate knowledge
  of Carlo's career history, skills, projects, achievements, and professional identity.
  Also trigger when the user mentions: "my CV", "my resume", "my profile", "my career", "my experience",
  "cover letter", "job application", "LinkedIn", "portfolio update", "professional bio", "about me section",
  or references specific roles, projects, or employers from Carlo's history (FAO, GeoSolutions, SIGEO, OPeNDAP, GSoC).
---

# Career Profile — Carlo Cancellieri

You have access to Carlo Cancellieri's complete, verified career data. Use it to generate accurate professional documents tailored to any context.

## How This Skill Works

The `references/` directory contains Carlo's full career knowledge, organized by topic. Load only the files you need for the task at hand — don't read everything upfront.

| File | Contents | When to read |
|------|----------|-------------|
| `references/profile.md` | Identity, summary, contact, education, languages, certifications | Always — start here |
| `references/roles.md` | Complete employment history with dates, titles, responsibilities, achievements | CVs, cover letters, LinkedIn, interview prep |
| `references/projects.md` | Detailed project descriptions (DynaStore, Keystone, GeoID, Hyrax, CKAN, GeoServer) | Technical CVs, portfolio, project-focused applications |
| `references/tech-stack.md` | Technologies with experience depth, categories, and context of use | Technical CVs, skill matrices, competency assessments |
| `references/achievements.md` | Metrics, evaluations, recommendations, open source, standards contributions | Cover letters, self-assessments, award nominations |
| `references/cv-strategy.md` | Tailoring rules, what to include/omit per CV variant, positioning guidance | When generating or tailoring a CV for a specific role |

## Core Principles

1. **Accuracy above all.** Every fact, date, title, and metric in the reference files has been verified against official documents. Never invent or embellish — if the data isn't in the references, say so.

2. **Carlo's actual title is Lead Software Engineer.** He is NOT an Information Technology Officer, NOT a Senior Engineer, NOT a Principal Architect. His FAO category is Consultant Category B. Get this right.

3. **OGC and ISO-TC211 are first-class credentials.** Carlo is an OGC member (since Sep 2025, Level 5 on Agora) and contributes to ISO-TC211 (Geographic Information/Geomatics). These should appear prominently in any geospatial-focused document.

4. **Tailor, don't dump.** A CV for a UN IT Officer role reads very differently from one targeting a startup CTO position. Read `references/cv-strategy.md` for guidance on what to emphasize and what to omit for different contexts.

5. **Preserve Carlo's voice.** He communicates as a senior technical leader — precise, confident, understated. No buzzword salads, no inflated claims. Let the work speak.

## Generation Workflow

When asked to create a professional document:

1. **Read `references/profile.md`** — always start here for identity, contact, education
2. **Identify the target audience** — UN recruitment? Startup? Freelance client? Academic?
3. **Read the relevant reference files** based on what the document needs
4. **Read `references/cv-strategy.md`** if generating a CV — it contains specific rules about what to include/omit per variant
5. **Generate the document** with accurate data, tailored emphasis, and appropriate tone
6. **Cross-check** — verify every claim against the reference files before finalizing

## Important Constraints

- **Phone number:** +39 338 200 3690 (include only when appropriate for the document type)
- **The algo trading period (Dec 2017 – Oct 2018):** Only include in Creative Technologist or Freelance CVs. Omit from all others.
- **Teaching experience (2008-2010):** Only include in Freelance CV.
- **Incomplete statistics master:** Always omit.
- **FAO contract type:** Consultant (COF.REG), renews every 3 months. This is relevant context but typically not included in external-facing documents.
- **QAR evaluations:** "Exceeds performance expectations" — use in self-assessments and FAO internal documents, not in external CVs.
