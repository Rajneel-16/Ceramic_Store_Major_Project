class Calculate():
    def __init__(self,length,breadth,price,light=0,dark=0,high=0):
        self.lenght=length
        self.breadth=breadth
        self.light=light
        self.dark=dark
        self.high=high
        self.price=price
    
    def  number_of_box(self,light,dark,high,price):
        Area = self.lenght*self.breadth
        Bands = light + dark + high
        Perbands = Area/Bands
        varient = {"light":{"box":light,"price":price},"dark":{"box":dark,"price":price},"high":{"box":high,"price":price}}
        for keys,value in varient.items():
            if value["box"]==0:
                varient[keys]["box"]=0
                varient[keys]["price"]=0
            else:
                total_box=int(Perbands*value["box"])
                varient[keys]["box"]=total_box
                amount = total_box*int(self.price)
                varient[keys]["price"]=amount
        return varient
    