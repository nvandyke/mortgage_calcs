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
        
    def monthly_insurance(self):
        return (self.property_value*.0035)/12
    
    def monthly_loan_payback(self):
        monthly_interest = self.interest_rate/12
        intermediate_step = np.power(1+monthly_interest, self.term_months)
        return self.loan_amount*monthly_interest*intermediate_step/(intermediate_step-1)
        
    def monthly_due(self):
        return self.monthly_loan_payback()   + \
               self.monthly_pmi()            + \
               self.monthly_property_taxes() + \
               self.monthly_insurance()
        
def generate_data():
    
    #constants
    property_value = 470000
    term_loan = 30
    size = 5
    
    #initialization
    discount = np.linspace(0,100000,size)
    interest_rate_loan = np.linspace(.01,0.1,size)
    interest_rate_inlaw = np.linspace(.01,0.1,size)
    term_inlaw = np.linspace(1,30,size)
    loan_value_pct = np.linspace(.5,1,size)
    payments = np.ndarray((size,size,size,size,size))
    inlaw_value_pct = property_value-loan_value_pct
    
    #looping
    for i, d in enumerate(discount):
        for j, irl in enumerate(interest_rate_loan):
            for k, iri in enumerate(interest_rate_inlaw):
                for l, ti in enumerate(term_inlaw):
                    for m, lvp in enumerate(loan_value_pct):
                        
                        #intermediate steps
                        house_price = property_value-d
                        bank_loan_value = house_price*lvp
                        inlaw_loan_value = house_price*(1-lvp)
                        
                        #create loan objects
                        bank_loan = loan(property_value,bank_loan_value,irl,term_loan)
                        
                        inlaw_loan = loan(property_value,inlaw_loan_value,iri,ti)
                        
                        #print(d)
                        #print(irl)
                        #print(iri)
                        #print(ti)
                        #print(lvp)
                        #print()
                        #print(bank_loan_value)
                        #print(inlaw_loan_value)
                        #print()
                        #print(bank_loan.monthly_due())
                        #print(inlaw_loan.monthly_loan_payback())
                        #print(bank_loan.monthly_due()+inlaw_loan.monthly_loan_payback())
                        #print()
                        #print()
                        
                        #storage
                        payments[i,j,k,l,m] = \
                            bank_loan.monthly_due()+inlaw_loan.monthly_loan_payback()
                            
    return payments
    
    
if __name__ == "__main__":
    payments = generate_data()
    print(payments)