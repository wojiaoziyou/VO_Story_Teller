library(ggplot2)

##create number

number<-floor(runif(20,0,10000))
number[2]<-0113 #give number for orlando

##create days frame

days_random<-rnorm(20,mean = 20,sd = 10)
days_random[2]<-1 #give day for orlando
days_7<-abs(floor(days_random ))
days_7

days_frame<-data.frame(number, days_7)

for (i in 1:6){
  days_frame[,ncol(days_frame)+1]<-days_frame[,2]-i
  names(days_frame)[ncol(days_frame)]<-paste0("day_",7-i)
}

days_frame[days_frame<0]<- 0 #remove days less than 1
days_frame
col_names<-colnames(days_frame)

##create order means
orders_mean<-floor( (-19) + 54/(1 + exp((-days_frame+1)/4)))
orders_mean[,1]<-days_frame[,1]
orders_mean[orders_mean<5]<-0
orders_mean

##create order rnorm frame
?data.frame()
orders_rnorm<-data.frame(number)

for(i in 1:7){
  orders_rnorm[,ncol(orders_rnorm)+1]<-floor(rnorm(20,orders_mean[,i+1],5))
}
colnames(orders_rnorm)<-col_names
orders_rnorm

for(x in 1:20){
  for(y in 1:8){
    if(days_frame[x,y] == 0){
      orders_rnorm[x,y]<-0
    }else{
      orders_rnorm[x,y]<-orders_rnorm[x,y]
    }
  }
  
} #remove the order for days less than 1



orders_rnorm[2,2]<-4 #give the order number for orlando
orders_rnorm


##create the order frame with days and orders
orders<-data.frame(number)
orders

for (i in 2:17){
  if (i %% 2 == 0){
    orders[,i]<-data.frame(days_frame[,i/2])
  }else{
    orders[,i]<-data.frame(orders_rnorm[,floor(i/2)])
  }
} 
orders<-orders[-c(2,3)] #remove extra number col
orders

for (i in 1:15){
  if(i==1){
    names(orders)[i]<-'number'
  }else if(i%%2 ==0){
    names(orders)[i]<-paste0("day_",8-i/2)
  }else{
    names(orders)[i]<-paste0("orders",8-floor(i/2))
  }
  
} #name the cols

orders

##create the plot for the chapter 1

plot_day_7<-data.frame(as.character(orders$number),orders$orders7)
colnames(plot_day_7)<-c('number','orders')
#label the min and max and give the color factor
order_max<-max(plot_day_7$orders)
order_min<-min(plot_day_7$orders)
for (i in 1:20){
  if (plot_day_7[i,2]== order_min){
    plot_day_7[i,3]<- 'red'
  }else if(plot_day_7[i,2]==order_max){
    plot_day_7[i,3]<-'blue'
  }else{
    plot_day_7[i,3]<-'black'
  }
} 
colnames(plot_day_7)[3]<-'color'
plot_day_7
#create the plot
ggplot(data = plot_day_7,mapping = aes(x=number, y = orders))+
  geom_bar(stat = 'identity', fill= plot_day_7$color)+
  labs(x="Numbers",y="Orders")+
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background=element_rect(colour = "black",size = 1,fill = "white"),
        axis.line = element_line(color = "black"),
        axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5),
        legend.position = "none")+
  geom_text(mapping = aes(label = number), size = 5, colour = 'orange', vjust = 0.5,hjust=0.5,angle=45)

##create the plot for each delivery guys

orders_t<-as.data.frame(t(orders_rnorm))
colnames(orders_t)<-orders_t[1,]  
orders_t<-orders_t[-1,]
orders_t[,ncol(orders_t)+1]<-7:1
colnames(orders_t)[ncol(orders_t)]<-'days'

days_frame_t<-as.data.frame(t(days_frame))
colnames(days_frame_t)<-days_frame_t[1,]  
days_frame_t<-days_frame_t[-1,]


a<-15 ##input the delivery guy 

plot_a<-data_frame(orders_t$days,orders_t[,a],days_frame_t[,a])
colnames(plot_a)<-c('days','orders','days_since_work')
plot_a
ggplot(data = plot_a,mapping = aes(x=days, y = orders))+
  geom_bar(stat = 'identity', fill= 'blue')+
  labs(y="Orders")+
  ylim(0,60)+
  scale_x_continuous('Days', 
                     breaks = seq(1,7,1),  
                     trans = 'reverse')+
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background=element_rect(colour = "black",size = 1,fill = "white"),
        axis.line = element_line(color = "black"),
        axis.text.x = element_text( hjust = 0.5, vjust = 0.5,size = 15),
        legend.position = "none")+
  geom_text(mapping = aes(label = days_since_work), size = 5, colour = 'red',hjust=-0.5)+
  coord_flip() 

