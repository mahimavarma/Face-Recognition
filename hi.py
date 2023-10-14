import numpy as np

# Sample data: Income and Expenses
income = np.array([50000, 60000, 70000, 80000, 90000])
expenses = np.array([20000, 25000, 30000, 35000, 40000])

# Define a function to calculate taxable income based on income and expenses
def calculate_taxable_income(income, expenses):
    return income - expenses

# Define a function to calculate tax based on taxable income
def calculate_tax(taxable_income, tax_rate):
    return taxable_income * tax_rate

# Gradient descent to find optimal tax rate
def gradient_descent(income, expenses, target_tax, learning_rate=0.01, epochs=1000):
    tax_rate = 0.1  # Initial guess for tax rate
    for _ in range(epochs):
        taxable_income = calculate_taxable_income(income, expenses)
        tax = calculate_tax(taxable_income, tax_rate)
        
        # Calculate the gradient of the loss with respect to the tax rate
        gradient = np.sum(2 * (tax - target_tax) * taxable_income)
        
        # Update tax rate using gradient descent
        tax_rate -= learning_rate * gradient
        
    return tax_rate

# Target tax to minimize
target_tax = 15000  # You can set your desired tax liability here

# Find the optimal tax rate
optimal_tax_rate = gradient_descent(income, expenses, target_tax)

print(f"Optimal Tax Rate: {optimal_tax_rate * 100}%")