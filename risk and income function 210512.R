
d=20 #input days
h=12 #input working hours
rate=1.1 #input expected and safe ratio
a=-19 #to calculate order safe 
      #orders_safe<- floor( a + b/(1 + exp(-x+1)))
b=54 #to calculate order safe
      #orders_safe<- floor( a + b/(1 + exp(-x+1)))
risk_rate_safe<-0.001 #risk for each order under safe 
c=1000 #to calculate the increasing of risk over safe  
      #risk_rate_dangerous<-risk_rate_safe-(time_expected - time_safe)/c
orders_starting = 10 #starting orders for orlando
income_each_basic=8 #basic income for each order
income_overtime=50 #to adjust the punishment for overtiming under expected total_income<-income_each_basic*x -(income_overtime ^ ( time_actual - time_expected))* x/10
income_d<-20 # to adjust the increase speed of income-order function over expected  total_income<-income_each_basic*tanh((x - y) / income_d)+y*income_each_basic


# rate=seq(0,2,length= 100)
orders_adding= 0 #input numbers of adding orders

#safe order numbers and time

funx_orders_safe<-function(x){
  orders_safe<- floor( a + b/(1 + exp(-x+1)))
  print(orders_safe)
  return(orders_safe)
}

orders_safe<-funx_orders_safe(d)  

time_safe<-h/orders_safe

#expected order numbers and time by the system

funx_orders_expected<-function(x){
  orders_expected<- ceiling(x*rate)
  print(orders_expected)
  return(orders_expected)
}
orders_expected<-funx_orders_expected(orders_safe)

time_expected<-h/orders_expected

## risk_rate

# here shows the rate of risk for each order


risk_rate_dangerous<-risk_rate_safe-(time_expected - time_safe)/c

# actual risk




orders_actual<-orders_starting + orders_adding 
time_actual<- h / orders_actual
#plot(x,orders_actual)
#plot(x,time_actual)

# risk_rate_actual<-ifelse(12/(10+x)>time_safe, 
#                          risk_rate_safe,
#                          risk_rate_dangerous )

funx_risk_rate_actual<-function(x){
  if(x>time_safe)
  {
    risk_rate_actual<-risk_rate_safe
  }else{
    risk_rate_actual<-risk_rate_dangerous
  }
  return(risk_rate_actual)
}
risk_rate_actual<-funx_risk_rate_actual(time_actual)

# plot(x,risk_rate_actual)
risk_actual<- (1 - (1 - risk_rate_actual)^orders_actual)*100
# plot(x,risk_actual,type = 'l')

#actual incomes
funx_income<-function(x,y){
  if(x<y){
    total_income<-income_each_basic*x -(income_overtime ^ ( time_actual - time_expected))* x/10
  }else{
    total_income<-income_each_basic*tanh((x - y) / income_d)+y*income_each_basic
  }
  return(total_income)
}

income_total<-funx_income(orders_actual,orders_expected)
income_each_orders<-income_total/orders_actual

print("actual orders/risk/ total income/ each order incomes =")
print(orders_actual)
print(risk_actual)
print(income_total)
print(income_each_orders)
# 
# income_actual<-ifelse(orders_actual > orders_expected,
#                       income_each_basic * tanh((orders_actual - orders_expected) / income_d) + orders_expected*income_each_basic,
#                       income_each_basic*orders_expected -(income_overtime ^ ( time_actual - time_expected))* orders_actual/10
#                       )

 plot(rate,income_actual,type = 'l')
# plot(x,income_actual/x, type = 'l',ylim =range (0:2))
