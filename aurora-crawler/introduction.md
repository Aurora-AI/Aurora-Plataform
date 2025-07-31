What is Agno? - Agno
Agno
home page
Search...
⌘
K
Ask AI
Discord
Community
agno-agi
/
agno
agno-agi
/
agno
Search...
Navigation
Introduction
What is Agno?
User Guide
Examples
Workspaces
FAQs
API reference
Changelog
Introduction
What is Agno?
Your first Agents
Multi Agent Systems
Playground
Monitoring & Debugging
Community & Support
Concepts
Agents
Teams
Models
Tools
Reasoning
Memory
Knowledge
Chunking
Vector DBs
Storage
Embeddings
Evals
Workflows
Workflows v2 (Beta)
Applications
Other
Agent UI
Agent API
Observability
Testing
How to
Install & Setup
Contributing to Agno
Migrate from Phidata to Agno
Authenticate with Agno Platform
On this page
Getting Started
Why Agno?
Dive deeper
Introduction
What is Agno?
Copy page
Agno is a python framework for building multi-agent systems with shared memory, knowledge and reasoning.
Engineers and researchers use Agno to build:
Level 1:
Agents with tools and instructions (
example
).
Level 2:
Agents with knowledge and storage (
example
).
Level 3:
Agents with memory and reasoning (
example
).
Level 4:
Agent Teams that can reason and collaborate (
example
).
Level 5:
Agentic Workflows with state and determinism (
example
).
Example:
Level 1 Reasoning Agent that uses the YFinance API to answer questions:
Reasoning Finance Agent
Copy
Ask AI
from
agno.agent
import
Agent
from
agno.models.anthropic
import
Claude
from
agno.tools.reasoning
import
ReasoningTools
from
agno.tools.yfinance
import
YFinanceTools
reasoning_agent
=
Agent(
model
=
Claude(
id
=
"claude-sonnet-4-20250514"
),
tools
=
[
ReasoningTools(
add_instructions
=
True
),
YFinanceTools(
stock_price
=
True
,
analyst_recommendations
=
True
,
company_info
=
True
,
company_news
=
True
),
],
instructions
=
"Use tables to display data."
,
markdown
=
True
,
)
Watch the reasoning finance agent in action
​
Getting Started
If you’re new to Agno, learn how to build your
first Agent
, chat with it on the
playground
and
monitor
it on
app.agno.com
.
Your first Agents
Learn how to build Agents with Agno
Agent Playground
Chat with your Agents using a beautiful Agent UI
Agent Monitoring
Monitor your Agents on
agno.com
After that, dive deeper into the
concepts below
or explore the
examples gallery
to build real-world applications with Agno.
​
Why Agno?
Agno will help you build best-in-class, highly-performant agentic systems, saving you hours of research and boilerplate. Here are some key features that set Agno apart:
Model Agnostic
: Agno provides a unified interface to 23+ model providers, no lock-in.
Highly performant
: Agents instantiate in
~3μs
and use
~6.5Kib
memory on average.
Reasoning is a first class citizen
: Reasoning improves reliability and is a must-have for complex autonomous agents. Agno supports 3 approaches to reasoning: Reasoning Models,
ReasoningTools
or our custom
chain-of-thought
approach.
Natively Multi-Modal
: Agno Agents are natively multi-modal, they accept text, image, audio and video as input and generate text, image, audio and video as output.
Advanced Multi-Agent Architecture
: Agno provides an industry leading multi-agent architecture (
Agent Teams
) with reasoning, memory, and shared context.
Built-in Agentic Search
: Agents can search for information at runtime using 20+ vector databases. Agno provides state-of-the-art Agentic RAG,
fully async and highly performant.
Built-in Memory & Session Storage
: Agents come with built-in
Storage
&
Memory
drivers that give your Agents long-term memory and session storage.
Structured Outputs
: Agno Agents can return fully-typed responses using model provided structured outputs or
json_mode
.
Pre-built FastAPI Routes
: After building your Agents, serve them using pre-built FastAPI routes. 0 to production in minutes.
Monitoring
: Monitor agent sessions and performance in real-time on
agno.com
.
​
Dive deeper
Agno is a battle-tested framework with a state of the art reasoning and multi-agent architecture, read the following guides to learn more:
Agents
Learn how to build lightning fast Agents.
Teams
Build autonomous multi-agent teams.
Models
Use any model, any provider, no lock-in.
Tools
100s of tools to extend your Agents.
Reasoning
Make Agents “think” and “analyze”.
Knowledge
Give Agents domain-specific knowledge.
Vector Databases
Store and search your knowledge base.
Storage
Persist Agent session and state in a database.
Memory
Remember user details and session summaries.
Embeddings
Generate embeddings for your knowledge base.
Workflows
Deterministic, stateful, multi-agent workflows.
Evals
Evaluate, monitor and improve your Agents.
Assistant
Responses are generated using AI and may contain mistakes.
Was this page helpful?
Yes
No
Suggest edits
Raise issue
Your first Agents
x
github
discord
youtube
website
Powered by Mintlify