import numpy as np

class loan:
    def __init__(self, property_value, loan_amount, interest_rate, term_years):
        self.property_value = property_value
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.term_months = term_years*12
    
    def monthly_property_taxes(self):
        return (self.property_value*.01)/12
    
    def monthly_pmi(self):
        return (self.loan_amount*.01)/12
    
    def monthly_loan_payback(self):
        monthly_interest = self.interest_rate/12
        intermediate_step = np.power(1+monthly_interest, self.term_months)
        return self.loan_amount*monthly_interest*intermediate_step/(intermediate_step-1)
        
    def monthly_due(self):
        return self.monthly_loan_payback() + self.monthly_pmi() + self.monthly_property_taxes()
        
        
if __name__ == "__main__":
    a = loan(100000,100000,.01,30)
    print(a.monthly_loan_payback())
    print(a.monthly_pmi())
    print(a.monthly_property_taxes())
    print(a.monthly_due())