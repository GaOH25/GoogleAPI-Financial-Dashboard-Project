from google import genai
import streamlit as st
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="THALFScape", page_icon="💰", layout="centered")
st.title("THALFScape Project")
st.markdown("## Personal Finance Analysis")

# System Prompt (Hidden From User) with LaTeX restriction
system_prompt = """
You are a helpful and insightful financial analyst. Your task is to analyze provided financial data and offer straightforward, actionable insights.

**CRITICAL FORMATTING RULES:**
- **NO LaTeX/Math Formatting:** Never use LaTeX syntax like \[ \], \( \), $$, \text, etc.
- **Clean Calculations:** Show calculations clearly but without messy parentheses
- **Keep Final Insights:** Maintain separate Final Insights section at the end

**ANALYSIS TASKS:**
1. **Expense Categorization:** Group expenses into standard categories
2. **Ratio Analysis:** Calculate key financial ratios with brief interpretations
3. **Financial Projection:** Project net cash flow for next 3 months

**OUTPUT REQUIREMENTS:**
Structure your response with these exact headings and formatting:

### Expense Categorization
- **Housing:** $Amount (description)
- **Food:** $Amount (description)
- **Transportation:** $Amount (description)
- **Utilities:** $Amount (description)
- **Entertainment:** $Amount (description)
- **Other:** $Amount (description)

### Ratio Analysis
- **Savings Rate:** X% | Calculation: (Income - Expenses) / Income | Interpretation: [Brief one-sentence insight]
- **Needs vs Wants:** Y% needs, Z% wants | Needs: [list categories], Wants: [list categories] | Interpretation: [Brief one-sentence insight]
- **Housing Cost Ratio:** A% | Calculation: Housing / Income | Interpretation: [Brief one-sentence insight against 30% guideline]

### Financial Projection
| Month | Projected Income | Projected Expenses | Projected Net |
| :--- | :--- | :--- | :--- |
| Next Month | $X | $Y | $Z |
| Month +2 | $X | $Y | $Z |
| Month +3 | $X | $Y | $Z |

### Final Insights
1. [First insight as a complete sentence]
2. [Second insight as a complete sentence]
3. [Third insight as a complete sentence]

**IMPORTANT:** Show calculations clearly but keep them organized with pipes (|) for separation. Maintain the Final Insights section separately.
"""

# Initialize session state for expenses if it doesn't exist
if 'expenses' not in st.session_state:
    st.session_state.expenses = []


def clean_latex_text(text):
    """Remove LaTeX formatting from text"""
    # Remove LaTeX math mode and commands
    text = re.sub(r'\\\[.*?\\\]', '', text)  # Remove \[ ... \]
    text = re.sub(r'\\\(.*?\\\)', '', text)  # Remove \( ... \]
    text = re.sub(r'\$.*?\$', '', text)  # Remove $ ... $
    text = re.sub(r'\\[a-z]+\{', '', text)  # Remove \command{
    text = re.sub(r'\}', '', text)  # Remove leftover }
    text = re.sub(r'\\', '', text)  # Remove any remaining backslashes
    return text.strip()


# User input section
st.sidebar.header("Enter Your Financial Data")

monthly_income = st.sidebar.number_input("Monthly Income ($)", min_value=0, value=5500, step=100, key="income_input")

st.sidebar.subheader("Monthly Expenses")
st.sidebar.caption("Add your expenses below")

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        category = st.text_input("Category", placeholder="e.g., Rent, Groceries", key="category_input")
    with col2:
        amount = st.number_input("Amount ($)", min_value=0, value=0, step=10, key="amount_input")

    # Add expense button with unique key
    if st.button("Add Expense", key="add_expense_button") and category and amount > 0:
        st.session_state.expenses.append((category, amount))
        st.success(f"Added {category}: ${amount}")

    # Clear expenses button with unique key
    if st.session_state.expenses and st.button("Clear All Expenses", key="clear_expenses_button"):
        st.session_state.expenses = []
        st.rerun()

# Display current expenses
if st.session_state.expenses:
    st.sidebar.subheader("Current Expenses")
    total_expenses = 0
    for i, (cat, amt) in enumerate(st.session_state.expenses):
        st.sidebar.write(f"- {cat}: ${amt}")
        total_expenses += amt

    st.sidebar.metric("Total Monthly Expenses", f"${total_expenses}")
    st.sidebar.metric("Remaining After Expenses", f"${monthly_income - total_expenses}")

# NEW: User Scenarios Section
st.sidebar.header("📈 Future Scenarios")

# Option A: User-Driven Changes
st.sidebar.subheader("Expected Changes")
income_change = st.sidebar.number_input("Monthly Income Change ($)", value=0, step=50,
                                        help="Expected change in monthly income (positive for increase, negative for decrease)")
expense_change = st.sidebar.number_input("Monthly Expense Change ($)", value=0, step=25,
                                         help="Expected change in total expenses (positive for increase, negative for decrease)")

# Option C: Goal-Based Projections
st.sidebar.subheader("🎯 Financial Goals")
goal_type = st.sidebar.selectbox(
    "What's your main financial goal?",
    ["No specific goal", "Save specific amount", "Reach target savings rate", "Reduce expenses"]
)

goal_details = ""
if goal_type == "Save specific amount":
    target_amount = st.sidebar.number_input("Target Savings ($)", min_value=100, value=1000, step=100)
    timeline = st.sidebar.slider("Timeline (months)", 1, 12, 3)
    goal_details = f"Save ${target_amount} in {timeline} months"
elif goal_type == "Reach target savings rate":
    target_rate = st.sidebar.slider("Target Savings Rate (%)", 5, 50, 20)
    goal_details = f"Reach {target_rate}% savings rate"
elif goal_type == "Reduce expenses":
    reduction_target = st.sidebar.slider("Reduce expenses by (%)", 5, 50, 10)
    goal_details = f"Reduce expenses by {reduction_target}%"

try:
    # Single analyze button with conditional logic
    if st.button("Analyze My Finances", key="analyze_button"):
        if st.session_state.expenses:
            # Build user data string
            user_data = f"Monthly Income: {monthly_income}\nExpenses:\n"
            for category, amount in st.session_state.expenses:
                user_data += f"- {category}: {amount}\n"

            # NEW: Add scenario information to the prompt
            scenario_info = f"""

            USER SCENARIOS:
            - Income Change: ${income_change} per month
            - Expense Change: ${expense_change} per month
            - Financial Goal: {goal_type} - {goal_details if goal_type != "No specific goal" else "None"}
            """

            user_data += scenario_info

            # Combine prompts
            full_prompt = system_prompt + "\n\nPlease analyze the following financial data:\n" + user_data

            # Generate response
            with st.spinner("Analyzing your finances..."):
                response = client.models.generate_content(
                    model="gemma-3n-e4b-it",
                    contents=full_prompt
                )

            # Clean the response text
            cleaned_text = clean_latex_text(response.text)

            # Display results
            st.markdown("## Financial Analysis Results")
            st.markdown(cleaned_text)

            # Then create visualizations
            st.markdown("## Visualizations")

            # Create a single figure with subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

            # Plot 1: Expense Breakdown (Bar Chart)
            categories = [cat for cat, amt in st.session_state.expenses]
            amounts = [amt for cat, amt in st.session_state.expenses]
            ax1.bar(categories, amounts, color='skyblue')
            ax1.set_title('Expense Breakdown by Category')
            ax1.set_ylabel('Amount ($)')
            ax1.tick_params(axis='x', rotation=45)

            # Plot 2: Expense Distribution (Pie Chart)
            ax2.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Expense Distribution')

            # Display the combined figure
            st.pyplot(fig)
            plt.close(fig)  # Important: close the figure to free memory

            # NEW: Trend Projection Chart
            if income_change != 0 or expense_change != 0 or goal_type != "No specific goal":
                st.markdown("## Future Projection Trend")

                # Create projection data
                months = ['Current', 'Next Month', 'Month +2', 'Month +3']
                current_income = monthly_income
                current_expenses = total_expenses

                # Calculate projections with changes
                projected_income = [current_income]
                projected_expenses = [current_expenses]

                for i in range(3):
                    projected_income.append(current_income + income_change)
                    projected_expenses.append(current_expenses + expense_change)

                projected_net = [inc - exp for inc, exp in zip(projected_income, projected_expenses)]

                # Create trend chart
                fig2, ax3 = plt.subplots(figsize=(10, 6))
                ax3.plot(months, projected_income, label='Income', marker='o', linewidth=2)
                ax3.plot(months, projected_expenses, label='Expenses', marker='s', linewidth=2)
                ax3.plot(months, projected_net, label='Net', marker='^', linewidth=2, linestyle='--')
                ax3.set_title('3-Month Financial Projection')
                ax3.set_ylabel('Amount ($)')
                ax3.legend()
                ax3.grid(True, alpha=0.3)

                st.pyplot(fig2)
                plt.close(fig2)

            # Debug info (optional)
            with st.expander("Debug: View generated prompt"):
                st.code(full_prompt)
        else:
            st.warning("Please add at least one expense to analyze.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")