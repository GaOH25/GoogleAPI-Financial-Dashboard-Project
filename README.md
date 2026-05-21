# THALFScape Financial Dashboard

THALFScape is a small AI-driven personal finance dashboard built with Streamlit and Google's Gemini API. It was originally made as a class project, so the goal was not to build a perfect or production-ready financial calculator. The main idea was to experiment with how well an AI model could analyze user-provided financial data and generate useful financial insights.

The app lets users enter monthly income, expenses, expected financial changes, and basic financial goals. After that, the AI generates a financial analysis that includes expense categorization, ratio analysis, projections, and final recommendations.

## What This Project Does

THALFScape allows users to:

- Enter monthly income
- Add monthly expenses
- Clear all expenses
- View total monthly expenses
- View remaining income after expenses
- Enter expected monthly income changes
- Enter expected monthly expense changes
- Select a financial goal
- Generate an AI-written financial analysis
- View expense breakdown charts
- View a 3-month financial projection trend

## Why AI-Driven?

This project was intentionally designed so that the AI handles most of the financial analysis.

In a more serious financial app, the safest approach would probably be to calculate everything directly in Python and then use AI only to explain the results. However, that was not the goal here. The purpose of this project was to test how well an AI model could perform the main analysis itself.

Because of that, the AI is responsible for generating:

- Expense categorization
- Savings rate analysis
- Needs vs. wants analysis
- Housing cost ratio analysis
- 3-month financial projections
- Final financial insights
- Goal-based recommendations

This makes the project more of an AI-analysis prototype than a traditional finance calculator.

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
```

Install the required packages:

```bash
pip install streamlit google-genai matplotlib seaborn
```

Optionally, you can create a `requirements.txt` file with:

```txt
streamlit
google-genai
matplotlib
seaborn
```

Then install everything using:

```bash
pip install -r requirements.txt
```

## API Key Setup

This project uses the Gemini API, so you need an API key.

Set your API key as an environment variable named:

```bash
GEMINI_API_KEY
```

On Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

On macOS/Linux:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

The app reads the key using:

```python
os.getenv("GEMINI_API_KEY")
```

## Running the App

Run the Streamlit app with:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## How It Works

The user enters financial data through the Streamlit sidebar. This includes income, expenses, expected income changes, expected expense changes, and a financial goal.

The app then builds a structured prompt using that information and sends it to Gemini. The AI generates the financial report based on the provided data.

The app also creates visualizations using Matplotlib and Seaborn, including:

- Expense breakdown bar chart
- Expense distribution pie chart
- Future projection trend chart

## Known Imperfections

Since this project relies heavily on AI-generated analysis, the output is not always perfect.

Some known issues include:

- The AI may occasionally make mathematical mistakes.
- The AI may sometimes ignore formatting instructions.
- The AI may still output LaTeX-style formatting even when told not to.
- Different Gemini models may produce different levels of consistency.
- Faster or smaller models may be less reliable.
- More advanced models may produce better results, but access, quotas, and availability can vary.
- The cleanup function helps reduce some unwanted formatting, but it does not completely solve the issue.

These imperfections were part of the learning experience. The project helped show both the usefulness and the limitations of using generative AI for financial analysis.

## Project Status

This project was completed as a class project and has already served its original purpose.

It is not currently being developed as a full financial application, but it remains a useful prototype for experimenting with:

- Streamlit interfaces
- AI-generated reports
- Prompt engineering
- Financial data visualization
- User-driven financial scenarios

## Disclaimer

THALFScape is an educational project.

It should not be used as professional financial advice. The AI-generated output may contain mistakes, especially in calculations or recommendations. Any important financial decisions should be double-checked manually or reviewed with a qualified professional.

## Author

Created as part of a class project exploring AI-assisted financial analysis.
