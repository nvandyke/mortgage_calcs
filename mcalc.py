import numpy as np
import matplotlib.pyplot as plt
import itertools
import os
import sys
#constants
property_value = 470000
term_loan = 30
size = 5
debug = 0
plot = 0

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

def make_plot(x,x_name,y,y_name,z):
    x_, y_ = np.meshgrid(x,y)
    #print(x_)
    #print(y_)
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(10)
    #print(z)
    CS = ax.contour(x_, y_, z)
    ax.clabel(CS,inline=True,fontsize=10)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    return ax

def calc_single_scenario(d,irl,iri,ti,lvp):
    #intermediate steps
    house_price = property_value-d
    bank_loan_value = house_price*lvp
    inlaw_loan_value = house_price*(1-lvp)
    
    #create loan objects
    bank_loan = loan(property_value,bank_loan_value,irl,term_loan)
    
    inlaw_loan = loan(property_value,inlaw_loan_value,iri,ti)
    
    if debug:
        print(f'discount {d}')
        print(f'int loan {irl}')
        print(f'int inlaw {iri}')
        print(f'term inlaw {ti}')
        print(f'loan pct {lvp}')
        print()
        print(f'bank {bank_loan_value}')
        print(f'inlaw {inlaw_loan_value}')
        print(f'total borrowed {bank_loan_value+inlaw_loan_value}')
        print()
        print(f'bank monthly {bank_loan.monthly_due()}')
        print(f'inlaw monthly {inlaw_loan.monthly_loan_payback()}')
        print(f'total {bank_loan.monthly_due()+inlaw_loan.monthly_loan_payback()}')
        print()
        print()
    return bank_loan.monthly_due()+inlaw_loan.monthly_loan_payback()

def run_mega_analysis():
    global debug
    
    
    #initialization
    discount = np.linspace(0,100000,size)
    interest_rate_loan = np.linspace(.06,0.085,size)
    interest_rate_inlaw = np.linspace(.01,0.04,size)
    term_inlaw = np.linspace(5,20,size)
    loan_value_pct = np.linspace(.5,1,size)
    parameters = {"Discount": [discount,0], "Loan Interest Rate": [interest_rate_loan,1], "In-Law Interest Rate": [interest_rate_inlaw,2], "In-Law Term": [term_inlaw,3], "Bank Loan Percentage": [loan_value_pct,4]}
    
    payments = np.ndarray((size,size,size,size,size))
    
    #looping
    for i, d in enumerate(discount):
        for j, irl in enumerate(interest_rate_loan):
            for k, iri in enumerate(interest_rate_inlaw):
                for l, ti in enumerate(term_inlaw):
                    for m, lvp in enumerate(loan_value_pct):
                        
                        #calc payment
                        payments[i,j,k,l,m] = calc_single_scenario(d,irl,iri,ti,lvp)
                        #os.system("pause")
    print(f'min value {payments.min().min().min().min().min()}')
    location = np.where(payments==payments.min().min().min().min().min())
    print(int(location[0].item()))
    debug = 1
    calc_single_scenario(discount[location[0].item()],
                         interest_rate_loan[location[1].item()],
                         interest_rate_inlaw[location[2].item()],
                         term_inlaw[location[3].item()],
                         loan_value_pct[location[4].item()])
    if not plot:
        return
    #get all pair combinations of the parameters
    all_pairs = list(itertools.combinations(parameters,2))
    
    for pair in all_pairs:
        for a in range(size):
            for b in range(size):
                for c in range(size):
                    
                    index_1 = parameters[pair[0]][1]
                    index_2 = parameters[pair[1]][1]
                    
                    #print(pair)
                    #print(parameters[pair[0]])
                    #print(payments[:,:,a,b,c].reshape(size,size))
                    
                    #print(a,b,c)
                    #figure out what slice
                    slices = [-1,-1,-1,-1,-1]
                    slices[index_1] = slice(None)
                    slices[index_2] = slice(None)
                    
                    slices[slices.index(-1)] = a
                    slices[slices.index(-1)] = b
                    slices[slices.index(-1)] = c
                    #print(slices)
                    
                    #print(payments[slices].reshape(size,size))
                    ax = make_plot(parameters[pair[0]][0],pair[0],parameters[pair[1]][0],pair[1],np.transpose(payments[slices].reshape(size,size)))
                    constants_list = [x for x in list(parameters.keys()) if x not in pair]
                    #print(constants_list)
                    constants_string = f'{constants_list[0]} = {parameters[constants_list[0]][0][a]}, {constants_list[1]} = {parameters[constants_list[1]][0][b]}, {constants_list[2]} = {parameters[constants_list[2]][0][c]}'
                    print(constants_string)
                    ax.set_title(constants_string)
                    #plt.show()
                    plt.savefig(f'a\\{constants_string}.png')

if __name__ == "__main__":
    run_mega_analysis()