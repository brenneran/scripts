from flask import Flask, render_template, request

app = Flask(__name__)

# Add cache control headers to prevent caching
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods=['GET', 'POST'])
def pension_calculator():
    if request.method == 'POST':
        initial_investment_input = request.form.get('initial_investment')
        if initial_investment_input:
            try:
                P = float(initial_investment_input)
            except ValueError:
                return render_template('index.html', result="Invalid initial investment amount.")
        else:
            P = 0

        monthly_contribution_input = request.form.get('monthly_contribution')
        if monthly_contribution_input:
            try:
                monthly_contribution = float(monthly_contribution_input)
                annual_contribution = monthly_contribution * 12
            except ValueError:
                return render_template('index.html', result="Invalid monthly contribution amount.")
        else:
            monthly_contribution = 0
            annual_contribution = 0

        annual_interest_rate_input = request.form.get('annual_interest_rate')
        if annual_interest_rate_input:
            try:
                r = float(annual_interest_rate_input) / 100
                if r <= 0:
                    return render_template('index.html', result="Annual interest rate must be greater than 0.")
            except ValueError:
                return render_template('index.html', result="Invalid annual interest rate.")
        else:
            r = 0

        try:
            t = int(request.form['investment_period'])
        except ValueError:
            return render_template('index.html', result="Invalid investment period.")

        inflation_rate_input = request.form.get('inflation_rate')
        if inflation_rate_input:
            try:
                inflation_rate = float(inflation_rate_input) / 100
            except ValueError:
                return render_template('index.html', result="Invalid inflation rate.")
        else:
            inflation_rate = 0

        compounding_frequency_input = request.form.get('compounding_frequency')
        if compounding_frequency_input:
            compounding_frequency = int(compounding_frequency_input)
        else:
            compounding_frequency = 1  # Default to Once a year if not provided

        if compounding_frequency == 0:  # No reinvest
            real_interest_rate = r
        else:
            real_interest_rate = (1 + r / compounding_frequency) ** compounding_frequency - 1

        # Calculate future value considering both initial investment and annual contributions
        future_value = 0
        year_data = []
        current_sum = P

        for year in range(1, t + 1):
            interest = current_sum * real_interest_rate
            current_sum += interest + annual_contribution
            year_data.append({
                "year": year,
                "started_sum": f"${P:,.2f}",
                "percentage_income_invested": f"${interest:,.2f}",
                "invested": f"${annual_contribution:,.2f}",
                "final_sum": f"${current_sum:,.2f}"
            })

        future_value = current_sum

        total_contributions = P + (annual_contribution * t)

        result = (f"The future value of your investment is: ${future_value:,.2f}.<br>"
                  f"Total contributions over {t} years: ${total_contributions:,.2f}.")

        return render_template('index.html', result=result, data=year_data)

    return render_template('index.html', result="")

if __name__ == '__main__':
    app.run(debug=True)
