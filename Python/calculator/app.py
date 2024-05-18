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

        compounding_frequency = int(request.form['compounding_frequency'])

        if compounding_frequency == 0:
            try:
                t = int(request.form['investment_period'])
            except ValueError:
                return render_template('index.html', result="Invalid investment period.")
                
            FV_real = P + (annual_contribution * t)
            inflation_rate = 0  # Set inflation_rate to 0 when there's no reinvestment
        else:
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

            real_interest_rate = (1 + r) / (1 + inflation_rate) - 1
            FV_real = P * (1 + real_interest_rate / compounding_frequency)**(compounding_frequency * t) + (annual_contribution * ((1 + real_interest_rate / compounding_frequency)**(compounding_frequency * t) - 1) / (real_interest_rate / compounding_frequency))

        result = f"The future value of your investment is: ${FV_real:,.2f}"
        if inflation_rate > 0:
            result = f"The future value of your investment adjusted for inflation is: ${FV_real:,.2f}"

        return render_template('index.html', result=result)

    return render_template('index.html', result="")

if __name__ == '__main__':
    app.run(debug=True)
