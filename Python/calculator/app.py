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
    table_data = []
    total_contributions = 0  # Initialize total_contributions

    if request.method == 'POST':
        initial_investment_input = request.form.get('initial_investment')
        if initial_investment_input:
            try:
                P = float(initial_investment_input)
            except ValueError:
                return render_template('index.html', result="Invalid initial investment amount.", table_data=table_data)
        else:
            P = 0

        monthly_contribution_input = request.form.get('monthly_contribution')
        if monthly_contribution_input:
            try:
                monthly_contribution = float(monthly_contribution_input)
                annual_contribution = monthly_contribution * 12
            except ValueError:
                return render_template('index.html', result="Invalid monthly contribution amount.", table_data=table_data)
        else:
            monthly_contribution = 0
            annual_contribution = 0

        annual_interest_rate_input = request.form.get('annual_interest_rate')
        if annual_interest_rate_input:
            try:
                r = float(annual_interest_rate_input) / 100
                if r <= 0:
                    return render_template('index.html', result="Annual interest rate must be greater than 0.", table_data=table_data)
            except ValueError:
                return render_template('index.html', result="Invalid annual interest rate.", table_data=table_data)
        else:
            r = 0

        try:
            compounding_frequency = int(request.form['compounding_frequency'])
        except ValueError:
            return render_template('index.html', result="Invalid compounding frequency.", table_data=table_data)

        try:
            t = int(request.form['investment_period'])
        except ValueError:
            return render_template('index.html', result="Invalid investment period.", table_data=table_data)

        inflation_rate_input = request.form.get('inflation_rate')
        if inflation_rate_input:
            try:
                inflation_rate = float(inflation_rate_input) / 100
            except ValueError:
                return render_template('index.html', result="Invalid inflation rate.", table_data=table_data)
        else:
            inflation_rate = 0

        # Calculate future value of initial investment and contributions
        FV_initial = P * (1 + r / compounding_frequency) ** (compounding_frequency * t)

        FV_contributions = 0
        for month in range(1, t * 12 + 1):
            FV_contributions += monthly_contribution * (1 + r / compounding_frequency) ** (compounding_frequency * (t - (month / 12)))

        final_sum = FV_initial + FV_contributions
        result = f"The future value of your investment is: ${final_sum:,.2f}"
        if inflation_rate > 0:
            result = f"The future value of your investment adjusted for inflation is: ${final_sum:,.2f}"

        # Calculate total contributions
        total_contributions = P + annual_contribution * t

        # Calculate total earned money
        total_earned = final_sum - total_contributions

        # Generate table data
        accumulated_value = P
        for year in range(1, t + 1):
            start_sum = accumulated_value
            for month in range(1, 13):
                accumulated_value = (accumulated_value + monthly_contribution) * (1 + r / compounding_frequency) ** (compounding_frequency / 12)
            interest_income = accumulated_value - start_sum - annual_contribution
            end_sum = accumulated_value
            table_data.append((year, f"${start_sum:,.2f}", f"${interest_income:,.2f}", f"${annual_contribution:,.2f}", f"${end_sum:,.2f}"))
        
        return render_template('index.html', result=result, table_data=table_data, total_contributions=f"${total_contributions:,.2f}", total_earned=f"${total_earned:,.2f}")

    return render_template('index.html', result="", table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)
