library(ggplot2)
library(reshape2)
library(ggthemes)


##create number

number<-floor(runif(20,1000,10000))
number[2]<-113 #give number for orlando

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

days_frame[days_frame < 1]<- 0 #remove days less than 1
days_frame
col_names<-colnames(days_frame)

##create order means
orders_mean<-floor( (-19) + 54/(1 + exp((-days_frame+1)/4)))
orders_mean[,1]<-days_frame[,1]
orders_mean[orders_mean<5]<-0
orders_mean

##create order rnorm frame
orders_rnorm<-data.frame(number)

for(i in 1:7){
  orders_rnorm[,ncol(orders_rnorm)+1]<-floor(rnorm(20,orders_mean[,i+1],5))
}
colnames(orders_rnorm)<-colnames(days_frame)
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
orders_rnorm


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


for (i in 1:15){
  if(i==1){
    names(orders)[i]<-'number'
  }else if(i%%2 ==0){
    names(orders)[i]<-paste0("day_",8-i/2)
  }else{
    names(orders)[i]<-paste0("orders_",8-floor(i/2))
  }
  
} #name the cols

orders

##create the plot for the chapter 2

plot_day_7<-data.frame(orders$number,orders$orders_7)
colnames(plot_day_7)<-c('number','orders')
#label the min and max and give the color factor
plot_day_7_ord<-plot_day_7
plot_day_7_ord
ord<-order(plot_day_7_ord$orders)
plot_day_7_ord<-plot_day_7_ord[ord,]
plot_day_7_ord
n<-3
min_num<-plot_day_7_ord$number[1:n]
min_num
max_num<-plot_day_7_ord$number[(21-n):20]
max_num

for (i in 1:20){
  if (plot_day_7[i,1] %in% min_num){
    plot_day_7[i,3]<- 'red'
  }else if(plot_day_7[i,1] %in% max_num){
    plot_day_7[i,3]<-'blue'
  }else{
    plot_day_7[i,3]<-'black'
  }
}

colnames(plot_day_7)[3]<-'color'
plot_day_7

#create the plot
ggplot(data = plot_day_7,mapping = aes(x=as.character(number), y = orders))+
  geom_bar(stat = 'identity', fill= plot_day_7$color)+
  labs(x="Numbers",y="Orders")+
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background=element_rect(colour = "black",size = 1,fill = "white"),
        axis.line = element_line(color = "black"),
        axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5, size = 15),
        axis.text.y = element_text( size = 15),
        legend.position = "none")+
  geom_text(mapping = aes(label = orders), size = 5, colour = 'orange', vjust =-0.5,hjust=0.5)

##create the plot for each delivery guys

orders_t<-as.data.frame(t(orders_rnorm))
colnames(orders_t)<-orders_t[1,]  
orders_t<-orders_t[-1,]
orders_t[,ncol(orders_t)+1]<-7:1
colnames(orders_t)[ncol(orders_t)]<-'days'

days_frame_t<-as.data.frame(t(days_frame))
colnames(days_frame_t)<-days_frame_t[1,]  
days_frame_t<-days_frame_t[-1,]


num_check<-4271 ##input the delivery guy 

a<-which(orders_rnorm$number == num_check)

dataframe_a<-data.frame(orders_t$days,orders_t[,a],days_frame_t[,a])
colnames(dataframe_a)<-c('days','orders','days_since_work')
overtime_rate<-rnorm(7,0.1,0.001)
dataframe_a<-cbind(dataframe_a,overtime_rate)
positive_feedback<- (1 - overtime_rate)*rnorm(1,0.8,0.0001)
positive_feedback

dataframe_a<-cbind(dataframe_a,positive_feedback)
dataframe_a$overtime_orders<-ceiling(dataframe_a$orders*dataframe_a$overtime_rate)
dataframe_a$positive_orders<-ceiling(dataframe_a$orders*dataframe_a$positive_feedback)

dataframe_a$other_orders<-dataframe_a$orders - dataframe_a$overtime_orders - dataframe_a$positive_orders

dataframe_a_orders<-data.frame(dataframe_a$days_since_work,dataframe_a$overtime_orders,dataframe_a$other_orders,dataframe_a$positive_orders)
colnames(dataframe_a_orders)<-c('days','overtime_orders',"other_orders","positive_orders")

plot_a<-melt(dataframe_a_orders,id.vars = 'days',variable.name =  'various',value.name="orders")
plot_a


ggplot()+
  geom_bar(data = plot_a,mapping = aes(x=days, y = orders,fill=factor(various)),stat = 'identity',position = 'stack')+
  labs(y="Orders" )+
  ggtitle(paste0("Orders taken by ",colnames(orders_t)[a]," in last 7 days"))+
  ylim(0,60)+
  scale_x_continuous('Days Since Joining',
                     breaks = seq(max(plot_a$days)-7,max(plot_a$days),1))+
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background=element_rect(colour = "black",size = 1,fill = "white"),
        axis.line = element_line(color = "black"),
        axis.text.x = element_text( hjust = 0.5, vjust = 0.5,size = 15),
        axis.text.y = element_text( size = 15),
        plot.title = element_text(size = 15))+
  geom_text(data=dataframe_a,
              mapping = aes(x=days_since_work, y = orders,label = orders), size = 5, colour = 'black',vjust = -1)+
  geom_text(data=dataframe_a,
            mapping = aes(x=days_since_work, y = positive_orders,label = positive_orders), size = 5, colour = 'black',vjust = 1)+
geom_text(data=dataframe_a,
          mapping = aes(x=days_since_work, y = positive_orders + other_orders,label = other_orders), size = 5, colour = 'black', vjust = 0.5 )

# ggplot()+
#   geom_line(data = plot_a,aes(x=days, y = orders, colour = 'orders'),stat = 'identity')+
#   geom_line(data = plot_a,aes(x=days, y = (1-overtime_rate)*50, colour = 'overtime rate'),stat = 'identity')+
#   geom_line(data = plot_a,aes(x=days, y = positive_feedback*50, colour = 'positive feedback'),stat = 'identity')+
#   labs(y="Orders" )+
#   ggtitle(paste0("Orders taken by ",colnames(orders_t)[a]," in last 7 days"))+
#   scale_y_continuous('Orders', 
#                      breaks = seq(0,70,10),
#                      limits = c(0,55))+
#   scale_x_continuous('Days', 
#                      breaks = seq(1,7,1),
#                      trans = 'reverse')+
#   theme(panel.grid.major = element_blank(),
#         panel.grid.minor = element_blank(),
#         panel.background=element_rect(colour = "black",size = 1,fill = "white"),
#         axis.line = element_line(color = "black"),
#         axis.text.x = element_text( hjust = 0.5, vjust = 0.5,size = 15),
#         axis.text.y = element_text( size = 15),
#         plot.title = element_text(size = 15))+
#   geom_text(data= plot_a,mapping = aes(x=days, y = orders,label = orders), size = 5, colour = 'red',hjust=-0.5)

