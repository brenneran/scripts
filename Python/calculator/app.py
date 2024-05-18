from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def pension_calculator():
    if request.method == 'POST':
        try:
            P = float(request.form['initial_investment'])
        except ValueError:
            return render_template('index.html', result="Invalid initial investment amount.")

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

        try:
            r = float(request.form['annual_interest_rate']) / 100
        except ValueError:
            return render_template('index.html', result="Invalid annual interest rate.")

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
