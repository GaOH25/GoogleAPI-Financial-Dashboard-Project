# THALFScape Financial Dashboard

THALFScape is a small AI-driven personal finance dashboard built with Streamlit and Google's Gemini API. It was originally made as a class project, so the main goal was not to build a perfect financial calculator, but to experiment with how far an AI model could go when asked to analyze user-provided financial data.

The app lets users enter monthly income, expenses, expected financial changes, and basic financial goals. It then asks an AI model to generate a financial analysis that includes expense categorization, ratio analysis, projections, and final insights.

## What This Project Does

THALFScape allows users to:

- Enter monthly income
- Add and clear monthly expenses
- View total expenses and remaining income
- Add expected monthly income or expense changes
- Select a financial goal
- Generate an AI-written financial analysis
- View expense breakdown charts
- View a 3-month projection trend chart

The main idea behind the project was to let the AI handle most of the financial reasoning, including categorization, ratios, projections, and recommendations.

## Why AI-Driven?

This project was intentionally designed around AI-generated analysis. Normally, the safest approach would be to calculate all financial values directly in Python and use AI only for explanations. However, the purpose of this project was different: it was meant to test how well an AI model could handle a larger part of the financial analysis process.

Because of that, the AI is responsible for generating the main report, including:

- Expense categorization
- Savings rate interpretation
- Needs vs. wants analysis
- Housing cost ratio
- 3-month financial projections
- Personalized insights based on the user's goal

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Matplotlib
- Seaborn
- Regular expressions for minor AI-output cleanup

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/THALFScape.git
cd THALFScape
