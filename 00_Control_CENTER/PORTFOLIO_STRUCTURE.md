# PORTFOLIO_STRUCTURE.md

## Purpose

This file defines the structure, content strategy, visual direction, and quality standard for my personal portfolio website.

The portfolio website should connect my GitHub repositories, CV, project case studies, technical profile, and personal story into one coherent professional presence.

The goal is to make the website suitable for:

- job applications
- master applications
- technical interviews
- networking
- direct outreach
- personal branding
- project presentation

---

## Core Principle

The portfolio should not be a digital CV dump.

It should be a curated technical showcase.

The website should communicate:

```text
I build models, simulations, data workflows, and digital systems for complex real-world problems.
```

The site should feel:

- professional
- technical
- visual
- clean
- premium
- personal enough to be memorable
- not student-like
- not overdesigned
- not generic

---

## Target Impression

When someone opens the website, they should understand within 30 seconds:

1. Who I am
2. What technical areas I work in
3. Which projects are strongest
4. Why my background is distinctive
5. Where to click next

The impression should be:

```text
Mathematically trained builder with strong technical range, real project ownership, and visual taste.
```

---

## Main Positioning

Recommended headline:

```text
From mathematical models to real-world systems.
```

Alternative headlines:

```text
Building simulations, data systems, and digital products for complex real-world problems.
```

```text
Mathematical modeling, simulation, automation, and digital systems.
```

```text
I turn messy systems into models, simulations, and digital products.
```

Recommended subheadline:

```text
I am a mathematics graduate and technical builder working across stochastic modeling, multi-agent simulation, supply chain automation, and digital commerce systems.
```

More personal version:

```text
I combine mathematical modeling, implementation, and visual technical communication — from autonomous field operation simulations to biomedical models and digital commerce systems for a family winery.
```

---

## Website Structure

Recommended pages:

```text
/
├── About
├── Projects
│   ├── Multi-Agent Tractor Simulation
│   ├── Glioblastoma Markov Modeling
│   ├── Supply Chain Data Quality
│   ├── Winery Digital Commerce System
│   └── Portfolio Website
├── CV
├── Writing / Notes
└── Contact
```

Minimum viable version:

```text
/
├── Home
├── Projects
├── About
├── CV
└── Contact
```

Do not overbuild the first version.

The first goal is a polished, focused website with 3-4 strong case studies.

---

## Recommended Tech Stack

Preferred:

```text
Astro + Tailwind CSS
```

Reason:

- fast
- static
- clean
- easy to deploy
- good for content-heavy portfolio
- lower complexity than Next.js
- excellent for case studies

Alternative:

```text
Next.js + Tailwind CSS
```

Use only if interactive components, dynamic routes, or heavier app-like behavior are needed.

Avoid for first version:

```text
WordPress
Webflow
Framer
overly complex CMS setup
heavy animation frameworks
```

The portfolio should be technically clean and easy to maintain.

---

## Homepage Structure

Recommended homepage sections:

```text
Hero
Selected Projects
Technical Focus
About Preview
CV / Contact CTA
Footer
```

---

## Hero Section

The hero must be immediately clear.

### Recommended Hero Copy

```text
From mathematical models to real-world systems.
```

Subheadline:

```text
I build simulations, data workflows, and digital systems across mathematical modeling, autonomous systems, supply chain automation, and digital commerce.
```

CTA buttons:

```text
View Projects
Download CV
```

Optional small line:

```text
Mathematics · Simulation · Data Systems · Automation
```

---

## Selected Projects Section

Show 3-4 strong project cards.

Recommended order:

1. Multi-Agent Tractor Simulation
2. Glioblastoma Markov Modeling
3. Supply Chain Data Quality
4. Winery Digital Commerce System

Each card should include:

```text
project title
one-sentence summary
technology tags
visual thumbnail
link to case study
link to GitHub if public
```

Do not show too many projects on the homepage.

Quality beats quantity.

---

## Technical Focus Section

Use 4 focus areas:

### Mathematical Modeling

```text
Stochastic processes, numerical methods, optimization, and computational models for complex systems.
```

### Simulation and Autonomy

```text
Multi-agent coordination, scheduling, path planning, and simulation of real-world operations.
```

### Data Systems and Automation

```text
Data quality workflows, dashboards, process transparency, and operational decision support.
```

### Digital Product Systems

```text
E-commerce infrastructure, product data, SEO, analytics, and conversion-focused web systems.
```

---

## About Preview Section

Short version:

```text
I studied Business Mathematics with a focus on stochastics, numerical analysis, optimization, and programming. My work connects mathematical modeling with practical implementation — from biomedical Markov models and autonomous field operation simulations to supply chain analytics and digital business systems.
```

More personal version:

```text
My background is unusual in a useful way: rigorous mathematical training, hands-on software and data projects, industry exposure in consulting and supply chain, and entrepreneurial work through a family winery. I like projects where abstract models meet messy real-world constraints.
```

---

## Project Case Study Template

Each project page should follow this structure:

```markdown
# [Project Name]

## One-Sentence Summary

[Clear summary]

## Problem

[What problem does this project address?]

## Motivation

[Why is it interesting or relevant?]

## Approach

[What did I build?]

## Technical Implementation

[Methods, architecture, tools, algorithms]

## Output

[Screenshot, plot, GIF, dashboard, simulation result]

## Challenges

[What was difficult?]

## Limitations

[Honest boundaries]

## Future Work

[What could be improved next?]

## Technologies

[Languages, libraries, tools]

## Links

[GitHub, demo, related material]
```

---

## Flagship Project: Multi-Agent Tractor Simulation

### Positioning

```text
Simulation and scheduling framework for autonomous agricultural field operations.
```

### Case Study Angle

This project should show:

- simulation engineering
- multi-agent coordination
- graph-based planning
- scheduling under constraints
- field-operation realism
- dynamic replanning potential
- strong visual output

### Needed Visuals

```text
simulation GIF
field geometry overview
scheduler architecture diagram
agent timeline or task allocation view
example output screenshot
```

### Portfolio Summary

```text
A Python-based simulation and scheduling framework for coordinating multiple autonomous tractors during field operations such as plowing and seeding. The project models operational constraints, task dependencies, field geometry, and multi-agent coordination.
```

---

## Flagship Project: Glioblastoma Markov Modeling

### Positioning

```text
Continuous-time Markov chain model for glioblastoma cell population dynamics.
```

### Case Study Angle

This project should show:

- stochastic modeling
- mathematical biology
- computational implementation
- thesis-level technical depth
- interdisciplinary communication
- reproducible modeling workflow

### Needed Visuals

```text
state transition diagram
example simulation plot
parameter sensitivity plot
model workflow diagram
```

### Portfolio Summary

```text
A mathematical modeling project based on continuous-time Markov chains to represent glioblastoma cell population dynamics. The project connects stochastic process theory, computational implementation, and biomedical model interpretation.
```

---

## Showcase Project: Supply Chain Data Quality

### Positioning

```text
Data quality and purchase order monitoring workflow for supply chain operations.
```

### Case Study Angle

This project should show:

- operational data understanding
- SAP-related workflow logic
- purchase order monitoring
- delivery-date quality
- supplier communication context
- dashboard or reporting structure

### Needed Visuals

```text
anonymized dashboard mockup
data pipeline diagram
example data quality table
process flow diagram
```

### Portfolio Summary

```text
A supply chain analytics and monitoring concept focused on purchase order transparency, delivery-date quality, and data-driven process improvement.
```

Important:

Use anonymized or synthetic data only.

Do not expose company-private information.

---

## Showcase Project: Winery Digital Commerce System

### Positioning

```text
Digital commerce and product data system for a family winery.
```

### Case Study Angle

This project should show:

- real business ownership
- WooCommerce system design
- product data modeling
- SEO
- analytics
- branding and conversion
- visual presentation

### Needed Visuals

```text
homepage screenshot
product page screenshot
taxonomy/filter diagram
SEO/content structure diagram
before/after UI comparison
```

### Portfolio Summary

```text
A digital commerce and product data system for a family winery, combining WooCommerce, product taxonomy, SEO, analytics, branding, and conversion-focused design.
```

---

## CV Page

The CV page should include:

```text
downloadable PDF
education
experience
selected projects
technical skills
languages
contact
```

Do not overload it.

The CV page should be clean and easy to scan.

Recommended CTA:

```text
Download CV
```

Optional:

```text
View GitHub
View LinkedIn
Contact me
```

---

## About Page

The About page should explain the story.

Suggested structure:

```text
Short intro
Academic background
Technical direction
Project philosophy
Personal angle
Current focus
```

The story should connect:

1. Business mathematics
2. stochastic modeling and numerical methods
3. glioblastoma modeling
4. robotics/simulation interest
5. supply chain and data systems
6. winery digital business
7. current direction toward complex technical systems

Avoid writing a long autobiography.

Keep it focused and useful.

---

## Writing / Notes Page

Optional, not necessary for version 1.

Possible topics:

```text
What I learned building a multi-agent field simulation
How to present academic code as a portfolio project
From Markov chains to biological dynamics
Data quality problems in supply chain operations
Building digital infrastructure for a family winery
```

This could become useful later for SEO and technical credibility.

Do not build this page before the project pages are strong.

---

## Contact Page

Simple contact section:

```text
Email
LinkedIn
GitHub
Location: Munich / Germany
```

Do not include too much personal information.

Contact copy:

```text
For project discussions, technical roles, collaborations, or opportunities, feel free to reach out.
```

---

## Visual Direction

The design should feel:

```text
technical
premium
clean
modern
slightly personal
visually precise
```

Avoid:

```text
generic SaaS startup template
neon hacker aesthetic
student portfolio look
too many badges
cartoon icons
excessive animations
```

Good visual motifs:

```text
field lines
contour lines
graph networks
state diagrams
simulation paths
mathematical notation
subtle vineyard references
clean serif/sans typography combinations
```

---

## Color Direction

Possible palette:

```text
off-white
deep green
dark graphite
warm beige
muted gold
soft gray
```

This connects technical clarity with the vineyard side without becoming rustic.

Avoid:

```text
bright neon
pure black-and-white only
too many colors
random gradients
```

---

## Typography Direction

Use a clean modern sans-serif for body text.

Possible heading direction:

```text
strong sans-serif
subtle serif accent
technical but premium
```

Avoid:

```text
overly playful fonts
default template typography
too many font families
```

---

## Animation Rules

Use animation sparingly.

Good animations:

```text
subtle fade-in
project card hover
small line movement
diagram reveal
smooth page transitions
```

Avoid:

```text
constant motion
parallax overload
3D gimmicks
cursor effects that distract
slow loading animations
```

The website should feel refined, not noisy.

---

## Homepage Copy Draft

```markdown
# From mathematical models to real-world systems.

I build simulations, data workflows, and digital systems across mathematical modeling, autonomous systems, supply chain automation, and digital commerce.

[View Projects] [Download CV]

## Selected Projects

### Multi-Agent Tractor Simulation
Simulation and scheduling framework for autonomous agricultural field operations.

### Glioblastoma Markov Modeling
Continuous-time Markov chain model for glioblastoma cell population dynamics.

### Supply Chain Data Quality
Purchase order monitoring and data quality workflow for supply chain operations.

### Winery Digital Commerce System
Digital commerce and product data system for a family winery.
```

---

## Navigation

Recommended navigation:

```text
Projects
About
CV
Contact
```

Optional later:

```text
Writing
```

Keep navigation simple.

---

## Footer

Footer should include:

```text
Felix Klein
GitHub
LinkedIn
Email
Location
```

Optional line:

```text
Mathematical modeling · Simulation · Data systems · Digital products
```

---

## Deployment

Recommended deployment:

```text
GitHub Pages
```

or:

```text
Vercel
```

For Astro:

```text
Vercel
Netlify
GitHub Pages
```

Best first choice:

```text
Vercel
```

Reason:

- easy deployment
- good preview links
- works well with modern frontend stack
- simple GitHub integration

---

## Version 1 Scope

Version 1 should include:

```text
Homepage
Projects overview
2 full case studies
CV page
Contact links
basic responsive design
GitHub links
downloadable CV
```

Recommended first two full case studies:

```text
Multi-Agent Tractor Simulation
Glioblastoma Markov Modeling
```

Add the others as shorter cards first.

Do not delay launch because every case study is not perfect.

---

## Version 2 Scope

Version 2 can add:

```text
Supply Chain case study
Winery digital commerce case study
better visuals
project thumbnails
writing section
animations
improved SEO
custom domain
```

---

## SEO Basics

Use clear page titles:

```text
Felix Klein – Mathematical Modeling, Simulation & Data Systems
```

Project page titles:

```text
Multi-Agent Tractor Simulation – Felix Klein
Glioblastoma Markov Modeling – Felix Klein
Supply Chain Data Quality – Felix Klein
Winery Digital Commerce System – Felix Klein
```

Meta description:

```text
Portfolio of Felix Klein, a mathematics graduate building simulations, data workflows, and digital systems across modeling, automation, and real-world operations.
```

---

## Portfolio Quality Checklist

Before publishing:

```text
Homepage explains positioning clearly
Projects are easy to scan
At least 2 projects have detailed case studies
CV is downloadable
GitHub links work
Contact links work
Mobile layout works
No placeholder text remains
No private information is exposed
Images are compressed
Writing is precise and non-generic
Design feels intentional
```

---

## Definition of Done

The portfolio is ready for version 1 when:

```text
A technical reader can understand my profile in 30 seconds.
A recruiter can identify my strongest projects quickly.
A professor or engineer can see technical credibility.
The website looks more professional than a student portfolio.
The projects connect to GitHub and CV.
The site is clean, responsive, and visually strong.
```

The final standard is:

```text
professional technical portfolio with distinctive personal positioning
```
