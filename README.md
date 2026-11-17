# AI Inference Cost & Token Efficiency Analyzer

## Overview
A data pipeline that analyzes 10,000 real ChatGPT conversations (from the HuggingFace WildChat-1M dataset) to quantify **cost-per-useful-answer** and identify wasted AI inference spend.

## Stack
- **Python (Pandas, Tiktoken):** Token counting, cost calculation, and waste flagging.
- **SQL (SQLite):** Relational modeling, aggregations, and business logic (`CASE WHEN`).
- **Power BI:** Efficiency dashboard tracking total cost vs. wasted spend.

## Key Insights
- Identified that GPT-4 costs **140x more** than GPT-3.5 per call.
- Found that **11.8% of GPT-3.5 calls** and **5.4% of GPT-4 calls** resulted in low-value responses (refusals or truncated answers).
- Out of a **$178.12** total budget, **$6.41** was wasted on low-value responses.
- **Recommendation:** Route low-complexity prompts to GPT-3.5 to reduce baseline costs.

## Dashboard Preview
