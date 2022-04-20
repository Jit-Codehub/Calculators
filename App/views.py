import math
from xdrlib import ConversionError
# from termios import B0
from django.shortcuts import render
import numpy as np
import scipy
import scipy.linalg

#FUNCTION FOR CONVERTING TAGS
def add_tags(tag, word):
	return "<%s>%s</%s>" % (tag, word, tag)

#FUNCTION FOR UNIT CONVERSION
def convert2(val,u1,num):
  if val=="volt":
    if u1=='V':
      return float(num),""
    elif u1=="mV":
      return float(num/1000),"/1000"
    elif u1=="kV":
      return float(num*1000),"*1000"
    elif u1=="MV":
      return float(num*1000000),"* 10"+add_tags("sup",6)
    else:
      return num,""       
  
  elif val=="res":
    if u1=="Ω":
     return float(num),""
    elif u1=="mΩ":
      return float(num/1000),"/1000"
    elif u1=="kΩ":
      return float(num*1000),"*1000"
    elif u1=="MΩ":
      return float(num*1000000),"* 10 "+add_tags("sup",6)  
    else:
      return 1,"";  

  elif val=="curr":
    if u1=='A':
     return float(num),""
    elif u1=="mA":
      return float(num/1000),"/1000"
    elif u1=="µA":
      return float(num/1000000),"/( 10"+add_tags("sup",6)+")"    
    else:
      return 1,"";  

  elif val=="mass":
    if u1=='g':
        return num,"/1000"
    elif u1=='kg':
        return num*1000,"" 
    elif u1=='mg':
        return num/1000,"/1000000"      
    elif u1=='µg':
        return num/(10**6),"/( 10 "+add_tags("sup",9)+")"
    elif u1=='dg':
        return num/10,"/10000"
    elif u1=='t':
        return num*(10**6),"*1000"
    elif u1=='oz':
        return num*28.34,"*0.02834"
    elif u1=='lb':
        return num*453.3,"*0.4533"
    elif u1=='me':
      return num*9.10938356*(10**-28),"* 9.109 * 10" + add_tags("sup",-31)
    elif u1=='mp':
      return num*1.672621898*(10**-24),"* 1.67 * 10" + add_tags("sup",-27)
    elif u1=='mn':
      return num*1.672621898*(10**-24),"* 1.67 * 10" + add_tags("sup",-27)
    elif u1=='u':
      return num*1.67*(10**-24),"* 1.67 * 10" + add_tags("sup",-27)
    elif u1=='e':
      return num*9.1094e-28,"* 9.1 * 10" + add_tags("sup",-31)
    else:
      return num,"" 
  
  
  elif val=="len":
    if u1=='m':
        return num,""
    elif u1=='nm':
        return num/(10**9),"* 10 " + add_tags("sup",-9) 
    elif u1=='pm':
        return num/(10**12),"* 10 " + add_tags("sup",-12)      
    elif u1=='µm':
        return num/(10**6),"* 10 " + add_tags("sup",-6)
    elif u1=='mm':
        return num/1000,"* 10" + add_tags("sup",-3)
    elif u1=='ft':
        return num*0.304,"* 0.304"
    elif u1=='in':
        return num*0.025,"* 0.025 "
    elif u1=='km':
       return num*1000 ,"* 1000"   
    elif u1=='cm':
       return num/100 ,"/100"   
    else:
      return num,""

  elif val=="charge":

    if u1=='C':
     return float(num),""
    elif u1=="mC":
      return float(num/1000),"/1000"
    elif u1=="μC":
      return float(num/1000000),"* 10" + add_tags("sup",-6)  
    elif u1=="nC":
      return float(num/(10**9)),"* 10" + add_tags("sup",-9)
    elif u1=="PC":
      return float(num/(10**12)),"* 10" + add_tags("sup",-12)
    elif u1=='e':
      return num*1.60218e-19,"* 1.602 "+ add_tags("sup",-19)    
    else:
      return num*2,""    

  elif val=="force":
    if u1=='N':
        return num,""
    elif u1=='kN':
        return num*1000,"* 1000"
    elif u1=='mN':
        return num/1000,"* 10" + add_tags("sup",-3)      
    elif u1=='μN':
        return num/(10**6),"* 10" + add_tags("sup",-6)
    elif u1=='d':
        return num/(10**5),"* 10" + add_tags("sup",-5)
    else:
      return num,""    
  
  elif val=="cap":
    if u1=='F':
        return num,""
    elif u1=='mF':
        return float(num/1000),"* 10 " + add_tags("sup",-3) 
    elif u1=='nF':
        return float(num/(10**9)),"* 10 " + add_tags("sup",-9)      
    elif u1=='µF':
        return float(num/(10**6)),"* 10 " + add_tags("sup",-6)
    else:
      return 1,""    

  elif val=="ind":
    if u1=='H':
        return num,""
    elif u1=='mH':
        return float(num/1000),"* 10 "+ add_tags("sup",-3) 
    elif u1=='nH':
        return float(num/(10**9)),"* 10 " + add_tags("sup",-9)      
    elif u1=='µH':
        return float(num/(10**6)),"* 10 " + add_tags("sup",-6)
    else:
      return 100,""       

  elif val=="freq":
    if u1=='Hz':
        return num,""
    elif u1=='mHz':
        return float(num/1000),"* 10 " + add_tags("sup",-3) 
    elif u1=='MHz':
        return float(num*(10**6)),"* 10 " + add_tags("sup",6)      
    elif u1=='kHz':
        return float(num*1000),"* 10 * " + add_tags("sup",3)
    else:
      return 1,""    

 
  elif val=="vel":
    if u1=='m/s':
        return num,""
    elif u1=='km/hr':
        return float(num*0.27)," * 0.27" 
    elif u1=='ft/s':
        return float(num*0.304),"* 0.304"      
    elif u1=='mph':
        return float(num*0.45)," * 0.45"
    else:
      return num,""              

  elif val=="temp":
    if u1=='°C':
        return num,""
    elif u1=='K':
        return num-273.15," -273.15"
    elif u1=='°F':
        return 5/9*(num-32),""      
    else:
      return 1,""              
    

  elif val=="time":
    if u1=="s":
      return num,""
    elif u1=="ms":
      return num/1000,"/1000"
    elif u1=="ns":
      return num/(10**9),"* 10 " + add_tags("sup",-9)
    elif u1=="ps":
      return num/(10**12),"* 10 " + add_tags("sup",-12)
    elif u1=='µs':
        return float(num/(10**6)),"* 10 " + add_tags("sup",-6)    
    elif u1=="min":
      return num*60,"*60"
    elif u1=="hr":
      return num*3600,"*3600"
    elif u1=="day":
      return num*86400,"*86400"
    elif u1=="week":
      return num*86400*7,"*86400*7"
    elif u1=="month":
      return num*2.628e+6,"* 2.628 * 10"+add_tags("sup",6) 
    elif u1=="year":
      return num*3.154e+7,"*3.154 * 10"+add_tags("sup",7)          
    else:
      return 1,""    
  
  elif val=="flow":
    if u1=="m/s":
      return num,""
    elif u1=="l/s":
      return num*0.01,"*0.01"
    elif u1=="cm/s":
      return num*(10**-6),"* 10" + add_tags("sup",-6)
    elif u1=="m/min":
      return num/60,"/ 60 "
    elif u1=="l/min":
      return num*0.01/60,"*0.01/60"
    elif u1=="cm/min":
      return num*(10**-6)/60,"* 10 "+ add_tags("sup",-6)+"/60"    
    else:
      return 1,""

  elif val=="energy":
    if u1=='J':
      return num,""
    elif u1=='kJ':
      return num*1000,"*1000"
    elif u1=='MJ':
      return num*(10**6),"*1000000"
    elif u1=="wh":
      return num*3600,"*3600"  
    elif u1=="kwh":
      return num*3.6e6,"*36000000"  
  
  elif val=="frequency":
    if u1=="per/second":
      return num,""
    elif u1=="per/min":
      return num/60,"/60"
    elif u1=="per/hour":
       return num/3600,"/3600"
    elif u1=="per/day":
       return num/86400,"/86400"   
    elif u1=="per/week":
      return num/(86400*7),"/( 86400*7 )"
    elif u1=="per/month":
      return num/2.628e+6,"/( 2.628 * 10"+add_tags("sup",6)+")" 
    elif u1=="per/year":
      return num/3.154e+7,"/ ( 3.154 * 10"+add_tags("sup",7)+")"          
  
  elif val=="pressure":
    if u1=="pa":
      return num,""
    elif u1=="mm":
       return num*133.32,"*133.32"
    elif u1=="atm":      
      return num*101325,"*101325"
    elif u1=="psi":
       return num*6894.76,"*6894.76"
    elif u1=="bar":
       return num*100000,"*100000"
    elif u1=="kpa":
       return num*1000,"*1000"
    elif u1=="Mpa":
       return num*1000000,"*100000"    



    
#FUCNTUON FOR CALCULATING THE MATERIAL FOR THE 
def materialValueCalculator(val):
   if val=="ABS":
     return 130
   elif val=="Aluminum":
     return 140  
   elif val=="Asbestos Cement":
     return 140  
   elif val=="Asphalt Lining":
     return 135
   elif val=="Brass":
     return 135
   elif val=="Brick sewer":
     return 95
   elif val=="Cast-Iron - new unlined (CIP)":
     return 130
   elif val=="Cement lining":
     return 135
   elif val=="Concrete":
     return 120
   elif val=="Concrete lined, steel forms":
     return 140
   elif val=="Concrete lined, wooden forms":
     return 120
   elif val=="Copper":
     return 135
   elif val=="Corrugated Metal":
     return 60
   elif val=="Ductile Iron Pipe (DIP)":
     return 120
   elif val=="Fiber":
     return 140
   elif val=="Fiber Glass Pipe - FRP":
     return 150
   elif val=="Galvanized iron":
     return 120
   elif val=="Glass":
     return 130
   elif val=="Lead":
     return 135
   elif val=="Metal Pipes - Very to extremely smooth":
     return 135
   elif val=="Plastic":
     return 140
   elif val=="Polyvinyl chloride, PVC, CPVC":
     return 150
   elif val=="Tin":
      return 130
   elif val=="Wood Stave":
      return 115         
       
     
#DICTIONARY FOR THE SPECIFIC HEAT OF A SUBSTANCE
specificHeat={
'Aluminium':897,
'Asphalt'	:915,
'Bone' :  440,
'Boron' :1106,
'Brass':920,
'Brick':841,
'Cast Iron':554,
'Clay':878,
'Coal':	1262,
'Cobalt':420,
'Concrete':	879,	
'Copper':385,
'Glass':792,
'Gold':130,
'Granite':774,
'Gypsum':1090,
'Helium':5192,
'Hydrogen':14300,
'Ice':2090,
'Iron':462,
'Lead':130,
'Limestone':806,
'Lithium':3580,	
'Magnesium':1024,	
'Marble':832,	
'Mercury':126,
'Nitrogen':	1040,
'Oak Wood':	2380,
'Oxygen':919,
'Platinum':150,	
'Plutonium':140,
'Quartzite':1100,
'Rubber':2005,
'Salt':881,	
'Sand':780,
'Sandstone':740,
'Silicon':710,
'Silver':236,
'Soil':1810,
'Stainless Steel': 316,
'Steam':2094,
'Sulfur':706,
'Thorium':118,
'Tin':226,	
'Titanium':521,
'Tungsten':133,	
'Uranium':115,	
'Vandium':490,	
'Water':4187,
'Zinc':	389,
}
  

#FUNCTION FOR THE ROUNDING OFF THE NUMBER
def Roundoff(n):
  base=""
  power=""
  n='%.2E' % n
  s=str(n)
  base=""
  power=""
  f=False
  for i in range(0,len(s)):
    if s[i]=='E':
        f=True
        continue
    if f:
        power+=s[i]
    else:
        base+=s[i]           
   
  return base,power
  


#FUNCTION FOR THE TRIANGULRA MATRIX CALCULTOR
def TriangularMatrix(data):
    matA=[]
    
    for i in range(0,len(data)):
      t=[]
      for j in range(0,len(data[i])):
        t.append(data[i][j])
      matA.append(t)  

    col=0
    row=1
    
    i=row
    j=col

    while row<len(matA) and col<len(matA[0]):
        
      i=row
      j=col
      factor=matA[row-1][col]
      if factor==0:
        for k in range(0,len(matA[0])):
          matA[k][col]+=1
        factor=matA[row-1][col]  
      
      while i<len(matA):
          factor=matA[i][col]/matA[row-1][col]  
          while j<len(matA[i]):
            matA[i][j]-=(matA[row-1][j]*factor)
            j+=1
          i+=1
          j=col
      
      
      row+=1
      col+=1

    return matA   



def ohmslawcalculator(request):

  if request.method=='POST':
     given_data=request.POST.get('given_data')
     
      #VALUE FOR THE Current
     if request.POST.get('Ia')!=None and request.POST.get('Ia')!='' :     
      inp=str(request.POST.get('Ia'))
      if inp.isdigit():
          Ia=int(request.POST.get('Ia'))
      else:
          Ia=float(request.POST.get('Ia'))
     else:
        Ia=None

    #VALUE FOR THE resistance
     if request.POST.get('Ib')!=None and request.POST.get('Ib')!='':
      inp=str(request.POST.get('Ib'))
      if inp.isdigit():
          Ib=int(request.POST.get('Ib'))
      else:
          Ib=float(request.POST.get('Ib'))
     else:
      Ib=None

    #VALUE FOR THE  VOLTAGE
     if request.POST.get('F')!=None and request.POST.get('F')!='':
      inp=str(request.POST.get('F'))
      if inp.isdigit():
          F=int(request.POST.get('F'))
      else:
          F=float(request.POST.get('F'))
     else:
      F=None


     if given_data=="form1" and Ia and Ib:
       
       #Copy of the values
       Ia1=Ia
       Ib1=Ib
       
       #Units
       Ia_op=request.POST.get('Ia_op')
       Ib_op=request.POST.get('Ib_op')

       #Copying of the units
       Ia1_op=Ia_op
       Ib1_op=Ib_op

       #Converting Units
       Ia,Ia_c=convert2("curr",Ia_op,Ia)
       Ib,Ib_c=convert2("res",Ib_op,Ib)

       F=Ia*Ib
       #Power 
       p=F*Ia
  

       if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
       else:
        Ia=round(Ia,5)
       
       if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
         base1,power1=Roundoff(Ib)
         Ib=f"{base1} X 10"+add_tags('sup',power1)
       else:
         Ib=round(Ib,5) 

       if not  ((p>=1 and p<=10000) or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
         base1,power1=Roundoff(p)
         p=f"{base1} X 10"+add_tags('sup',power1)
       else:
         p=round(p,5) 
       
       if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
       else:
         F=round(F,5) 


       context={
         'F':F,
         'Ia':Ia,
         'Ib':Ib,
         'Ia1':Ia1,
         'Ib1':Ib1,
         'Ia_op':Ia_op,
         'Ib_op':Ib_op,
         'Ia1_op':Ia1_op,
         'Ib1_op':Ib1_op,
         'p':p,
         'given_data':given_data,
         'id':1,
         'Ia_c':Ia_c,
         'Ib_c':Ib_c
       }

       return render(request,'ohmslawcalculator.html',context)
     
     
     elif given_data=="form2" and F and Ib:
       
       
       #Copy of the values
       
       Ib1=Ib
       F1=F

       #Units
       F_op=request.POST.get('F_op')
       Ib_op=request.POST.get('Ib_op')
       
       
       #Copying of the units
       F1_op=F_op
       Ib1_op=Ib_op

       F,F_c=convert2("volt",F_op,F)
       Ib,Ib_c=convert2("res",Ib_op,Ib)

       Ia=F/Ib
       Ia1=Ia
       #Power 
       p=F*Ia
       
       if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
       else:
        Ia=round(Ia,5)
       
       if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
         base1,power1=Roundoff(Ib)
         Ib=f"{base1} X 10"+add_tags('sup',power1)
       else:
         Ib=round(Ib,5) 

       if not  ((p>=1 and p<=10000) or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
         base1,power1=Roundoff(p)
         p=f"{base1} X 10"+add_tags('sup',power1)
       else:
         p=round(p,5) 
       
       if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
       else:
         F=round(F,5) 
       
       

       context={
         'F':F,
         'Ia':Ia,
         'Ib':Ib,
         'F1':F1,
         'Ia1':Ia1,
         'Ib1':Ib1,
         'F_op':F_op,
         'Ib_op':Ib_op,
         'F1_op':F1_op,
         'Ib1_op':Ib1_op,
         'p':p,
         'given_data':given_data,
         'id':1,
         'F_c':F_c,
         'Ib_c':Ib_c
       }

       return render(request,'ohmslawcalculator.html',context)

     elif given_data=="form3" and F and Ia:
       
       #Copy of the values
       Ia1=Ia
       F1=F

       #Units
       F_op=request.POST.get('F_op')
       Ia_op=request.POST.get('Ia_op')

       #Copying of the units
       F1_op=F_op
       Ia1_op=Ia_op
       
       F,F_c=convert2("volt",F_op,F)
       Ia,Ia_c=convert2("curr",Ia_op,Ia)

       Ib=F/Ia
       Ib1=Ib
       #Power 
       p=F*Ia

       if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
       else:
        Ia=round(Ia,5)
       
       if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
         base1,power1=Roundoff(Ib)
         Ib=f"{base1} X 10"+add_tags('sup',power1)
       else:
         Ib=round(Ib,5) 

       if not  ((p>=1 and p<=10000) or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000 )):
         base1,power1=Roundoff(p)
         p=f"{base1} X 10"+add_tags('sup',power1)
       else:
         p=round(p,5) 
       
       if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
       else:
         F=round(F,5)  
      
       

       context={
         'F':F,
         'Ia':Ia,
         'Ib':Ib,
         'F1':F1,
         'Ia1':Ia1,
         'Ib1':Ib1,
         'F_op':F_op,
         'Ia_op':Ia_op,
         'F1_op':F1_op,
         'Ia1_op':Ia1_op,
         'p':p,
         'given_data':given_data,
         'id':1,
         'F_c':F_c,
         'Ia_c':Ia_c
       }

       return render(request,'ohmslawcalculator.html',context)
   
     else:
      return render(request,'ohmslawcalculator.html',{'given_data':given_data})  

  else:  
   return render(request,'ohmslawcalculator.html',{'given_data':'form1'})





def accelerationofparticleinelectricfield(request): 
   if request.method=='POST':
      given_data=request.POST.get('given_data')
      


      if request.POST.get('Ia')!=None and  request.POST.get('Ia')!="":
        inp=str(request.POST.get('Ia'))
        if inp.isdigit():
          Ia=int(request.POST.get('Ia'))
        else:
         Ia=float(request.POST.get('Ia'))

      else:
        Ia=None


      if request.POST.get('Ib')!=None and request.POST.get('Ib')!="":
        inp=str(request.POST.get('Ib'))
        if inp.isdigit():
          Ib=int(request.POST.get('Ib'))
        else:
          Ib=float(request.POST.get('Ib'))

      else:
        Ib=None


      if request.POST.get('F')!=None and request.POST.get('F')!="":
        inp=str(request.POST.get('F'))
        if inp.isdigit():
          F=int(request.POST.get('F'))
        else:
         F=float(request.POST.get('F'))
      else:
        F=None


      if request.POST.get('d')!=None and request.POST.get('d')!="":
        inp=str(request.POST.get('d'))
        if inp.isdigit():
          d=int(request.POST.get('d'))
        else:
          d=float(request.POST.get('d'))

      else:
        d=None

      if given_data=='form1' and Ia and Ib and d:
        #Copying the variables
        Ia1=Ia
        Ib1=Ib
        d1=d

        #Fetching the units  
        Ia_op=request.POST.get('Ia_op')
        Ib_op=request.POST.get('Ib_op')
        d_op=request.POST.get('d_op')

        #Conversion of units
        Ia,Ia_c=convert2("mass",Ia_op,Ia)
        Ib,Ib_c=convert2("force",Ib_op,Ib)
        d,d_c=convert2("charge",d_op,d)
        ###
        Ia=Ia/1000

        #Calculation
        F=Ib*d/Ia

        if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and round(Ia,3)<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
        else:
         Ia=round(Ia,5)
       
        if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and round(Ib,3)<=10000)):
         base1,power1=Roundoff(Ib)
         Ib=f"{base1} X 10"+add_tags('sup',power1)
        else:
          Ib=round(Ib,5) 

        if not  ((d>=1 and d<=10000) or (round(d,3)!=0 and round(d,3)!=0.001 and round(d,3)<=10000)):
         base1,power1=Roundoff(d)
         d=f"{base1} X 10"+add_tags('sup',power1)
        else:
         d=round(d,5) 
       
        if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and round(F,3)<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
        else:
         F=round(F,5)  
      

        #Passing the variables
        context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'd':d,
          'Ia1':Ia1,
          'Ib1':Ib1,
          'd1':d1,
          'Ia_op':Ia_op,
          'Ib_op':Ib_op,
          'd_op':d_op,
          'given_data':given_data,
          'id':1,
          'Ia_c':Ia_c,
          'Ib_c':Ib_c,
          'd_c':d_c,
          
        }

        #Rendering the template
        return render(request,'accelerationofparticleinelectricfield.html',context)
      
      
      elif given_data=='form2' and F and Ib and d:
        #Copying the variables
        F1=F
        Ib1=Ib
        d1=d

        #Fetching the units  
        F_op=request.POST.get('F_op')
        Ib_op=request.POST.get('Ib_op')
        d_op=request.POST.get('d_op')

        #Conversion of units
        
        Ib,Ib_c=convert2("force",Ib_op,Ib)
        d,d_c=convert2("charge",d_op,d)
        

        #Calculation
        Ia=Ib*d/F
        if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
          base1,power1=Roundoff(Ia)
          Ia=f"{base1} X 10 "+add_tags('sup',power1)
        else:
          Ia=round(Ia,5)
        
        if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
          base1,power1=Roundoff(Ib)
          Ib=f"{base1} X 10"+add_tags('sup',power1)
        else:
          Ib=round(Ib,5) 

        if not  ((d>=1 and d<=10000) or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
          base1,power1=Roundoff(d)
          d=f"{base1} X 10"+add_tags('sup',power1)
        else:
          d=round(d,5) 
        
        if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
          base1,power1=Roundoff(F)
          F=f"{base1} X 10"+add_tags('sup',power1)
        else:
          F=round(F,5)  
        


        #Passing the variables
        context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'd':d,
          'F1':F1,
          'Ib1':Ib1,
          'd1':d1,
          'F_op':F_op,
          'Ib_op':Ib_op,
          'd_op':d_op,
          'given_data':given_data,
          'id':1,
          'Ib_c':Ib_c,
          'd_c':d_c,
        }
        #Rendering the template
        return render(request,'accelerationofparticleinelectricfield.html',context)
      
      elif given_data=='form3' and F and Ia and d:
        #Copying the variables
        F1=F
        Ia1=Ia
        d1=d

        #Fetching the units  
        F_op=request.POST.get('F_op')
        Ia_op=request.POST.get('Ia_op')
        d_op=request.POST.get('d_op')

        #Conversion of units
        Ia,Ia_c=convert2("mass",Ia_op,Ia)
        d,d_c=convert2("charge",d_op,d)
        ###

        Ia=Ia/1000


        #Calculation
        Ib=Ia*F/d

        if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
          base1,power1=Roundoff(Ia)
          Ia=f"{base1} X 10 "+add_tags('sup',power1)
        else:
          Ia=round(Ia,5)
        
        if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
          base1,power1=Roundoff(Ib)
          Ib=f"{base1} X 10"+add_tags('sup',power1)
        else:
          Ib=round(Ib,5) 

        if not  ((d>=1 and d<=10000) or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
          base1,power1=Roundoff(d)
          d=f"{base1} X 10"+add_tags('sup',power1)
        else:
          d=round(d,5) 
        
        if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
          base1,power1=Roundoff(F)
          F=f"{base1} X 10"+add_tags('sup',power1)
        else:
          F=round(F,5)  
        


        #Passing the variables
        context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'd':d,
          'F1':F1,
          'Ia1':Ia1,
          'd1':d1,
          'F_op':F_op,
          'Ia_op':Ia_op,
          'd_op':d_op,
          'given_data':given_data,
          'id':1,
          'Ia_c':Ia_c,
          'd_c':d_c,
        }
        #Rendering the template
        return render(request,'accelerationofparticleinelectricfield.html',context)
      
      elif given_data=='form4' and F and Ia and Ib:
        #Copying the variables
        F1=F
        Ia1=Ia
        Ib1=Ib

        #Fetching the units  
        F_op=request.POST.get('F_op')
        Ia_op=request.POST.get('Ia_op')
        Ib_op=request.POST.get('Ib_op')

        #Conversion of units
        Ia,Ia_c=convert2("mass",Ia_op,Ia)
        Ib,Ib_c=convert2("force",Ib_op,Ib)
        
        ###
        Ia=Ia/1000

        #Calculation
        d=Ia*F/Ib
        
        if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
          base1,power1=Roundoff(Ia)
          Ia=f"{base1} X 10 "+add_tags('sup',power1)
        else:
          Ia=round(Ia,5)
        
        if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
          base1,power1=Roundoff(Ib)
          Ib=f"{base1} X 10"+add_tags('sup',power1)
        else:
          Ib=round(Ib,5) 

        if not  ((d>=1 and d<=10000) or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
          base1,power1=Roundoff(d)
          d=f"{base1} X 10"+add_tags('sup',power1)
        else:
          d=round(d,5) 
        
        if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)): 
          base1,power1=Roundoff(F)
          F=f"{base1} X 10"+add_tags('sup',power1)
        else:
          F=round(F,5)  
        


        #Passing the variables
        context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'd':d,
          'F1':F1,
          'Ia1':Ia1,
          'Ib1':Ib1,
          'F_op':F_op,
          'Ia_op':Ia_op,
          'Ib_op':Ib_op,
          'given_data':given_data,
          'id':1,
          'Ia_c':Ia_c,
          'Ib_c':Ib_c,
        }

        #Rendering the template
        return render(request,'accelerationofparticleinelectricfield.html',context)



      else:
        return render(request,'accelerationofparticleinelectricfield.html',{'given_data':given_data})

   else: 
    return render(request,'accelerationofparticleinelectricfield.html',{'given_data':'form1'})




def weightotherplanets(request):
  if request.method=='POST':
     
     given_data=request.POST.get('given_data')
     
     val={"Earth":1,"Mercury":0.38,"Venus":0.91,"Mars":0.38,"Jupiter":2.34,"Saturn":1.06,"Uranus":0.92,"Neptun":1.19,"Pluto":0.06,"Moon":0.167}
     
     names=["Earth","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptun","Pluto","Moon"]
     values=[1,0.38,0.91,0.38,2.34,1.06,0.92,1.19,0.06,0.167]
     

     form=False
     if 'f1' in request.POST:
       form=True

     if request.POST.get('Ia')!=None and request.POST.get('Ia')!='' :     
              inp=str(request.POST.get('Ia'))
              if inp.isdigit():
                  Ia=int(request.POST.get('Ia'))
              else:
                  Ia=float(request.POST.get('Ia'))
     else:
       Ia=None


     if given_data=="form1" and form:
       
       name="Earth"       
        
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       
       Ia=round(Ia/1000,6)

       ans=[]
       for i in val:
         j=round(val[i]*Ia,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'id':1,
         'Ia_c':Ia_c          
       }
       return render(request,'weightotherplanets.html',context)
     


     elif given_data=="form2" and form:
       name="Mercury" 
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,
         'Ia_c':Ia_c          
       }
       return render(request,'weightotherplanets.html',context)  
     


     elif given_data=="form3" and form:
       name="Venus"
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,
         'Ia_c':Ia_c          
       }
       return render(request,'weightotherplanets.html',context)   
     


     elif given_data=="form4" and form:
       name="Mars"
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,
         'Ia_c':Ia_c          
       }
       return render(request,'weightotherplanets.html',context)  
     


     elif given_data=="form5" and form:
       name="Jupiter"
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,
         'Ia_c':Ia_c          
       }
       return render(request,'weightotherplanets.html',context)  
     


     elif given_data=="form6" and form:
       name="Saturn"
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,
         'Ia_c':Ia_c          
       }
       return render(request,'weightotherplanets.html',context)  
     


     elif given_data=="form7" and form:
       name="Uranus"
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,
         'Ia_c':Ia_c          
       }
       return render(request,'weightotherplanets.html',context)  
     


     elif given_data=="form8" and form:
       name="Neptun"
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,    
         'Ia_c':Ia_c      
       }
       return render(request,'weightotherplanets.html',context)  
      


     elif given_data=="form9" and form:
       name="Pluto"
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
         
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,   
         'Ia_c':Ia_c       
       }
       return render(request,'weightotherplanets.html',context) 
     


     elif given_data=="form10" and form:
       name="Moon"
       Ia1=Ia
       Ia_op=request.POST.get('Ia_op')
       Ia,Ia_c=convert2("mass",Ia_op,Ia)
       Ia=round(Ia/1000,6)

       Iw=round(Ia/val[name],6)

       ans=[]
       for i in val:
         j=round(val[i]*Iw,6)
         ans.append(j)  

       list=zip(names,values,ans)
       sellername=[1,2,3,4]  
       context={
         'name':name,
         'given_data':given_data,
         'Ia':Ia,
         'Ia1':Ia1,
         'Ia_op':Ia_op,
         'list':list,
         'fact':val[name],
         'Iw':Iw,
         'id':1,          
         'Ia_c':Ia_c
       }
       return render(request,'weightotherplanets.html',context)  

     else:
        id=int(given_data[4:])
        Name=names[id-1]  
        return render(request,'weightotherplanets.html',{'given_data':given_data,'Ia1':12,'name':Name})  
      
  else:
    return render(request,'weightotherplanets.html',{'name':'Earth','Ia1':12})





#FUNCTION FOR THE MOMENTUM WITH TIME CALCULATOR
def momentumwithtimecalculator(request):
  """Here Ib is for the change in time
     Here F is for the change in momentum
     Here Ia is for the Force
  """
  if request.method=='POST':
  
    given_data=request.POST.get('given_data')
   
    #Obtaining the Ia
    if request.POST.get('Ia')!=None and request.POST.get('Ia')!='' :     
              inp=str(request.POST.get('Ia'))
              if inp.isdigit():
                  Ia=int(request.POST.get('Ia'))
              else:
                  Ia=float(request.POST.get('Ia'))
    else:
       Ia=None
    
    #Obtaining the Ib
    if request.POST.get('Ib')!=None and request.POST.get('Ib')!='' :     
              inp=str(request.POST.get('Ib'))
              if inp.isdigit():
                  Ib=int(request.POST.get('Ib'))
              else:
                  Ib=float(request.POST.get('Ib'))
    else:
       Ib=None

   #Obtaining the F 
    if request.POST.get('F')!=None and request.POST.get('F')!='' :     
              inp=str(request.POST.get('F'))
              if inp.isdigit():
                  F=int(request.POST.get('F'))
              else:
                  F=float(request.POST.get('F'))
    else:
       F=None

    form=False
  
    if "f1" in request.POST:
      form=True

    if given_data=='form1' and form:  
      #Copying of variables
      Ia1=Ia
      Ib1=Ib
      
      #Units
      Ia_op=request.POST.get('Ia_op')
      Ib_op=request.POST.get('Ib_op')

      #Conversion of units
      Ia,Ia_c=convert2("force",Ia_op,Ia)
      Ib,Ib_c=convert2("time",Ib_op,Ib)
      

      #Calculation
      F=Ia*Ib
      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
          base1,power1=Roundoff(Ia)
          Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
      
      if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
        base1,power1=Roundoff(Ib)
        Ib=f"{base1} X 10"+add_tags('sup',power1)
      else:
        Ib=round(Ib,5) 
      
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
        base1,power1=Roundoff(F)
        F=f"{base1} X 10"+add_tags('sup',power1)
      else:
        F=round(F,5)  
      
      context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'Ia1':Ia1,
          'Ib1':Ib1,
          'Ia_op':Ia_op,
          'Ib_op':Ib_op,
          'id':1,
          'given_data':given_data,
          'Ia_c':Ia_c,
          'Ib_c':Ib_c,  
      }
      return render(request,'momentumwithtimecalculator.html',context)

    elif given_data=='form2' and form:  
      #Copying of variables
      F1=F
      Ib1=Ib
      
      #Units
      F_op=request.POST.get('F_op')
      Ib_op=request.POST.get('Ib_op')
      
      #Conversion of units
      
      #for the momentum
      F_c=""
      if F_op[0]!='k':
        F=F/1000
        F_c="/1000"
      
      Ib,Ib_c=convert2("time",Ib_op,Ib)
  
      #Calculation
      Ia=F/Ib

      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ib<=10000)):
        base1,power1=Roundoff(Ia)
        Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
      
      if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
        base1,power1=Roundoff(Ib)
        Ib=f"{base1} X 10"+add_tags('sup',power1)
      else:
        Ib=round(Ib,5) 

      
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
        base1,power1=Roundoff(F)
        F=f"{base1} X 10"+add_tags('sup',power1)
      else:
        F=round(F,5)  
    
      context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'F1':F1,
          'Ib1':Ib1,
          'F_op':F_op,
          'Ib_op':Ib_op,
          'id':1,
          'given_data':given_data,
          'Ib_c':Ib_c,
          'F_c':F_c
      }
      return render(request,'momentumwithtimecalculator.html',context)

    elif given_data=='form3' and form:  
      #Copying of variables
      Ia1=Ia
      F1=F
      
      #Units
      Ia_op=request.POST.get('Ia_op')
      F_op=request.POST.get('F_op')
      
      #Conversion of units
      F_c=""
      if F_op[0]!='k':
        F=F/1000
        F_c="/1000"
      Ia,Ia_c=convert2("force",Ia_op,Ia)
      
      #Calculation
      Ib=F/Ia
      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
        base1,power1=Roundoff(Ia)
        Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
       Ia=round(Ia,5)
      
      if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
        base1,power1=Roundoff(Ib)
        Ib=f"{base1} X 10"+add_tags('sup',power1)
      else:
        Ib=round(Ib,5) 

      
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
        base1,power1=Roundoff(F)
        F=f"{base1} X 10"+add_tags('sup',power1)
      else:
        F=round(F,5)  

      context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'Ia1':Ia1,
          'F1':F1,
          'Ia_op':Ia_op,
          'F_op':F_op,
          'id':1,
          'given_data':given_data,
          'Ia_c':Ia_c,
          'F_c':F_c
      }
      return render(request,'momentumwithtimecalculator.html',context)  
      
    else:
       return render(request,'momentumwithtimecalculator.html',{'given_data':given_data})

  else:
        return render(request,'momentumwithtimecalculator.html',{'given_data':'form1'})  

  




#FUNCTION FOR THE SPECIFIC HEAT CAPACITY CALCULATOR
def specificheatcalculator(request):
  """
  Here Ia is for the change in temperature
  mass is for the mass
  F is for the energy
  mat_op is for the material
  c is for the specific heat capacity
  """
  if request.method=="POST":
    given_data=request.POST.get('given_data')
    #Obtaining the Ia
    if request.POST.get('Ia')!=None and request.POST.get('Ia')!='' :     
              inp=str(request.POST.get('Ia'))
              if inp.isdigit():
                  Ia=int(request.POST.get('Ia'))
              else:
                  Ia=float(request.POST.get('Ia'))
    else:
       Ia=None
    
   #Obtaining the F 
    if request.POST.get('F')!=None and request.POST.get('F')!='' :     
              inp=str(request.POST.get('F'))
              if inp.isdigit():
                  F=int(request.POST.get('F'))
              else:
                  F=float(request.POST.get('F'))
    else:
       F=None

    form=False

   #Obtaining the mass 
    if request.POST.get('mass')!=None and request.POST.get('mass')!='' :     
              inp=str(request.POST.get('mass'))
              if inp.isdigit():
                  mass=int(request.POST.get('mass'))
              else:
                  mass=float(request.POST.get('mass'))
    else:
       mass=None

    #OBTAINING THE MATERIAL
    mat_op=request.POST.get("mat_op")
  
    form=False
    if "f1" in request.POST:
      form=True
    
     
     #FORM 1
    if given_data=='form1' and form:  
      #Copying of variables
      Ia1=Ia
      mass1=mass
      
      #Specific heat capacity of material
      c=specificHeat[mat_op]

      #Units
      mass_op=request.POST.get('mass_op')
      Ia_op=request.POST.get('Ia_op')

      #Conversion of units
      mass,mass_c=convert2("mass",mass_op,mass)
      Ia_c=""
      if Ia_op=="°F":
        Ia=0.55*Ia
        Ia_c="*0.55"


      mass=mass/1000
      #Calculation
      F=c*mass*Ia

      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
       
      if not  ((mass>=1 and mass<=10000) or (round(mass,3)!=0 and round(mass,3)!=0.001 and mass<=10000)):
         base1,power1=Roundoff(mass)
         mass=f"{base1} X 10"+add_tags('sup',power1)
      else:
         mass=round(mass,5) 
       
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
      else:
         F=round(F,5)       

      context={
          'F':F,
          'Ia':Ia,
          'mass':mass,
          'Ia1':Ia1,
          'mass1':mass1,
          'Ia_op':Ia_op,
          'mass_op':mass_op,
          'mat_op':mat_op,
          'c':c,
          'id':1,
          'given_data':given_data,
          'id':1,
          'mass_c':mass_c,
          'Ia_c':Ia_c
      }
      return render(request,'specificheatcalculator.html',context)


    #FORM 2
    elif given_data=='form2' and form:  
      #Copying of variables
      F1=F
      mass1=mass

      
      #Units
      F_op=request.POST.get('F_op')
      mass_op=request.POST.get('mass_op')

      
      if mass==0:
        context={
         'F1':F1,
         'F':F,
         'mass':mass,
         'mass1':mass1,
         'F_op':F_op,
         'mass_op':mass_op,
         'given_data':given_data,
          'message':"Enter Valid data"
        }
        return render(request,'specificheatcalculator.html',context)

      #Specific heat capacity of material
      c=specificHeat[mat_op]

      #Conversion of units
      F,F_c=convert2("energy",F_op,F)
      mass,mass_c=convert2("mass",mass_op,mass)
      mass=mass/1000
      #Calculation
      Ia=F/(c*mass)
      
      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
       
      if not  ((mass>=1 and mass<=10000) or (round(mass,3)!=0 and round(mass,3)!=0.001 and mass<=10000)):
         base1,power1=Roundoff(mass)
         mass=f"{base1} X 10"+add_tags('sup',power1)
      else:
         mass=round(mass,5) 
       
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
      else:
         F=round(F,5)  
      
 
      context={
          'F':F,
          'Ia':Ia,
          'mass':mass,
          'F1':F1,
          'mass1':mass1,
          'F_op':F_op,
          'mass_op':mass_op,
          'mat_op':mat_op,
          'c':c,
          'id':1,
          'given_data':given_data,
          'F_c':F_c,
          'mass_c':mass_c
      }
      return render(request,'specificheatcalculator.html',context)


    elif given_data=='form3' and form:  
      #Copying of variables
      Ia1=Ia
      F1=F
     
      #Specific heat capacity of material
      c=specificHeat[mat_op]

      #Units
      Ia_op=request.POST.get('Ia_op')
      F_op=request.POST.get('F_op')
           

      #Conversion of units
      F,F_c=convert2("energy",F_op,F)
      Ia_c=""
      if Ia=="°F":
        Ia=0.55*Ia
        Ia_c="*0.55"

      #Calculation
      mass=F/(c*Ia)
      
      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
       
      if not  ((mass>=1 and mass<=10000) or (round(mass,3)!=0 and round(mass,3)!=0.001 and mass<=10000)):
         base1,power1=Roundoff(mass)
         mass=f"{base1} X 10"+add_tags('sup',power1)
      else:
         mass=round(mass,5) 
       
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
      else:
         F=round(F,5)  
      


      context={
          'F':F,
          'Ia':Ia,
          'mass':mass,
          'Ia1':Ia1,
          'F1':F1,
          'F_op':F_op,
          'mat_op':mat_op,
          'c':c,
          'id':1,
          'given_data':given_data,
          'F_c':F_c,
          'Ia_c':Ia_c
      }
      return render(request,'specificheatcalculator.html',context)    
    
    else:
        return render(request,'specificheatcalculator.html',{'given_data':given_data}) 
  
  else:
    return render(request,'specificheatcalculator.html',{'given_data':'form1'})
  
  



#FUNCTION FOR THE HALF LIFE CALCULATOR
def halflifecalculator(request):
 """
  Here Ia is for the remainig quantity 
  decay is for the decay constant
  F is for the initial quantity
  mat is for the total time
  
  """
 if request.method=="POST":
    given_data=request.POST.get('given_data')
    #Obtaining the Ia
    if request.POST.get('Ia')!=None and request.POST.get('Ia')!='' :     
              inp=str(request.POST.get('Ia'))
              if inp.isdigit():
                  Ia=int(request.POST.get('Ia'))
              else:
                  Ia=float(request.POST.get('Ia'))
    else:
       Ia=None
    
   #Obtaining the F 
    if request.POST.get('F')!=None and request.POST.get('F')!='' :     
              inp=str(request.POST.get('F'))
              if inp.isdigit():
                  F=int(request.POST.get('F'))
              else:
                  F=float(request.POST.get('F'))
    else:
       F=None

    form=False

   #Obtaining the decay 
    if request.POST.get('decay')!=None and request.POST.get('decay')!='' :     
              inp=str(request.POST.get('decay'))
              if inp.isdigit():
                  decay=int(request.POST.get('decay'))
              else:
                  decay=float(request.POST.get('decay'))
    else:
       decay=None

    #OBTAINING THE MATERIAL
    if request.POST.get('mat')!=None and request.POST.get('mat')!='' :     
              inp=str(request.POST.get('mat'))
              if inp.isdigit():
                  mat=int(request.POST.get('mat'))
              else:
                  mat=float(request.POST.get('mat'))
    else:
       mat=None


  
    form=False
    if "f1" in request.POST:
      form=True
    
     
     #FORM 1
    if given_data=='form1' and form:  
      #Copying of variables
      Ia1=Ia
      decay1=decay
      mat1=mat

      
      if decay==0:
          message="Decay Consant cannot be 0"
          context={
           'Ia':Ia, 
           'mat':mat,
           'Ia1':Ia1,
           'mat1':mat1,
           'decay':decay,
           'decay1':decay1,
           'decay_op':request.POST.get('decay_op'),
           'given_data':given_data,
           'message':message
          }
          return render(request,'halflifecalculator.html',context)
      

      
      #Units
      decay_op=request.POST.get('decay_op')
      mat_op=request.POST.get('mat_op')

      #Conversion of units
      decay,decay_c=convert2("frequency",decay_op,decay)
      mat,mat_c=convert2("time",mat_op,mat)
      
      
      half=0.693/decay
      
      #Calculation
      #N(t) = N(0) * 0.5(t/T)
      if 0.5**(mat/half)!=0:
        F=Ia/(0.5**(mat/half))
      else:
        F= float('inf')  

     #CALCULATING THE HALF LIFE
      half=0.693/decay
      
      if not((half>=1 and half<=10000) or (round(half,3)!=0 and round(half,3)!=0.001 and half<=10000)):
              base1,power1=Roundoff(half)
              half=f"{base1} X 10 "+add_tags('sup',power1)
            
      else:
              half=round(half,4)
         
  
      if not((Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
            if Ia!=0:
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Ia='0'  
      else:
              Ia=round(Ia,4)
         
      if not((decay>=1 and decay<=10000) or (round(decay,3)!=0 and round(decay,3)!=0.001 and decay<=10000)):
              base1,power1=Roundoff(decay)
              decay=f"{base1} X 10 "+add_tags('sup',power1)
            
      else:
              decay=round(decay,4)
         
  
      if not((mat>=1 and mat<=10000) or (round(mat,3)!=0 and round(mat,3)!=0.001 and mat<=10000)):
              base1,power1=Roundoff(mat)
              mat=f"{base1} X 10 "+add_tags('sup',power1)
           
      else:
              mat=round(mat,4)
         
     
      if not((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
             if F!= float('inf'): 
              base1,power1=Roundoff(F)
              F=f"{base1} X 10 "+add_tags('sup',power1)

      else:
              F=round(F,4)
         
          
              
      
      context={
          'F':F,
          'Ia':Ia,
          'decay':decay,
          'Ia1':Ia1,
          'mat':mat,
          'mat1':mat1,
          'decay1':decay1,
          'half':half,
          'decay_op':decay_op,
          'mat_op':mat_op,
          'id':1,
          'given_data':given_data,
          'id':1,
          'decay_c':decay_c,
          'mat_c':mat_c
      }
      return render(request,'halflifecalculator.html',context)


    #FORM 2
    elif given_data=='form2' and form:  
      #Copying of variables
      F1=F
      decay1=decay
      mat1=mat
      
      if decay==0:
          message="Decay Consant cannot be 0"
          context={
           'F':F, 
           'mat':mat,
           'F1':F1,
           'mat1':mat1,
           'decay':decay,
           'decay1':decay1,
           'decay_op':request.POST.get('decay_op'),
           'given_data':given_data,
           'message':message
          }
          return render(request,'halflifecalculator.html',context)
      
      
      #Units
      mat_op=request.POST.get('mat_op')
      decay_op=request.POST.get('decay_op')

      #Conversion of units
      decay,decay_c=convert2("frequency",decay_op,decay)
      mat,mat_c=convert2("time",mat_op,mat)
      
      #CALCULATING THE HALF LIFE
      half=0.693/decay

      #Calculation
      #N(t) = N(0) * 0.5(t/T)
      Ia=F*0.5**(mat/half)

      if not((half>=1 and half<=10000) or (round(half,3)!=0 and round(half,3)!=0.001 and half<=10000)):
              base1,power1=Roundoff(half)
              half=f"{base1} X 10 "+add_tags('sup',power1) 
      else:
              half=round(half,4)
         
  
      if not((Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
            if Ia!=0:
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Ia='0'  
      else:
              Ia=round(Ia,4)
         
      if not((decay>=1 and decay<=10000) or (round(decay,3)!=0 and round(decay,3)!=0.001 and decay<=10000)):
              base1,power1=Roundoff(decay)
              decay=f"{base1} X 10 "+add_tags('sup',power1)
            
      else:
              decay=round(decay,4)
         
  
      if not((mat>=1 and mat<=10000) or (round(mat,3)!=0 and round(mat,3)!=0.001 and mat<=10000)):
              base1,power1=Roundoff(mat)
              mat=f"{base1} X 10 "+add_tags('sup',power1)
           
      else:
              mat=round(mat,4)
         
     
      if not((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10 "+add_tags('sup',power1)
            
      else:
              F=round(F,4)
         
          
      
 
      context={
          'F':F,
          'Ia':Ia,
          'decay':decay,
          'F1':F1,
          'mat1':mat1,
          'mat':mat,
          'decay1':decay1,
          'decay_op':decay_op,
          'mat_op':mat_op,
          'half':half,
          'id':1,
          'given_data':given_data,
          'decay_c':decay_c,
          'mat_c':mat_c
      }
      return render(request,'halflifecalculator.html',context)


    elif given_data=='form3' and form:  
      #Copying of variables
      Ia1=Ia
      F1=F
      decay1=decay
      
      if Ia>F or decay==0 :
          message="Remaining Quantity cannot be greater than Initial Quantity and decay constant cannot be zero"
          context={
           'F':F, 
           'Ia':Ia,
           'F1':F1,
           'Ia1':Ia1,
           'decay':decay,
           'decay1':decay1,
           'decay_op':request.POST.get('decay_op'),
           'given_data':given_data,
           'message':message
          }
          return render(request,'halflifecalculator.html',context)
      
      #Units
      decay_op=request.POST.get('decay_op')
     
      #Conversion of units
      decay,decay_c=convert2("frequency",decay_op,decay)
     
      half=0.693/decay  
      #Calculation
      #N(t) = N(0) * 0.5(t/T)
      k=math.log(Ia/F,0.5)
      mat=k*half

      if not((half>=1 and half<=10000) or (round(half,3)!=0 and round(half,3)!=0.001 and half<=10000)):
              base1,power1=Roundoff(half)
              half=f"{base1} X 10 "+add_tags('sup',power1)
             
      else:
              half=round(half,4)
         
  
      if not((Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
            if Ia!=0:
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Ia='0'  
      else:
              Ia=round(Ia,4)
         
      if not((decay>=1 and decay<=10000) or (round(decay,3)!=0 and round(decay,3)!=0.001 and decay<=10000)):
              base1,power1=Roundoff(decay)
              decay=f"{base1} X 10 "+add_tags('sup',power1)
             
      else:
              decay=round(decay,4)
         
  
      if not((mat>=1 and mat<=10000) or (round(mat,3)!=0 and round(mat,3)!=0.001 and mat<=10000)):
              base1,power1=Roundoff(mat)
              mat=f"{base1} X 10 "+add_tags('sup',power1)
             
      else:
              mat=round(mat,4)
         
     
      if not((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10 "+add_tags('sup',power1)
             
      else:
              F=round(F,4)
                       
    
      context={
          'F':F,
          'Ia':Ia,
          'decay':decay,
          'decay1':decay1,
          'decay_op':decay_op,
          'Ia1':Ia1,
          'F1':F1,
          'mat':mat,
          'half':half,
          'id':1,
          'given_data':given_data,
          'decay_c':decay_c
      }
      return render(request,'halflifecalculator.html',context)    
    
    else:
        return render(request,'halflifecalculator.html',{'given_data':given_data}) 
  
 else:
    return render(request,'halflifecalculator.html',{'given_data':'form1'})
  
  


#FUNCTION FOR THE WET BULB CALCULATOR
def wetbulbcalculator(request):
    if request.method=='POST':
      
      """Here rh is for the relative humidity
         Here Tw is for the temperature
      """
      #FETCHING THE VARIABLE rh     
      if request.POST.get('rh')!=None and request.POST.get('rh')!='' :     
              inp=str(request.POST.get('rh'))
              if inp.isdigit():
                  rh=int(request.POST.get('rh'))
              else:
                  rh=float(request.POST.get('rh'))
      else:
        rh=None

      #FETCHING THE VARIABLE T
      if request.POST.get('T')!=None and request.POST.get('T')!='' :     
              inp=str(request.POST.get('T'))
              if inp.isdigit():
                  T=int(request.POST.get('T'))
              else:
                  T=float(request.POST.get('T'))
      else:
        T=None
      
      #UNITS 
      T_op=request.POST.get('T_op')
      rh_op=request.POST.get('rh_op')

      #COPYING OF VARIABLES 
      T1=T
      rh1=rh

      #CONVERSION OF UNITS
      T,T_c=convert2("temp",T_op,T)
      
      ans1=False
      ans2=False

      if T_op=="°C" and not (T>=-20 and T<=50):
        ans1=True 
      # elif T_op=="°F" and not (T>=-4 and T<=122):
      #   ans1=True   
      # elif T_op=="K" and not (T>=-253.15 and T<=323.15):
      #   ans1=True   

      rh_c=""
      if rh_op =='‰':
        rh=rh*0.1  
        rh_c="*0.1"
       
      elif rh_op=='‱':
         rh=rh*0.01
         rh_c="*0.01"

      if not (rh>=5 and rh<=99):   
        ans2=True

      message1="This calculator is only accurate for temperatures between -20 °C to 50 °C, 253.15 k to 323.15 k , -4 °F to 122 °F"

      message2="This calculator is only accurate for relative humidities between 5% to 99%, 50‰ to 990‰,,500‱ to 9900‱"     

      if ans1 or ans2:
        context={
          'given_data':'form1',
          'rh':rh,
          'T':T,
          'rh1':rh1,
          'T1':T1,
          'T_op':T_op,
          'rh_op':rh_op,
           'message1':message1,
           'message2':message2,
        } 
        return render(request,'wetbulbcalculator.html',context)


      #CALCULATION
      Tw = T * math.atan(0.151977 * ((rh + 8.313659)**(1/2))) + math.atan(T + rh) - math.atan(rh - 1.676331) + 0.00391838 *((rh)**(3/2)) * math.atan(0.023101*rh) - 4.686035    
      
      if not  ((Tw>=1 and Tw<=10000) or (round(Tw,3)!=0 and round(Tw,3)!=0.001)):
         base1,power1=Roundoff(Tw)
         Tw=f"{base1} X 10"+add_tags('sup',power1)
      else:
         Tw=round(Tw,5) 
  
      
      context={
        'given_data':'form1',
        'T':T,
        'rh':rh,
        'T1':T1,
        'rh1':rh1,
        'T_op':T_op,
        'rh_op':rh_op,
        'Tw':Tw,
        'id':1,
        'rh_c':rh_c,
        'T_c':T_c
      }
      return render(request,'wetbulbcalculator.html',context)          

    else:  
      return render(request,'wetbulbcalculator.html',{'given_data':'form1','T1':6,'rh1':5})







def arrowspeedcalculator(request):
  if request.method=='POST':
    given_data=request.POST.get('given_data')
    
    """ Here Ib for the arrow speed(ft/s)
        Here Ia for the IBO rating(ft/s)
        Here F for the draw length(inches)
        Here p for the draw weight(pounds lb)
        Here q for the arrow weight(grains gr)
        Here r for the additional weight (grains gr)
    """
    #Obtaining the Ia
    if request.POST.get('Ia')!=None and request.POST.get('Ia')!='' :     
              inp=str(request.POST.get('Ia'))
              if inp.isdigit():
                  Ia=int(request.POST.get('Ia'))
              else:
                  Ia=float(request.POST.get('Ia'))
    else:
       Ia=None
    
    #Obtaining the Ib
    if request.POST.get('Ib')!=None and request.POST.get('Ib')!='' :     
              inp=str(request.POST.get('Ib'))
              if inp.isdigit():
                  Ib=int(request.POST.get('Ib'))
              else:
                  Ib=float(request.POST.get('Ib'))
    else:
       Ib=None

   #Obtaining the F 
    if request.POST.get('F')!=None and request.POST.get('F')!='' :     
              inp=str(request.POST.get('F'))
              if inp.isdigit():
                  F=int(request.POST.get('F'))
              else:
                  F=float(request.POST.get('F'))
    else:
       F=None

    #Obtaining the p
    if request.POST.get('p')!=None and request.POST.get('p')!='' :     
              inp=str(request.POST.get('p'))
              if inp.isdigit():
                  p=int(request.POST.get('p'))
              else:
                  p=float(request.POST.get('p'))
    else:
       p=None

    #Obtaining the q
    if request.POST.get('q')!=None and request.POST.get('q')!='' :     
              inp=str(request.POST.get('q'))
              if inp.isdigit():
                  q=int(request.POST.get('q'))
              else:
                  q=float(request.POST.get('q'))
    else:
       q=None

    #Obtaining the r
    if request.POST.get('r')!=None and request.POST.get('r')!='' :     
              inp=str(request.POST.get('r'))
              if inp.isdigit():
                  r=int(request.POST.get('r'))
              else:
                  r=float(request.POST.get('r'))
    else:
       r=None
       
    #FOR CHECKING THE FORM
    form=False
    if "f1" in request.POST:
      form=True   
  
    if given_data == 'form1' and form:
      
      #FETCHING THE UNITS
      Ia_op=request.POST.get('Ia_op')
      Ib_op=request.POST.get('Ib_op')
      F_op=request.POST.get('F_op')
      p_op=request.POST.get('p_op')
      q_op=request.POST.get('q_op')
      r_op=request.POST.get('r_op')

      #COPYING OF THE VARIABLES
      Ia1=Ia
      p1=p
      F1=F
      q1=q
      r1=r

      #Conversion of units here
      Ia_c=""
      if Ia_op != 'ft/s':
        Ia,Ia_c=convert2("vel",Ia_op,Ia)
        Ia=round(Ia*3.28,2)#CONVERTING INTO ft/s
        Ia_c+=" *3.28"
      
      p_c=""
      if p_op != 'lb':
        p,p_c=convert2("mass",p_op,p)
        p=p*0.453#convert into pounds
        p=p/1000
        p_c+=" *0.453"
      
      F_c=""
      if F_op != 'in':
        F,F_c=convert2("len",F_op,F)
        F=F*39.37
        F_c+="*39.37"
      
      q_c=""
      if q_op != 'gr' :
        q,q_c=convert2("mass",q_op,q)
        q=q*15432
        q=q/1000
        q_c+=" *15432"
      
      r_c=""
      if r_op != 'gr' :
        r,r_c=convert2("mass",r_op,r)
        r=r*15432  
        r=r/1000     
        r_c+=" *15432"

      #Calculation
      Ib=Ia+(F-30)*10-r/3+min(0,-(q-5*p/3))
     
      if not((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000) or (Ib<=-1 and Ib>=-10000)):
             if Ib!=0: 
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        Ib=round(Ib,3)    

     
      if not((Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000) or (Ia<=-1 and Ia>=-10000)):
             if Ia!=0: 
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        Ia=round(Ia,3)    
 

     
      if not((p>=1 and p<=10000) or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000) or (p<=-1 and p>=-10000)):
             if p!=0: 
              base1,power1=Roundoff(p)
              p=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        p=round(p,3)    

             
      
      
      if not((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000) or (F<=-1 and F>=-10000)):
             if F!=0: 
              base1,power1=Roundoff(F)
              F=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        F=round(F,3)    
   


      if not((q>=1 and q<=10000) or (round(q,3)!=0 and round(q,3)!=0.001 and q<=10000) or (q<=-1 and q>=-10000)):
             if q!=0: 
              base1,power1=Roundoff(q)
              q=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        q=round(q,3)    
    
      

      if not((r>=1 and r<=10000) or (round(r,3)!=0 and round(r,3)!=0.001 and r<=10000) or (r<=-1 and r>=-10000)):
             if r!=0: 
              base1,power1=Roundoff(r)
              r=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        r=round(r,3)    
            
         

      context={
         'given_data':given_data,
         'id':1,
         'Ia':Ia,
         'Ib':Ib,
         'F':F,
         'r':r,
         'p':p,
         'q':q,
         'Ia1':Ia1,
         'F1':F1,
         'r1':r1,
         'p1':p1,
         'q1':q1,
         'Ia_op':Ia_op,
         'F_op':F_op,
         'p_op':p_op,
         'r_op':r_op,
         'q_op':q_op,
         'Ia_c':Ia_c,
         #'Ib_c':Ib_c,
         'F_c':F_c,
         'p_c':p_c,
         'r_c':r_c,
         'q_c':q_c,

      }
      return render(request,'arrowspeedcalculator.html',context)

    if given_data == 'form2' and form:
      
      #FETCHING THE UNITS
      Ia_op=request.POST.get('Ia_op')
      Ib_op=request.POST.get('Ib_op')
      F_op=request.POST.get('F_op')
      p_op=request.POST.get('p_op')
      q_op=request.POST.get('q_op')
      r_op=request.POST.get('r_op')

      #COPYING OF THE VARIABLES
      Ib1=Ib
      p1=p
      F1=F
      q1=q
      r1=r

      #Conversion of units here
      Ib_c=""
      if Ib_op != 'ft/s':
        Ib,Ib_c=convert2("vel",Ib_op,Ib)
        Ib=round(Ib*3.28,2)#CONVERTING INTO ft/s
        Ib_c+=" *3.28"
       
      p_c=""
      if p_op != 'lb':
        p,p_c=convert2("mass",p_op,p)
        p=p*0.453#convert into pounds
        p=p/1000
        p_c+=" *0.453"
      
      F_c=""
      if F_op != 'in':
        F,F_c=convert2("len",F_op,F)
        F=F*39.37
        F_c+="*39.37"
      
      q_c=""
      if q_op != 'gr' :
        q,q_c=convert2("mass",q_op,q)
        q=q*15432
        q=q/1000
        q_c+=" *15432"
      
      r_c=""
      if r_op != 'gr' :
        r,r_c=convert2("mass",r_op,r)
        r=r*15432 
        r=r/1000     
        r_c+=" *15432"
      #Calculation
      Ia=Ib-(F-30)*10-r/3+min(0,-(q-5*p/3))
        
      if not((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000) or (Ib<=-1 and Ib>=-10000)):
             if Ib!=0: 
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        Ib=round(Ib,3)    

     
      if not((Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000) or (Ia<=-1 and Ia>=-10000)):
             if Ia!=0: 
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
         Ia=round(Ia,3)    
 

     
      if not((p>=1 and p<=10000) or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000) or (p<=-1 and p>=-10000)):
             if p!=0: 
              base1,power1=Roundoff(p)
              p=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        p=round(p,3)    

             
      
      
      if not((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000) or (F<=-1 and F>=-10000)):
             if F!=0: 
              base1,power1=Roundoff(F)
              F=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        F=round(F,3)    
   


      if not((q>=1 and q<=10000) or (round(q,3)!=0 and round(q,3)!=0.001 and q<=10000) or (q<=-1 and q>=-10000)):
             if q!=0: 
              base1,power1=Roundoff(q)
              q=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        q=round(q,3)    
    
      

      if not((r>=1 and r<=10000) or (round(r,3)!=0 and round(r,3)!=0.001 and r<=10000) or (r<=-1 and r>=-10000)):
             if r!=0: 
              base1,power1=Roundoff(r)
              r=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        r=round(r,3)    
            
         
     

      context={
         'given_data':given_data,
         'id':1,
         'Ia':Ia,
         'Ib':Ib,
         'F':F,
         'r':r,
         'p':p,
         'q':q,
         'Ib1':Ib1,
         'F1':F1,
         'r1':r1,
         'p1':p1,
         'q1':q1,
         'Ia_op':Ia_op,
         'F_op':F_op,
         'p_op':p_op,
         'r_op':r_op,
         'q_op':q_op,
         'Ib_op':Ib_op,
         'Ib_c':Ib_c,
         'F_c':F_c,
         'p_c':p_c,
         'r_c':r_c,
         'q_c':q_c,

      }
      return render(request,'arrowspeedcalculator.html',context)

    if given_data == 'form3' and form:
      
      #FETCHING THE UNITS
      Ia_op=request.POST.get('Ia_op')
      Ib_op=request.POST.get('Ib_op')
      F_op=request.POST.get('F_op')
      p_op=request.POST.get('p_op')
      q_op=request.POST.get('q_op')
      r_op=request.POST.get('r_op')

      #COPYING OF THE VARIABLES
      Ib1=Ib
      p1=p
      Ia1=Ia
      q1=q
      r1=r

      #Conversion of units here
      Ib_c=""
      if Ib_op != 'ft/s':
        Ib,Ib_c=convert2("vel",Ib_op,Ib)
        Ib=round(Ib*3.28,2)#CONVERTING INTO ft/s
        Ib_c+=" *3.28"
        
      Ia_c=""
      if Ia_op != 'ft/s':
        Ia,Ia_c=convert2("vel",Ia_op,Ia)
        Ia=round(Ia*3.28,2)#CONVERTING INTO ft/s
        Ia_c+=" *3.28"
      
      p_c=""
      if p_op != 'lb':
        p,p_c=convert2("mass",p_op,p)
        p=p*0.453#convert into pounds
        p=p/1000
        p_c+=" *0.453"
      
      
      q_c=""
      if q_op != 'gr' :
        q,q_c=convert2("mass",q_op,q)
        q=q*15432
        q=q/1000
        q_c+=" *15432"
      
      r_c=""
      if r_op != 'gr' :
        r,r_c=convert2("mass",r_op,r)
        r=r*15432  
        r=r/1000     
        r_c+="*15432"
      #Calculation
      F=(Ib-Ia+r/3-min(0,- (q-5*p)/3 ) )/10+30

      if not((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000) or (Ib<=-1 and Ib>=-10000)):
              if Ib!=0: 
                base1,power1=Roundoff(Ib)
                Ib=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
          Ib=round(Ib,3)    

      
      if not((Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000) or (Ia<=-1 and Ia>=-10000)):
              if Ia!=0: 
                base1,power1=Roundoff(Ia)
                Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
          Ia=round(Ia,3)    
  

      
      if not((p>=1 and p<=10000) or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000) or (p<=-1 and p>=-10000)):
              if p!=0: 
                base1,power1=Roundoff(p)
                p=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
          p=round(p,3)    

              
        
        
      if not((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000) or (F<=-1 and F>=-10000)):
              if F!=0: 
                base1,power1=Roundoff(F)
                F=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
          F=round(F,3)    
    


      if not((q>=1 and q<=10000) or (round(q,3)!=0 and round(q,3)!=0.001 and q<=10000) or (q<=-1 and q>=-10000)):
             if q!=0: 
              base1,power1=Roundoff(q)
              q=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        q=round(q,3)    
    
      

      if not((r>=1 and r<=10000) or (round(r,3)!=0 and round(r,3)!=0.001 and r<=10000) or (r<=-1 and r>=-10000)):
             if r!=0: 
              base1,power1=Roundoff(r)
              r=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        r=round(r,3)    
            
      
      context={
         'given_data':given_data,
         'id':1,
         'Ia':Ia,
         'Ib':Ib,
         'F':F,
         'r':r,
         'p':p,
         'q':q,
         'Ib1':Ib1,
         'Ia1':Ia1,
         'r1':r1,
         'p1':p1,
         'q1':q1,
         'Ia_op':Ia_op,
         'F_op':F_op,
         'p_op':p_op,
         'r_op':r_op,
         'q_op':q_op,
         'Ib_op':Ib_op, 
         'Ia_c':Ia_c,
         'Ib_c':Ib_c,
         'p_c':p_c,
         'r_c':r_c,
         'q_c':q_c,

      }
      return render(request,'arrowspeedcalculator.html',context)
    
    
    if given_data == 'form6' and form:
      
      #FETCHING THE UNITS
      Ia_op=request.POST.get('Ia_op')
      Ib_op=request.POST.get('Ib_op')
      F_op=request.POST.get('F_op')
      p_op=request.POST.get('p_op')
      q_op=request.POST.get('q_op')
      r_op=request.POST.get('r_op')

      #COPYING OF THE VARIABLES
      Ib1=Ib
      F1=F
      Ia1=Ia
      p1=p
      q1=q

      #Conversion of units here
      Ib_c=""
      if Ib_op != 'ft/s':
        Ib,Ib_c=convert2("vel",Ib_op,Ib)
        Ib=round(Ib*3.28,2)#CONVERTING INTO ft/s
        Ib_c+=" *3.28"
        
      Ia_c=""
      if Ia_op != 'ft/s':
        Ia,Ia_c=convert2("vel",Ia_op,Ia)
        Ia=round(Ia*3.28,2)#CONVERTING INTO ft/s
        Ia_c+=" *3.28"
      
      p_c=""
      if p_op != 'lb':
        p,p_c=convert2("mass",p_op,p)
        p=p*0.453#convert into pounds
        p=p/1000
        p_c+=" *0.453"
      
      F_c=""
      if F_op != 'in':
        F,F_c=convert2("len",F_op,F)
        F=F*39.37
        F_c+="*39.37"
      
      q_c=""
      if q_op != 'gr' :
        q,q_c=convert2("mass",q_op,q)
        q=q*15432
        q=q/1000
        q_c+=" *15432"
      
      
      #Ia=Ib-(F-30)*10-r/3+min(0,-(q-5*p/3))
      r=(Ib+(F-30)*10-Ia+min(0,-(q-5*p)/3))*3
      
      
      
      if not((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000) or (Ib<=-1 and Ib>=-10000)):
             if Ib!=0: 
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        Ib=round(Ib,3)    

     
      if not((Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000) or (Ia<=-1 and Ia>=-10000)):
             if Ia!=0: 
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        Ia=round(Ia,3)    
 

     
      if not((p>=1 and p<=10000) or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000) or (p<=-1 and p>=-10000)):
             if p!=0: 
              base1,power1=Roundoff(p)
              p=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        p=round(p,3)    

             
      
      
      if not((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000) or (F<=-1 and F>=-10000)):
             if F!=0: 
              base1,power1=Roundoff(F)
              F=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        F=round(F,3)    
   


      if not((q>=1 and q<=10000) or (round(q,3)!=0 and round(q,3)!=0.001 and q<=10000) or (q<=-1 and q>=-10000)):
             if q!=0: 
              base1,power1=Roundoff(q)
              q=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        q=round(q,3)    
    
      

      if not((r>=1 and r<=10000) or (round(r,3)!=0 and round(r,3)!=0.001 and r<=10000) or (r<=-1 and r>=-10000)):
             if r!=0: 
              base1,power1=Roundoff(r)
              r=f"{base1} X 10 "+add_tags('sup',power1)
      else:  
        r=round(r,3)    
            


      context={
         'given_data':given_data,
         'id':1,
         'Ia':Ia,
         'Ib':Ib,
         'F':F,
         'r':r,
         'p':p,
         'q':q,
         'Ib1':Ib1,
         'Ia1':Ia1,
         'q1':q1,
         'F1':F1,
         'p1':p1,
         'Ia_op':Ia_op,
         'F_op':F_op,
         'p_op':p_op,
         'r_op':r_op,
         'q_op':q_op,
         'Ib_op':Ib_op,
        'Ia_c':Ia_c,
         'Ib_c':Ib_c,
         'F_c':F_c,
         'p_c':p_c,
         'q_c':q_c,


      }
      return render(request,'arrowspeedcalculator.html',context)
      

    else:
     return render(request,'arrowspeedcalculator.html',{'given_data':given_data,'F1':12,'Ia1':9,'Ib1':9,'p1':6,'q1':5,'r1':11,'id1':2})
    
  else:
    return render(request,'arrowspeedcalculator.html',{'given_data':'form1','F1':12,'Ia1':9,'Ib1':9,'p1':6,'q1':5,'r1':11,'id1':2})




def frictionlosscalculator(request):
  """Here Ib is for the pipe length
     Here Ia is for the pipe inside diameter
     Here F is for the friction head loss
     Here mat_op is for the pipe material
     Here flow is for the flow rate of fluid
     Here c is for the Specific heat capacity of material
  """
  if request.method=="POST":
    given_data=request.POST.get('given_data')
    #Obtaining the Ia
    if request.POST.get('Ia')!=None and request.POST.get('Ia')!='' :     
              inp=str(request.POST.get('Ia'))
              if inp.isdigit():
                  Ia=int(request.POST.get('Ia'))
              else:
                  Ia=float(request.POST.get('Ia'))
    else:
       Ia=None
    
    #Obtaining the Ib
    if request.POST.get('Ib')!=None and request.POST.get('Ib')!='' :     
              inp=str(request.POST.get('Ib'))
              if inp.isdigit():
                  Ib=int(request.POST.get('Ib'))
              else:
                  Ib=float(request.POST.get('Ib'))
    else:
       Ib=None

   #Obtaining the F 
    if request.POST.get('F')!=None and request.POST.get('F')!='' :     
              inp=str(request.POST.get('F'))
              if inp.isdigit():
                  F=int(request.POST.get('F'))
              else:
                  F=float(request.POST.get('F'))
    else:
       F=None

    form=False

   #Obtaining the flow 
    if request.POST.get('flow')!=None and request.POST.get('flow')!='' :     
              inp=str(request.POST.get('flow'))
              if inp.isdigit():
                  flow=int(request.POST.get('flow'))
              else:
                  flow=float(request.POST.get('flow'))
    else:
       flow=None

    #OBTAINING THE MATERIAL
    mat_op=request.POST.get("mat_op")
  
    form=False
    if "f1" in request.POST:
      form=True
    
     
     #FORM 1
    if given_data=='form1' and form:  
      #Copying of variables
      Ia1=Ia
      Ib1=Ib
      flow1=flow
      
      #Specific heat capacity of material
      c=materialValueCalculator(mat_op)

      #Units
      Ia_op=request.POST.get('Ia_op')
      Ib_op=request.POST.get('Ib_op')
      flow_op=request.POST.get('flow_op')

      #Conversion of units
      #F,F_c=convert2("len",F_op,F)
      Ia,Ia_c=convert2("len",Ia_op,Ia)
      Ib,Ib_c=convert2("len",Ib_op,Ib)
      flow,flow_c=convert2("flow",flow_op,flow)
      
      #Calculation
      v1=flow**1.852
      v2=int(c)**1.852
      v3=Ia**4.87

      
      F=10.67*Ib*v1/(v2*v3)

      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
       
      if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
         base1,power1=Roundoff(Ib)
         Ib=f"{base1} X 10"+add_tags('sup',power1)
      else:
         Ib=round(Ib,5) 
       
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
      else:
         F=round(F,5)  
      
      if not  ((flow>=1 and flow<=10000) or (round(flow,3)!=0 and round(flow,3)!=0.001 and flow<=10000)):
         base1,power1=Roundoff(flow)
         flow=f"{base1} X 10"+add_tags('sup',power1)
      else:
         flow=round(flow,5)

      A=""
      B=""
      for i in range(0,len(flow_op)):
        if flow_op[i]=="/":      
           break
        A+= flow_op[i]
      
      for j in range(i,len(flow_op)):
        B+= flow_op[j]
      

      context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'flow':flow,
          'Ia1':Ia1,
          'Ib1':Ib1,
          'flow1':flow1,
          'Ia_op':Ia_op,
          'Ib_op':Ib_op,
          'flow_op':flow_op,
          'mat_op':mat_op,
          'c':c,
          'id':1,
          'given_data':given_data,
          #'F_c':F_c,
          'Ia_c':Ia_c,
          'Ib_c':Ib_c,
          'flow_c':flow_c,
          'A':A,
          'B':B
      }
      return render(request,'frictionlosscalculator.html',context)


    #FORM 2
    elif given_data=='form2' and form:  
      #Copying of variables
      F1=F
      Ib1=Ib
      flow1=flow
      
      #Specific heat capacity of material
      c=materialValueCalculator(mat_op)

      #Units
      F_op=request.POST.get('F_op')
      Ib_op=request.POST.get('Ib_op')
      flow_op=request.POST.get('flow_op')

      #Conversion of units
      F,F_c=convert2("len",F_op,F)
      Ib,Ib_c=convert2("len",Ib_op,Ib)
      flow,flow_c=convert2("flow",flow_op,flow)
     
      #Calculation
      v1=flow**1.857
      v2=int(c)**1.857
      v3=10.67*Ib*v1/(v2*F)
      Ia=v3**(1/4.87)
      
      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
       
      if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
         base1,power1=Roundoff(Ib)
         Ib=f"{base1} X 10"+add_tags('sup',power1)
      else:
         Ib=round(Ib,5) 
       
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
      else:
         F=round(F,5)  
      
      if not  ((flow>=1 and flow<=10000) or (round(flow,3)!=0 and round(flow,3)!=0.001 and flow<=10000)):
         base1,power1=Roundoff(flow)
         flow=f"{base1} X 10"+add_tags('sup',power1)
      else:
         flow=round(flow,5)
      
      A=""
      B=""
      for i in range(0,len(flow_op)):
        if flow_op[i]=="/":      
           break
        A+= flow_op[i]
      
      for j in range(i,len(flow_op)):
        B+= flow_op[j]
                     

      context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'flow':flow,
          'F1':F1,
          'Ib1':Ib1,
          'flow1':flow1,
          'F_op':F_op,
          'Ib_op':Ib_op,
          'flow_op':flow_op,
          'mat_op':mat_op,
          'c':c,
          'id':1,
          'given_data':given_data,
          'F_c':F_c,
          'Ib_c':Ib_c,
          'flow_c':flow_c,
          'A':A,
          'B':B
      }
      return render(request,'frictionlosscalculator.html',context)


    elif given_data=='form3' and form:  
      #Copying of variables
      Ia1=Ia
      F1=F
      flow1=flow
      
      #Specific heat capacity of material
      c=materialValueCalculator(mat_op)

      #Units
      Ia_op=request.POST.get('Ia_op')
      F_op=request.POST.get('F_op')
      flow_op=request.POST.get('flow_op')


      #Conversion of units
      F,F_c=convert2("len",F_op,F)
      Ia,Ia_c=convert2("len",Ia_op,Ia)
      flow,flow_c=convert2("flow",flow_op,flow)
     
      #Calculation
      v1=flow**1.852
      v2=int(c)**1.852
      v3=Ia**4.87

      #F=10.67*Ib*v1/(v2*v3)
      Ib=F*v2*v3/(10.67*v1)

      
      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
       
      if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
         base1,power1=Roundoff(Ib)
         Ib=f"{base1} X 10"+add_tags('sup',power1)
      else:
         Ib=round(Ib,5) 
       
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
      else:
         F=round(F,5)  
      
      if not  ((flow>=1 and flow<=10000) or (round(flow,3)!=0 and round(flow,3)!=0.001 and flow<=10000)):
         base1,power1=Roundoff(flow)
         flow=f"{base1} X 10"+add_tags('sup',power1)
      else:
         flow=round(flow,5)   

      A=""
      B=""
      for i in range(0,len(flow_op)):
        if flow_op[i]=="/":      
           break
        A+= flow_op[i]
      
      for j in range(i,len(flow_op)):
        B+= flow_op[j]
       


      context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'flow':flow,
          'Ia1':Ia1,
          'F1':F1,
          'flow1':flow1,
          'Ia_op':Ia_op,
          'F_op':F_op,
          'flow_op':flow_op,
          'mat_op':mat_op,
          'c':c,
          'id':1,
          'given_data':given_data,
          'F_c':F_c,
          'Ia_c':Ia_c,
          'flow_c':flow_c,
          'A':A,
          'B':B
      }
      return render(request,'frictionlosscalculator.html',context)

    elif given_data=='form4' and form:  
      #Copying of variables
      Ia1=Ia
      Ib1=Ib
      F1=F
      
      #Specific heat capacity of material
      c=materialValueCalculator(mat_op)

      #Units
      Ia_op=request.POST.get('Ia_op')
      Ib_op=request.POST.get('Ib_op')
      F_op=request.POST.get('F_op')

      #Conversion of units
      F,F_c=convert2("len",F_op,F)
      Ia,Ia_c=convert2("len",Ia_op,Ia)
      Ib,Ib_c=convert2("len",Ib_op,Ib)
      
      #Calculation
      
      #v1=flow**1.8
      v2=int(c)**1.852
      v3=Ia**4.87
      #F=10.67*Ib*v1/(v2*v3)
      v1=F*v2*v3/(10.67*Ib)
      flow=v1**(1/1.852)
      
      
      if not ( (Ia>=1 and Ia<=10000) or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
         base1,power1=Roundoff(Ia)
         Ia=f"{base1} X 10 "+add_tags('sup',power1)
      else:
        Ia=round(Ia,5)
       
      if not  ((Ib>=1 and Ib<=10000) or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
         base1,power1=Roundoff(Ib)
         Ib=f"{base1} X 10"+add_tags('sup',power1)
      else:
         Ib=round(Ib,5) 
       
      if not  ((F>=1 and F<=10000) or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
         base1,power1=Roundoff(F)
         F=f"{base1} X 10"+add_tags('sup',power1)
      else:
         F=round(F,5)  
      
      if not  ((flow>=1 and flow<=10000) or (round(flow,3)!=0 and round(flow,3)!=0.001 and flow<=10000)):
         base1,power1=Roundoff(flow)
         flow=f"{base1} X 10"+add_tags('sup',power1)
      else:
         flow=round(flow,5)   


      
      context={
          'F':F,
          'Ia':Ia,
          'Ib':Ib,
          'flow':flow,
          'Ia1':Ia1,
          'Ib1':Ib1,
          'F1':F1,
          'Ia_op':Ia_op,
          'Ib_op':Ib_op,
          'F_op':F_op,
          'mat_op':mat_op,
          'c':c,
          'id':1,
          'given_data':given_data,
          'F_c':F_c,
          'Ia_c':Ia_c,
          'Ib_c':Ib_c,
          
      }
      return render(request,'frictionlosscalculator.html',context)
        
    
    
    else:
        return render(request,'frictionlosscalculator.html',{'given_data':given_data}) 
  
  else:
    return render(request,'frictionlosscalculator.html',{'given_data':'form1'})
  





#CODE FOR THE VOLATGE DIVIDER CALCULATOR

def voltagedividercalculator(request):
  if request.method=='POST':
      given_data=request.POST.get('given_data')
      given_option=request.POST.get('given_option')
      
      #VALUE FOR THE RESISTANCE 1
      if request.POST.get('Ia')!=None and request.POST.get('Ia')!='' :     
        inp=str(request.POST.get('Ia'))
        if inp.isdigit():
           Ia=int(request.POST.get('Ia'))
        else:
           Ia=float(request.POST.get('Ia'))
      else:
         Ia=None

      #VALUE FOR THE RESISTANCE 2
      if request.POST.get('Ib')!=None and request.POST.get('Ib')!='':
        inp=str(request.POST.get('Ib'))
        if inp.isdigit():
            Ib=int(request.POST.get('Ib'))
        else:
            Ib=float(request.POST.get('Ib'))
      else:
        Ib=None

      #VALUE FOR THE OUTPUT VOLTAGE
      if request.POST.get('F')!=None and request.POST.get('F')!='':
        inp=str(request.POST.get('F'))
        if inp.isdigit():
           F=int(request.POST.get('F'))
        else:
           F=float(request.POST.get('F'))
      else:
        F=None
      
      #VALUE FOR THE INPUT VOLTAGE 
      if request.POST.get('d')!=None and request.POST.get('d')!='':
        inp=str(request.POST.get('d'))
        if inp.isdigit():
            d=int(request.POST.get('d'))
        else:
             d=float(request.POST.get('d'))
      else:
        d=None

      form=False
      if "f1" in request.POST:
        form=True  

      if given_option=='RR':
          unit=str(request.POST.get('Ia_op'))
          ch=unit[len(unit)-1]
          
          if given_data=='form1'  and form:
            #Copying the variables
            Ia1=Ia
            Ib1=Ib
            d1=d 

            #Fetching the units  
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')
            

            #Conversion of units
            Ia,Ia_c=convert2("res",Ia_op,Ia)
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            
            #Calculation
            F=Ib*d/(Ia+Ib)
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)


            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'd1':d1,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'Ia_c':Ia_c,
              'Ib_c':Ib_c,
              'd_c':d_c,
             }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form4'  and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            Ib1=Ib

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')

            #Conversion of units

            Ia,Ia_c=convert2("res",Ia_op,Ia)
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            F,F_c=convert2("volt",F_op,F)

            #Calculation
            d=F*(Ia+Ib)/Ib

            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
 

            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'Ia_c':Ia_c,
              'Ib_c':Ib_c,
              'F_c':F_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form3'  and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            d1=d

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            d_op=request.POST.get('d_op')

            #Conversion of units
            Ia,Ia_c=convert2("res",Ia_op,Ia)
            d,d_c=convert2("volt",d_op,d)
            F,F_c=convert2("volt",F_op,F)
            #Calculation
            Ib=F*Ia/(d-F)
           
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)


            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'd1':d1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'Ia_c':Ia_c,
              'F_c':F_c,
              'd_c':d_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form2' and form:
            #Copying the variables
            F1=F
            Ib1=Ib
            d1=d
            
            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')

            #Conversion of units
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            F,F_c=convert2("volt",F_op,F)
            

            #Calculation
            Ia=Ib*d/F -Ib
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)


            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ib1':Ib1,
              'd1':d1,
              'F_op':F_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'Ib_c':Ib_c,
              'F_c':F_c,
              'd_c':d_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)
                          
          else:
            if given_data==None:
              given_data='form1'  
            return render(request,'voltagedividercalculator.html',{'given_data':given_data,'given_option':given_option})
      

      elif given_option=='CC':
          unit=str(request.POST.get('Ia_op'))
          ch=unit[len(unit)-1]
          
          if given_data=='form1'  and form:
            #Copying the variables
            Ia1=Ia
            Ib1=Ib
            d1=d 

            #Fetching the units  
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')

            #Conversion of units
            Ia,Ia_c=convert2("cap",Ia_op,Ia)
            Ib,Ib_c=convert2("cap",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            #F=convert2("volt",F_op,F) 
            #Calculation
            F=d*Ia/(Ia+Ib)
           
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
           
      
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'd1':d1,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1, 
              'Ia_c':Ia_c,
              'Ib_c':Ib_c,
              'd_c':d_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form4'  and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            Ib1=Ib

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')

            #Conversion of units
            
            Ia,Ia_c=convert2("cap",Ia_op,Ia)
            Ib,Ib_c=convert2("cap",Ib_op,Ib)
            F,F_c=convert2("volt",F_op,F) 

            #Calculation
            d=F*(Ia+Ib)/Ia
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
           
      
            
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'Ia_c':Ia_c,
              'Ib_c':Ib_c,
              'F_c':F_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form3'  and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            d1=d

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            d_op=request.POST.get('d_op')

            #Conversion of units
            Ia,Ia_c=convert2("cap",Ia_op,Ia)
            d,d_c=convert2("volt",d_op,d)
            F,F_c=convert2("volt",F_op,F) 
          
            #Calculation
            Ib=Ia*d/F -Ia
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
           
      
            
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'd1':d1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'Ia_c':Ia_c,
              'F_c':F_c,
              'd_c':d_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form2' and form:
            #Copying the variables
            F1=F
            Ib1=Ib
            d1=d
            
            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')

            #Conversion of units
            Ib,Ib_c=convert2("cap",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            F,F_c=convert2("volt",F_op,F) 

            #Calculation
            Ia=F*Ib/(d-F)

            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
           
      
            
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ib1':Ib1,
              'd1':d1,
              'F_op':F_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'Ib_c':Ib_c,
              'F_c':F_c,
              'd_c':d_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)
                          
          else:
            if given_data==None:
              given_data='form1'  
            return render(request,'voltagedividercalculator.html',{'given_data':given_data,'given_option':given_option})
      
      
      
      elif given_option=='LL':
          unit=str(request.POST.get('Ia_op'))
          ch=unit[len(unit)-1]
          
          if given_data=='form1' and form:
            #Copying the variables
            Ia1=Ia
            Ib1=Ib
            d1=d 

            #Fetching the units  
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')

            #Conversion of units
            Ia,Ia_c=convert2("ind",Ia_op,Ia)
            Ib,Ib_c=convert2("ind",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            #F,F_c=convert2("volt",F_op,F)
          
            #Calculation
            F=Ib*d/(Ia+Ib)

            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
           
            
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'd1':d1,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'Ia_c':Ia_c,
              'd_c':d_c,
              'Ib_c':Ib_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form4'  and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            Ib1=Ib

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')

            #Conversion of units
            Ia,Ia_c=convert2("ind",Ia_op,Ia)
            Ib,Ib_c=convert2("ind",Ib_op,Ib)
            #d,d_c=convert2("volt",d_op,d)
            F,F_c=convert2("volt",F_op,F)
          

            #Calculation
            d=F*(Ia+Ib)/Ib
            
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
           
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,              
              'Ia_c':Ia_c,
              'F_c':F_c,
              'Ib_c':Ib_c,
            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form3'  and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            d1=d

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            d_op=request.POST.get('d_op')

            #Conversion of units
            Ia,Ia_c=convert2("ind",Ia_op,Ia)
            d,d_c=convert2("volt",d_op,d)
            F,F_c=convert2("volt",F_op,F)
          
            #Calculation
            Ib=F*Ia/(d-F)
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
           
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'd1':d1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,              
              'Ia_c':Ia_c,
              'F_c':F_c,
              'd_c':d_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form2' and form:
            #Copying the variables
            F1=F
            Ib1=Ib
            d1=d
            
            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')

            #Conversion of units
            Ib,Ib_c=convert2("ind",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            F,F_c=convert2("volt",F_op,F)
          

            #Calculation
            Ia=Ib*d/F -Ib
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)
           
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ib1':Ib1,
              'd1':d1,
              'F_op':F_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'id':1,
              'F_c':F_c,
              'd_c':d_c,
              'Ib_c':Ib_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)
                          
          else:
            if given_data==None:
              given_data='form1'  
            return render(request,'voltagedividercalculator.html',{'given_data':given_data,'given_option':given_option})


        
      elif given_option=='RC':
          unit=str(request.POST.get('p_op'))
          if given_data!="form5":
           ch=unit[len(unit)-1]
          else:
            ch='z' 
        
          if request.POST.get('p')!=None and request.POST.get('p')!='' :     
              inp=str(request.POST.get('p'))
              if inp.isdigit():
                  p=int(request.POST.get('p'))
              else:
                  p=float(request.POST.get('p'))
          else:
               p=None

          
          if given_data=='form1'  and form:
            #Copying the variables
            Ia1=Ia
            Ib1=Ib
            d1=d 
            p1=p

            #Fetching the units  
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')
            p_op=request.POST.get('p_op')

            #Conversion of units
            Ia,Ia_c=convert2("cap",Ia_op,Ia)
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            p,p_c=convert2("freq",p_op,p)
            
          
            #Calculation
            val=( (2*math.pi*Ia*Ib*p)**2 +1 )**0.5
            F=d/val
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)

            
            if not  (p>=1 and p<=10000 or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
              base1,power1=Roundoff(p)
              p=f"{base1} X 10"+add_tags('sup',power1)
            else:
              p=round(p,4)  
           

            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'd1':d1,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
              'p1':p1,
              'p_op':p_op,
              'id':1,              
              'Ia_c':Ia_c,
              'd_c':d_c,
              'Ib_c':Ib_c,
              'p_c':p_c
            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form4'  and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            Ib1=Ib
            p1=p

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')
            p_op=request.POST.get('p_op')

            #Conversion of units
            Ia,Ia_c=convert2("cap",Ia_op,Ia)
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            p,p_c=convert2("freq",p_op,p)
            F,F_c=convert2("volt",F_op,F)
          
            #Calculation
            val=((2*math.pi*Ia*Ib*p)**2+1)**0.5
            d=F*val
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)

            
            if not  (p>=1 and p<=10000 or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
              base1,power1=Roundoff(p)
              p=f"{base1} X 10"+add_tags('sup',power1)
            else:
              p=round(p,4)  
           
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'given_data':given_data,
              'given_option':given_option,
               'p':p,
               'p_op':p_op,
               'p1':p1,
               'id':1,    
              'Ia_c':Ia_c,
              'F_c':F_c,
              'Ib_c':Ib_c,
              'p_c':p_c

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form3' and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            d1=d
            p1=p

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            d_op=request.POST.get('d_op')
            p_op=request.POST.get('p_op')

            #Conversion of units
            Ia,Ia_c=convert2("cap",Ia_op,Ia)
            d,d_c=convert2("volt",d_op,d)
            p,p_c=convert2("freq",p_op,p)
            F,F_c=convert2("volt",F_op,F)

            if F>=d:
               context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'd1':d1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
              'p1':p1,
              'p_op':p_op,
              'message':"Output voltage cannot be greater than or equal to input volatge"
               }
               return render(request,'voltagedividercalculator.html',context)

               
            #Calculation
            Ib=(d*d/(F*F)-1)**0.5/(2*math.pi*Ia*p)
            
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)

            
            if not  (p>=1 and p<=10000 or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
              base1,power1=Roundoff(p)
              p=f"{base1} X 10"+add_tags('sup',power1)
            else:
              p=round(p,4)  
           
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'd1':d1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
              'p_op':p_op,
              'p1':p1,
              'id':1,  
              'Ia_c':Ia_c,
              'F_c':F_c,
              'd_c':d_c,
              'p_c':p_c

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form2' and form:
            #Copying the variables
            F1=F
            Ib1=Ib
            d1=d
            p1=p
            
            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')
            p_op=request.POST.get('p_op')

            #Conversion of units
            
           
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            p,p_c=convert2("freq",p_op,p)
            F,F_c=convert2("volt",F_op,F)
            
            if F>=d:
               context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ib1':Ib1,
              'd1':d1,
              'F_op':F_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
              'p1':p1,
              'p_op':p_op,
              'message':"Output voltage cannot be greater than or equal to input volatge"
               }
               return render(request,'voltagedividercalculator.html',context)


            #Calculation
            val=(abs( (d/F)**2 -1))**0.5
            Ia=val/(2*math.pi*p*Ib)
          
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)

            
            if not  (p>=1 and p<=10000 or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
              base1,power1=Roundoff(p)
              p=f"{base1} X 10"+add_tags('sup',power1)
            else:
              p=round(p,4)  
           
            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ib1':Ib1,
              'd1':d1,
              'F_op':F_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
               'p_op':p_op,
               'p1':p1,
               'id':1,
              'F_c':F_c,
              'd_c':d_c,
              'Ib_c':Ib_c,
              'p_c':p_c

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

          
            
          elif given_data=='form5' and form:
            #Copying the variables
            F1=F
            Ib1=Ib
            d1=d
            Ia1=Ia
            
            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')
            Ia_op=request.POST.get('Ia_op')

            #Conversion of units
            Ia,Ia_c=convert2("cap",Ia_op,Ia)
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            F,F_c=convert2("volt",F_op,F)

            
            if F>=d:
               context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'd1':d1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
              'Ib1':Ib1,
              'Ib_op':Ib_op,
              'message':"Output voltage cannot be greater than or equal to input volatge"
               }
               return render(request,'voltagedividercalculator.html',context)

          
            #Calculation
            val=((d/F)**2-1)**0.5
            p=val/(math.pi*2*Ia*Ib)
            
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)

            
            if not  (p>=1 and p<=10000 or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
              base1,power1=Roundoff(p)
              p=f"{base1} X 10"+add_tags('sup',power1)
            else:
              p=round(p,4)  
           

            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ib1':Ib1,
              'd1':d1,
              'Ia1':Ia1,
              'Ia_op':Ia_op,
              'F_op':F_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
               'id':1, 
              'Ia_c':Ia_c,
              'F_c':F_c,
              'd_c':d_c,
              'Ib_c':Ib_c,

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)
                          

          else:
            if given_data==None:
              given_data='form1'  
            return render(request,'voltagedividercalculator.html',{'given_data':given_data,'given_option':given_option})


      elif given_option=='RL':
          unit=str(request.POST.get('p_op'))
          if given_data!="form5":
           ch=unit[len(unit)-1]
          else:
            ch='z' 
        
          if request.POST.get('p')!=None and request.POST.get('p')!='' :     
              inp=str(request.POST.get('p'))
              if inp.isdigit():
                  p=int(request.POST.get('p'))
              else:
                  p=float(request.POST.get('p'))
          else:
               p=None

          
          if given_data=='form1' and form:
            #Copying the variables
            Ia1=Ia
            Ib1=Ib
            d1=d 
            p1=p

            #Fetching the units  
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')
            d_op=request.POST.get('d_op')
            p_op=request.POST.get('p_op')


            #Conversion of units
            Ia,Ia_c=convert2("ind",Ia_op,Ia)
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            d,d_c=convert2("volt",d_op,d)
            p,p_c=convert2("freq",p_op,p)
          
          
            #Calculation
            val=2*math.pi*Ia*p
            F=val*d/(Ib*Ib+val*val)**0.5
            
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)

            
            if not  (p>=1 and p<=10000 or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
              base1,power1=Roundoff(p)
              p=f"{base1} X 10"+add_tags('sup',power1)
            else:
              p=round(p,4)  
           


            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'd1':d1,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
              'p1':p1,
              'p_op':p_op,
              'id':1,
              'Ia_c':Ia_c,
              'Ib_c':Ib_c,
              'd_c':d_c,
              'p_c':p_c

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form4'  and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            Ib1=Ib
            p1=p

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            Ib_op=request.POST.get('Ib_op')
            p_op=request.POST.get('p_op')

            #Conversion of units
            Ia,Ia_c=convert2("ind",Ia_op,Ia)
            Ib,Ib_c=convert2("res",Ib_op,Ib)
            p,p_c=convert2("freq",p_op,p)
            F,F_c=convert2("volt",F_op,F)
          
            #Calculation
            val=2*math.pi*Ia*p
            #F=val*d/(Ib*Ib+val*val)**0.5
            d=(Ib*Ib+val*val)**0.5*F/val
            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)

            
            if not  (p>=1 and p<=10000 or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
              base1,power1=Roundoff(p)
              p=f"{base1} X 10"+add_tags('sup',power1)
            else:
              p=round(p,4)  
           

            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'Ib1':Ib1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'Ib_op':Ib_op,
              'given_data':given_data,
              'given_option':given_option,
               'p':p,
               'p_op':p_op,
               'p1':p1,
               'id':1,
              'Ia_c':Ia_c,
              'Ib_c':Ib_c,
              'F_c':F_c,
              'p_c':p_c

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

            
          elif given_data=='form3' and form:
            #Copying the variables
            F1=F
            Ia1=Ia
            d1=d
            p1=p

            #Fetching the units  
            F_op=request.POST.get('F_op')
            Ia_op=request.POST.get('Ia_op')
            d_op=request.POST.get('d_op')
            p_op=request.POST.get('p_op')

            #Conversion of units
            Ia,Ia_c=convert2("ind",Ia_op,Ia)
            d,d_c=convert2("volt",d_op,d)
            p,p_c=convert2("freq",p_op,p)
            F,F_c=convert2("volt",F_op,F)
          
            #Calculation
            val=2*math.pi*Ia*p
            #F=val*d/(Ib*Ib+val*val)**0.5

            Ib=( (val*d/F)**2-val*val)**0.5
            if isinstance(Ib, complex):
             context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'd1':d1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
              'p_op':p_op,
              'p1':p1,
              'message':"Enter valid data"
            }
             return render(request,'voltagedividercalculator.html',context)

            
            if not  (Ia>=1 and Ia<=10000 or (round(Ia,3)!=0 and round(Ia,3)!=0.001 and Ia<=10000)):
              base1,power1=Roundoff(Ia)
              Ia=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ia=round(Ia,4)
          
            if not  (Ib>=1 and Ib<=10000 or (round(Ib,3)!=0 and round(Ib,3)!=0.001 and Ib<=10000)):
              base1,power1=Roundoff(Ib)
              Ib=f"{base1} X 10"+add_tags('sup',power1)
            else:
              Ib=round(Ib,4)


           
            if not  (d>=1 and d<=10000 or (round(d,3)!=0 and round(d,3)!=0.001 and d<=10000)):
              base1,power1=Roundoff(d)
              d=f"{base1} X 10"+add_tags('sup',power1)
            else:
              d=round(d,4)
        
           
            if not  (F>=1 and F<=10000 or (round(F,3)!=0 and round(F,3)!=0.001 and F<=10000)):
              base1,power1=Roundoff(F)
              F=f"{base1} X 10"+add_tags('sup',power1)
            else:
              F=round(F,4)

            
            if not  (p>=1 and p<=10000 or (round(p,3)!=0 and round(p,3)!=0.001 and p<=10000)):
              base1,power1=Roundoff(p)
              p=f"{base1} X 10"+add_tags('sup',power1)
            else:
              p=round(p,4)  
           

            #Passing the variables
            context={
              'F':F,
              'Ia':Ia,
              'Ib':Ib,
              'd':d,
              'F1':F1,
              'Ia1':Ia1,
              'd1':d1,
              'F_op':F_op,
              'Ia_op':Ia_op,
              'd_op':d_op,
              'given_data':given_data,
              'given_option':given_option,
              'p':p,
              'p_op':p_op,
              'p1':p1,
              'id':1,
              'Ia_c':Ia_c,
              'F_c':F_c,
              'd_c':d_c,
              'p_c':p_c

            }

            #Rendering the template
            return render(request,'voltagedividercalculator.html',context)

          else:
            if given_data==None:
              given_data='form1'  
            return render(request,'voltagedividercalculator.html',{'given_data':given_data,'given_option':given_option})  

      
  else:
   return render(request,'voltagedividercalculator.html',{'given_data':'form1','given_option':'RR'})




#CODE FOR THE FREQEUNCY CALCULATOR


def frequencycalcultor(request):
  
  if request.method=='POST':
     
     #FOR GETTING THE FORM
     given_data=request.POST.get('given_data')
     
     #FOR GETTING THE wave velocity
     if request.POST.get('waveVel')!=None and request.POST.get('waveVel')!='' :
              waveVel_op=request.POST.get('waveVel_op')     
              inp=str(request.POST.get('waveVel'))
              if inp.isdigit():
                  waveVel=int(request.POST.get('waveVel'))
              else:
                  waveVel=float(request.POST.get('waveVel'))
              waveVel1=waveVel    
     else:
       waveVel=None
     
     #FOR GETTING THE time
     if request.POST.get('time')!=None and request.POST.get('time')!='' :
              time_op=request.POST.get('time_op')     
              inp=str(request.POST.get('time'))
              if inp.isdigit():
                  time=int(request.POST.get('time'))
              else:
                  time=float(request.POST.get('time'))
              time1=time    
     else:
       time=None

     #FOR GETTING THE WAVELENGTH
     if request.POST.get('wave')!=None and request.POST.get('wave')!='' :
              wave_op=request.POST.get('wave_op')     
              inp=str(request.POST.get('wave'))
              if inp.isdigit():
                  wave=int(request.POST.get('wave'))
              else:
                  wave=float(request.POST.get('wave'))
              wave1=wave    
     else:
       wave=None

     #TO CHECK WHETHER THE FORM IS SUBMITTED OR NOT
     form= False
     if "f1" in request.POST:
       form=True


     if given_data=='form1' and form:    
       
       #Conversion
       time,time_c=convert2('time',time_op,time)
       wave,wave_c=convert2('len',wave_op,wave)
       
       #Calculation
       waveVel=wave/time
       freq=1/time

       if not( (wave>=1 and wave<=10000) or (round(wave,3)!=0 and round(wave,3)!=0.001 and wave<=10000)):
              base1,power1=Roundoff(wave)
              wave=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              wave=round(wave,4)
       
       if not( (time>=1 and time<=10000) or (round(time,3)!=0 and round(time,3)!=0.001 and time<=10000)):
              base1,power1=Roundoff(time)
              time=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              time=round(time,4)

       if not( (waveVel>=1 and waveVel<=10000) or (round(waveVel,3)!=0 and round(waveVel,3)!=0.001 and waveVel<=10000)):
              base1,power1=Roundoff(waveVel)
              waveVel=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              waveVel=round(waveVel,4)
       
       if not( (freq>=1 and freq<=10000) or (round(freq,3)!=0 and round(freq,3)!=0.001 and freq<=10000)):
              base1,power1=Roundoff(freq)
              freq=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              freq=round(freq,4)

       context={
          'waveVel':waveVel,
          'freq':freq,
          'time':time,
          'wave':wave,
          'time1':time1,
          'wave1':wave1,
          'wave_op':wave_op,
          'time_op':time_op,
          'id':1,
          'given_data':given_data,
          'time_c':time_c,
          'wave_c':wave_c,
          }       
       return render(request,'frequencycalcultor.html',context)
     
     
     if given_data=='form2' and form:    
       
       #Conversion
       waveVel,waveVel_c=convert2('vel',waveVel_op,waveVel)
       time,time_c=convert2('time',time_op,time)
       
       #Calculation
       wave=waveVel*time
       freq=1/time

       if not( (wave>=1 and wave<=10000) or (round(wave,3)!=0 and round(wave,3)!=0.001 and wave<=10000)):
              base1,power1=Roundoff(wave)
              wave=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              wave=round(wave,4)
       
       if not( (time>=1 and time<=10000) or (round(time,3)!=0 and round(time,3)!=0.001 and time<=10000)):
              base1,power1=Roundoff(time)
              time=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              time=round(time,4)

       if not( (waveVel>=1 and waveVel<=10000) or (round(waveVel,3)!=0 and round(waveVel,3)!=0.001 and waveVel<=10000)):
              base1,power1=Roundoff(waveVel)
              waveVel=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              waveVel=round(waveVel,4)
       
       if not( (freq>=1 and freq<=10000) or (round(freq,3)!=0 and round(freq,3)!=0.001 and freq<=10000)):
              base1,power1=Roundoff(freq)
              freq=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              freq=round(freq,4)

       context={
          'wave':wave,
          'freq':freq,
          'time':time,
          'waveVel':waveVel,
          'time1':time1,
          'waveVel1':waveVel1,
          'waveVel_op':waveVel_op,
          'time_op':time_op,
          'id':1,
          'given_data':given_data,
          'time_c':time_c,
          'waveVel_c':waveVel_c
       }       
       return render(request,'frequencycalcultor.html',context)


     if given_data=='form3' and form:    
       
       #Conversion
       waveVel,waveVel_c=convert2('vel',waveVel_op,waveVel)
       wave,wave_c=convert2('len',wave_op,wave)
       
       
       #Calculation
       time=wave/waveVel
       freq=1/time

       if not( (wave>=1 and wave<=10000) or (round(wave,3)!=0 and round(wave,3)!=0.001 and wave<=10000)):
              base1,power1=Roundoff(wave)
              wave=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              wave=round(wave,4)
       
       if not( (time>=1 and time<=10000) or (round(time,3)!=0 and round(time,3)!=0.001 and time<=10000)):
              base1,power1=Roundoff(time)
              time=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              time=round(time,4)

       if not( (waveVel>=1 and waveVel<=10000) or (round(waveVel,3)!=0 and round(waveVel,3)!=0.001 and waveVel<=10000)):
              base1,power1=Roundoff(waveVel)
              waveVel=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              waveVel=round(waveVel,4)
       
       if not( (freq>=1 and freq<=10000) or (round(freq,3)!=0 and round(freq,3)!=0.001 and freq<=10000)):
              base1,power1=Roundoff(freq)
              freq=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              freq=round(freq,4)


       context={
          'wave':wave,
          'freq':freq,
          'time':time,
          'waveVel':waveVel,
          'wave1':wave1,
          'waveVel1':waveVel1,
          'waveVel_op':waveVel_op,
          'wave_op':wave_op,
          'id':1,
          'given_data':given_data,
          'wave_c':wave_c,
          'waveVel_c':waveVel_c
       }       
       return render(request,'frequencycalcultor.html',context)
 

     else:
        return render(request,'frequencycalcultor.html',{'given_data':given_data})   
  else:
    return render(request,'frequencycalcultor.html',{'given_data':'form1'})








def circularvelocitycalculator(request):
  
  if request.method=='POST':
     
     #FOR GETTING THE FORM
     given_data=request.POST.get('given_data')
     
     #FOR GETTING THE  velocity
     if request.POST.get('vel')!=None and request.POST.get('vel')!='' :
              vel_op=request.POST.get('vel_op')     
              inp=str(request.POST.get('vel'))
              if inp.isdigit():
                  vel=int(request.POST.get('vel'))
              else:
                  vel=float(request.POST.get('vel'))
              vel1=vel    
     else:
       vel=None
     
     #FOR GETTING THE Time
     if request.POST.get('Time')!=None and request.POST.get('Time')!='' :
              Time_op=request.POST.get('Time_op')     
              inp=str(request.POST.get('Time'))
              if inp.isdigit():
                  Time=int(request.POST.get('Time'))
              else:
                  Time=float(request.POST.get('Time'))
              Time1=Time    
     else:
       Time=None

     #FOR GETTING THE radius
     if request.POST.get('radius')!=None and request.POST.get('radius')!='' :
              radius_op=request.POST.get('radius_op')     
              inp=str(request.POST.get('radius'))
              if inp.isdigit():
                  radius=int(request.POST.get('radius'))
              else:
                  radius=float(request.POST.get('radius'))
              radius1=radius    
     else:
       radius=None

     #TO CHECK WHETHER THE FORM IS SUBMITTED OR NOT
     form= False
     if "f1" in request.POST:
       form=True  


     if given_data=='form1' and form:    
       
       #Conversion
       Time,Time_c=convert2('time',Time_op,Time)
       radius,radius_c=convert2('len',radius_op,radius)
       
       #Calculation
       vel=2*math.pi*radius/Time


       if not( (radius>=1 and radius<=10000) or (round(radius,3)!=0 and round(radius,3)!=0.001 and radius<=10000)):
              base1,power1=Roundoff(radius)
              radius=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              radius=round(radius,4)
       
       if not( (Time>=1 and Time<=10000) or (round(Time,3)!=0 and round(Time,3)!=0.001 and Time<=10000)):
              base1,power1=Roundoff(Time)
              Time=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              Time=round(Time,4)

       if not( (vel>=1 and vel<=10000) or (round(vel,3)!=0 and round(vel,3)!=0.001 and vel<=10000)):
              base1,power1=Roundoff(vel)
              vel=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              vel=round(vel,4)
       

       context={
          'vel':vel,
          'Time':Time,
          'radius':radius,
          'Time1':Time1,
          'radius1':radius1,
          'radius_op':radius_op,
          'Time_op':Time_op,
          'id':1,
          'given_data':given_data,
          'Time_c':Time_c,
          'radius_c':radius_c,
          }       
       return render(request,'circularvelocitycalculator.html',context)
       
     
     elif given_data=='form2' and form:    
       
       #Conversion
       vel,vel_c=convert2('vel',vel_op,vel)
       Time,Time_c=convert2('time',Time_op,Time)
       
       #Calculation
       radius=vel*Time/(2*math.pi)
       

       if not( (radius>=1 and radius<=10000) or (round(radius,3)!=0 and round(radius,3)!=0.001 and radius<=10000)):
              base1,power1=Roundoff(radius)
              radius=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              radius=round(radius,4)
       
       if not( (Time>=1 and Time<=10000) or (round(Time,3)!=0 and round(Time,3)!=0.001 and Time<=10000)):
              base1,power1=Roundoff(Time)
              Time=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              Time=round(Time,4)

       if not( (vel>=1 and vel<=10000) or (round(vel,3)!=0 and round(vel,3)!=0.001 and vel<=10000)):
              base1,power1=Roundoff(vel)
              vel=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              vel=round(vel,4)

       context={
          'radius':radius,
          'Time':Time,
          'vel':vel,
          'Time1':Time1,
          'vel1':vel1,
          'vel_op':vel_op,
          'Time_op':Time_op,
          'id':1,
          'given_data':given_data,
          'Time_c':Time_c,
          'vel_c':vel_c
       }       
       return render(request,'circularvelocitycalculator.html',context)

     

     elif given_data=='form3' and form:    
       
       #Conversion
       vel,vel_c=convert2('vel',vel_op,vel)
       radius,radius_c=convert2('len',radius_op,radius)
       
       
       #Calculation
       Time=2*math.pi*radius/vel
       

       if not( (radius>=1 and radius<=10000) or (round(radius,3)!=0 and round(radius,3)!=0.001 and radius<=10000)):
              base1,power1=Roundoff(radius)
              radius=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              radius=round(radius,4)
       
       if not( (Time>=1 and Time<=10000) or (round(Time,3)!=0 and round(Time,3)!=0.001 and Time<=10000)):
              base1,power1=Roundoff(Time)
              Time=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              Time=round(Time,4)

       if not( (vel>=1 and vel<=10000) or (round(vel,3)!=0 and round(vel,3)!=0.001 and vel<=10000)):
              base1,power1=Roundoff(vel)
              vel=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              vel=round(vel,4)
       
       

       context={
          'radius':radius,
          'Time':Time,
          'vel':vel,
          'radius1':radius1,
          'vel1':vel1,
          'vel_op':vel_op,
          'radius_op':radius_op,
          'id':1,
          'given_data':given_data,
          'radius_c':radius_c,
          'vel_c':vel_c
       }       
       return render(request,'circularvelocitycalculator.html',context)
    

     else: 
          return render(request,'circularvelocitycalculator.html',{'given_data':given_data})


  else:
   return render(request,'circularvelocitycalculator.html',{'given_data':'form1'})



#FUNCTION FOR THE ENGINE HORSEPOWER CALCULATOR

def enginehorsepowercalculator(request):
   
  if request.method=='POST':
     
     #FOR GETTING THE FORM
     given_data=request.POST.get('given_data')
     
     #FOR GETTING THE  HORSEPOWER
     if request.POST.get('hp')!=None and request.POST.get('hp')!='' :
              hp_op=request.POST.get('hp_op')     
              inp=str(request.POST.get('hp'))
              if inp.isdigit():
                  hp=int(request.POST.get('hp'))
              else:
                  hp=float(request.POST.get('hp'))
              hp1=hp    
     else:
       hp=None
     
     #FOR GETTING THE ET
     if request.POST.get('ET')!=None and request.POST.get('ET')!='' :
              ET_op=request.POST.get('ET_op')     
              inp=str(request.POST.get('ET'))
              if inp.isdigit():
                  ET=int(request.POST.get('ET'))
              else:
                  ET=float(request.POST.get('ET'))
              ET1=ET    
     else:
       ET=None

     #FOR GETTING THE weight
     if request.POST.get('weight')!=None and request.POST.get('weight')!='' :
              weight_op=request.POST.get('weight_op')     
              inp=str(request.POST.get('weight'))
              if inp.isdigit():
                  weight=int(request.POST.get('weight'))
              else:
                  weight=float(request.POST.get('weight'))
              weight1=weight    
     else:
       weight=None

     #TO CHECK WHETHER THE FORM IS SUBMITTED OR NOT
     form= False
     if "f1" in request.POST:
       form=True  


     if given_data=='form1' and form:    
       
       #Conversion
       ET,ET_c=convert2('time',ET_op,ET)
       weight,weight_c=convert2('mass',weight_op,weight)
       weight=weight*0.00220462

       if weight_op=="kg":
         weight_c="*2.20462"
       elif weight_op=="t":
          weight_c="*2204.62"    
      

       hp=weight/(ET/5.825)**3


       if not( (weight>=1 and weight<=10000) or (round(weight,3)!=0 and round(weight,3)!=0.001 and weight<=10000)):
              base1,power1=Roundoff(weight)
              weight=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              weight=round(weight,4)
       
       if not( (ET>=1 and ET<=10000) or (round(ET,3)!=0 and round(ET,3)!=0.001 and ET<=10000)):
              base1,power1=Roundoff(ET)
              ET=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              ET=round(ET,4)

       if not( (hp>=1 and hp<=10000) or (round(hp,3)!=0 and round(hp,3)!=0.001 and hp<=10000)):
              base1,power1=Roundoff(hp)
              hp=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              hp=round(hp,4)
       

       context={
          'hp':hp,
          'ET':ET,
          'weight':weight,
          'ET1':ET1,
          'weight1':weight1,
          'weight_op':weight_op,
          'ET_op':ET_op,
          'id':1,
          'given_data':given_data,
          'ET_c':ET_c,
          'weight_c':weight_c,
          }       
       return render(request,'enginehorsepowercalculator.html',context)

          
     elif given_data=='form2' and form:    
       
       #Conversion
       ET,ET_c=convert2('time',ET_op,ET)
       
       hp_c=""
       if hp_op=='watt':
         hp/=745.69
         hp_c="/745.69"

       #Calculation
       weight=hp*(ET/5.825)**3
       

       if not( (weight>=1 and weight<=10000) or (round(weight,3)!=0 and round(weight,3)!=0.001 and weight<=10000)):
              base1,power1=Roundoff(weight)
              weight=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              weight=round(weight,4)
       
       if not( (ET>=1 and ET<=10000) or (round(ET,3)!=0 and round(ET,3)!=0.001 and ET<=10000)):
              base1,power1=Roundoff(ET)
              ET=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              ET=round(ET,4)

       if not( (hp>=1 and hp<=10000) or (round(hp,3)!=0 and round(hp,3)!=0.001 and hp<=10000)):
              base1,power1=Roundoff(hp)
              hp=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              hp=round(hp,4)

       context={
          'weight':weight,
          'ET':ET,
          'hp':hp,
          'ET1':ET1,
          'hp1':hp1,
          'hp_op':hp_op,
          'ET_op':ET_op,
          'id':1,
          'given_data':given_data,
          'ET_c':ET_c,
          'hp_c':hp_c
       }       
       return render(request,'enginehorsepowercalculator.html',context)

     
     elif given_data=='form3' and form:    
       
       #Conversion
       
       weight,weight_c=convert2('mass',weight_op,weight)
       weight=weight*0.00220462

       if weight_op=="kg":
         weight_c="*2.20462"
       elif weight_op=="t":
          weight_c="*2204.62"    
      

       
       hp_c=""
       if hp_op=='watt':
         hp/=745.69
         hp_c="/745.69"

       
       #Calculation
       ET=5.825*(weight/hp)**(1/3)      

       if not( (weight>=1 and weight<=10000) or (round(weight,3)!=0 and round(weight,3)!=0.001 and weight<=10000)):
              base1,power1=Roundoff(weight)
              weight=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              weight=round(weight,4)
       
       if not( (ET>=1 and ET<=10000) or (round(ET,3)!=0 and round(ET,3)!=0.001 and ET<=10000)):
              base1,power1=Roundoff(ET)
              ET=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              ET=round(ET,4)

       if not( (hp>=1 and hp<=10000) or (round(hp,3)!=0 and round(hp,3)!=0.001 and hp<=10000)):
              base1,power1=Roundoff(hp)
              hp=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              hp=round(hp,4)
       
       

       context={
          'weight':weight,
          'ET':ET,
          'hp':hp,
          'weight1':weight1,
          'hp1':hp1,
          'hp_op':hp_op,
          'weight_op':weight_op,
          'id':1,
          'given_data':given_data,
          'weight_c':weight_c,
          'hp_c':hp_c
       }       
       return render(request,'enginehorsepowercalculator.html',context)
      

     else:
       return render(request,'enginehorsepowercalculator.html',{'given_data':given_data})        


  
  else:
     return render(request,'enginehorsepowercalculator.html',{'given_data':'form1'})


#FUCNTION FOR THE EQUIVALENCE RESISTANCE CALCULATOR

def equivalentresistancecalculator(request):
  if request.method=='POST':
    if "f1" not in request.POST:  
        resistance=request.POST.get('resistance')
        count=int(resistance)
        given_data=request.POST.get('given_data')
        
        name=[]
        unit=[]
        number=[]

        for i in range(1,count+1):
          n1='R'+str(i)
          n2=n1+'_op'
          name.append(n1)
          unit.append(n2)
          number.append(i)   

        data=zip(name,unit,number)
        reset=zip(name,unit)
        context={
          'data':data,
          'resistance':resistance,
          'given_data':given_data,
          'id':1,
          'reset':reset,
        }
        
        return render(request,'equivalentresistancecalculator.html',context)

    else:
        #FOR GETTING THE NUMBER OF RESISTANCE
        resistance=request.POST.get('resistance')
        count=int(resistance)
        
        #FOR THE SERIES OR PARALEL
        given_data=request.POST.get('given_data')
        
        name=[]
        unit=[]
        number=[]
        #FOR DISPLAYING THE DATA
        for i in range(1,count+1):
          n1='R'+str(i)
          n2=n1+'_op'
          name.append(n1)
          unit.append(n2)
          number.append(i) 

        #FOR INPUT DATA
        Input=[]
        
        #FOR THE UNIT OF THE INPUT DATA 
        conversion=[]
        
        #GETTING THE INPUT VALUES 
        for i in name:
          v1=request.POST.get(i)
          Input.append(v1)
        
        #GETTING THE UNITS
        for i in unit:
          v1=request.POST.get(i)
          conversion.append(v1)
        
        dataIn=zip(name,unit,number,Input,conversion)
        data2=zip(name,Input,conversion)

        #CONVERSION OF INPUT VALUES AS PER UNITS
        formulaConversion=[]
        Input1=[]
        for i in range(0,len(Input)):
          inp=str(Input[i])
          if inp.isdigit():
              val=int(Input[i])
          else:
              val=float(Input[i])
              val=round(val,5)

          if conversion[i] != 'Ω':
             t1,t2=convert2("res",conversion[i],val)
             Input1.append(t1)
             formulaConversion.append(t2)
          else:
            Input1.append(val)
            formulaConversion.append("")

        #FOR THE UNIT CONVERSION 
        data3=zip(name,Input,formulaConversion,conversion,Input1)  
        
        #CALCULATING THE ANSWER
        ans=0
        if given_data=="series":
          for i in Input1:
            ans+=i
        else:
            temp=0
            for i in Input1:
              temp+=1/i
            ans=1/temp  
        
        if not( (ans>=1 and ans<=10000) or (round(ans,3)!=0 and round(ans,3)!=0.001 and ans<=10000)):
              base1,power1=Roundoff(ans)
              ans=f"{base1} X 10 "+add_tags('sup',power1)
        else:
              ans=round(ans,4)
        
        reset=zip(name,unit)

        context={
          'dataIn':dataIn,
          'resistance':resistance,
          'given_data':given_data,
          'data2':data2,
          'data3':data3,
          'ans':ans,
          'id':2,
          'reset':reset,
        }
        
        return render(request,'equivalentresistancecalculator.html',context)

  else:
        name=[]
        unit=[]
        number=[]

        for i in range(1,3):
          n1='R'+str(i)
          n2=n1+'_op'
          name.append(n1)
          unit.append(n2)
          number.append(i)   

        data=zip(name,unit,number)
        reset=zip(name,unit)
        context={
          'data':data,
          'id':1,
          'reset':reset,
        }
        
        return render(request,'equivalentresistancecalculator.html',context)
  




#FUNCTION FOR THE EFFECTIVE NOISE TEMPERARYURE CALCULATOR
def noisetemperaturecalculator(request):

  if request.method == 'POST':
     given_data=request.POST.get('given_data')
     
     #FOR GETTING THE  EFFECTIVE  NOISE TEMPERATURE
     if request.POST.get('Etemp')!=None and request.POST.get('Etemp')!='' :
              Etemp_op=request.POST.get('Etemp_op')     
              inp=str(request.POST.get('Etemp'))
              if inp.isdigit():
                  Etemp=int(request.POST.get('Etemp'))
              else:
                  Etemp=float(request.POST.get('Etemp'))
              Etemp1=Etemp    
     else:
       Etemp=None
     
     #FOR GETTING THE NOISE
     if request.POST.get('noise')!=None and request.POST.get('noise')!='' :
              noise_op=request.POST.get('noise_op')     
              inp=str(request.POST.get('noise'))
              if inp.isdigit():
                  noise=int(request.POST.get('noise'))
              else:
                  noise=float(request.POST.get('noise'))
              noise1=noise   
     else:
       noise=None

     #FOR GETTING THE REFERENCE TEMPERATURE
     if request.POST.get('Tref')!=None and request.POST.get('Tref')!='' :
              Tref_op=request.POST.get('Tref_op')     
              inp=str(request.POST.get('Tref'))
              if inp.isdigit():
                  Tref=int(request.POST.get('Tref'))
              else:
                  Tref=float(request.POST.get('Tref'))
              Tref1=Tref    
     else:
       Tref=None

     #TO CHECK WHETHER THE FORM IS SUBMITTED OR NOT
     form= False
     if "f1" in request.POST:
       form=True  

     if given_data=='form1' and form:    
       
       #Conversion
       Tref,Tref_c=convert2('temp',Tref_op,Tref)
       Tref+=273.15      
       Tref_c=""
       if Tref_op=='°C':
         Tref_c="+273.15"
       elif Tref_op=='°F':
          Tref_c= "× 5/9 + 273.15 "  

       Etemp=Tref*(10**(noise/10)-1)


       if not( (Tref>=1 and Tref<=10000) or (round(Tref,3)!=0 and round(Tref,3)!=0.001 and Tref<=10000)):
             if Tref != 0: 
              base1,power1=Roundoff(Tref)
              Tref=f"{base1} X 10 "+add_tags('sup',power1)
             else:
               Tref='0' 
       else:
              Tref=round(Tref,4)
       
       if not( (noise>=1 and noise<=10000) or (round(noise,3)!=0 and round(noise,3)!=0.001 and noise<=10000)):
              base1,power1=Roundoff(noise)
              noise=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              noise=round(noise,4)

       if not( (Etemp>=1 and Etemp<=10000) or (round(Etemp,3)!=0 and round(Etemp,3)!=0.001 and Etemp<=10000)):
            if Etemp != 0: 
              base1,power1=Roundoff(Etemp)
              Etemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Etemp='0'
       else:
              Etemp=round(Etemp,4)
       

       context={
          'Etemp':Etemp,
          'noise':noise,
          'Tref':Tref,
          'noise1':noise1,
          'Tref1':Tref1,
          'Tref_op':Tref_op,
          'id':1,
          'given_data':given_data,
          'noise_op':noise_op,
          'Tref_c':Tref_c,
          }       
       return render(request,'noisetemperaturecalculator.html',context)

     
     elif given_data=='form2' and form:    
       
       #Conversion
       Etemp,Etemp_c=convert2('temp',Etemp_op,Etemp)
       Etemp+=273.15      
       Etemp_c=""

       if Etemp_op=='°C':
         Etemp_c="+273.15"
       elif Etemp_op=='°F':
          Etemp_c= "× 5/9 + 273.15"



       #Calculation
       Tref=Etemp/(10**(noise/10)-1)
       


       if not( (Tref>=1 and Tref<=10000) or (round(Tref,3)!=0 and round(Tref,3)!=0.001 and Tref<=10000)):
             if Tref != 0: 
              base1,power1=Roundoff(Tref)
              Tref=f"{base1} X 10 "+add_tags('sup',power1)
             else:
               Tref='0' 
       else:
              Tref=round(Tref,4)
       
       if not( (noise>=1 and noise<=10000) or (round(noise,3)!=0 and round(noise,3)!=0.001 and noise<=10000)):
              base1,power1=Roundoff(noise)
              noise=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              noise=round(noise,4)

       if not( (Etemp>=1 and Etemp<=10000) or (round(Etemp,3)!=0 and round(Etemp,3)!=0.001 and Etemp<=10000)):
            if Etemp != 0: 
              base1,power1=Roundoff(Etemp)
              Etemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Etemp='0'
       else:
              Etemp=round(Etemp,4)
       

       context={
          'Tref':Tref,
          'Etemp':Etemp,
          'noise':noise,
          'Etemp1':Etemp1,
          'noise1':noise1,
          'noise_op':noise_op,
          'Etemp_op':Etemp_op,
          'id':1,
          'given_data':given_data,
          'Etemp_c':Etemp_c,
          
       }       
       return render(request,'noisetemperaturecalculator.html',context)
  
     
     elif given_data=='form3' and form:    
       
       #Conversion
       Tref,Tref_c=convert2('temp',Tref_op,Tref)
       Etemp,Etemp_c=convert2('temp',Etemp_op,Etemp)
       Etemp+=273.15
       Tref+=273.15
       Etemp_c=""
       if Etemp_op=='°C':
         Etemp_c="+273.15"
       elif Etemp_op=='°F':
          Etemp_c= "× 5/9 + 273.15"

       Tref_c=""
       if Tref_op=='°C':
         Tref_c="+273.15"
       elif Tref_op=='°F':
          Tref_c= "× 5/9 + 273.15 "  
       
       #Calculation
       try:
         noise=10*math.log(Etemp/Tref+1,10) 
              
       except:
         message=""
         if Tref==0:
           message="Reference temperature cannot be 0"
           Tref='0'
           context={
                'Tref':Tref,
                'Etemp':Etemp,
                'Tref1':Tref1,
                'Etemp1':Etemp1,
                'Etemp_op':Etemp_op,
                'Tref_op':Tref_op,
                'message':message,
                'given_data':given_data,
                'Tref_c':Tref_c,
                'Etemp_c':Etemp_c
            }       
           return render(request,'noisetemperaturecalculator.html',context)
            
       if noise == None:
          message="Enter Valid data"
          context={
                'Tref':Tref,
                'Etemp':Etemp,
                'Tref1':Tref1,
                'Etemp1':Etemp1,
                'Etemp_op':Etemp_op,
                'Tref_op':Tref_op,
                'message':message,
                'given_data':given_data,
                'Tref_c':Tref_c,
                'Etemp_c':Etemp_c
            }       
          return render(request,'noisetemperaturecalculator.html',context)
        



       if not( (Tref>=1 and Tref<=10000) or (round(Tref,3)!=0 and round(Tref,3)!=0.001 and Tref<=10000)):
             if Tref != 0: 
              base1,power1=Roundoff(Tref)
              Tref=f"{base1} X 10 "+add_tags('sup',power1)
             else:
               Tref='0' 
       else:
              Tref=round(Tref,4)
       
       if not( (noise>=1 and noise<=10000) or (round(noise,3)!=0 and round(noise,3)!=0.001 and noise<=10000)):
              base1,power1=Roundoff(noise)
              noise=f"{base1} X 10 "+add_tags('sup',power1)
       else:
              noise=round(noise,4)

       if not( (Etemp>=1 and Etemp<=10000) or (round(Etemp,3)!=0 and round(Etemp,3)!=0.001 and Etemp<=10000)):
            if Etemp != 0: 
              base1,power1=Roundoff(Etemp)
              Etemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Etemp='0'
       else:
              Etemp=round(Etemp,4)
       
       
       

       context={
          'Tref':Tref,
          'noise':noise,
          'Etemp':Etemp,
          'Tref1':Tref1,
          'Etemp1':Etemp1,
          'Etemp_op':Etemp_op,
          'Tref_op':Tref_op,
          'id':1,
          'given_data':given_data,
          'Tref_c':Tref_c,
          'Etemp_c':Etemp_c
       }       
       return render(request,'noisetemperaturecalculator.html',context)
      


     else:
        return render(request,'noisetemperaturecalculator.html',{'given_data':given_data})
  
  else: 
    return render(request,'noisetemperaturecalculator.html',{'given_data':'form1'})






#FUNCTION FOR THE DOPLER SHIFT CALCULATOR
def dopplershiftcalculator(request):
   if request.method=='POST':
     
     given_data=request.POST.get('given_data')
     
     #FOR GETTING THE WAVE VELOCITY
     if request.POST.get('wvel')!=None and request.POST.get('wvel')!='' :
              wvel_op=request.POST.get('wvel_op')     
              inp=str(request.POST.get('wvel'))
              if inp.isdigit():
                  wvel=int(request.POST.get('wvel'))
              else:
                  wvel=float(request.POST.get('wvel'))
              wvel1=wvel    
     else:
       wvel=None
     
     #FOR GETTING THE SOURCE VELOCITY
     if request.POST.get('svel')!=None and request.POST.get('svel')!='' :
              svel_op=request.POST.get('svel_op')     
              inp=str(request.POST.get('svel'))
              if inp.isdigit():
                  svel=int(request.POST.get('svel'))
              else:
                  svel=float(request.POST.get('svel'))
              svel1=svel   
     else:
       svel=None

     #FOR GETTING THE WAVELENGTH
     if request.POST.get('wave')!=None and request.POST.get('wave')!='' :
              wave_op=request.POST.get('wave_op')     
              inp=str(request.POST.get('wave'))
              if inp.isdigit():
                  wave=int(request.POST.get('wave'))
              else:
                  wave=float(request.POST.get('wave'))
              wave1=wave    
     else:
       wave=None

     #FOR GETTING THE FREQUENCY        
     if request.POST.get('freq')!=None and request.POST.get('freq')!='' :
              freq_op=request.POST.get('freq_op')     
              inp=str(request.POST.get('freq'))
              if inp.isdigit():
                  freq=int(request.POST.get('freq'))
              else:
                  freq=float(request.POST.get('freq'))
              freq1=freq    
     else:
       freq=None  

     #TO CHECK WHETHER THE FORM IS SUBMITTED OR NOT
     form= False
     if "f1" in request.POST:
       form=True  
     
     if given_data=='form1' and form:    
       
       #Conversion
       wvel,wvel_c=convert2('vel',wvel_op,wvel)
       svel,svel_c=convert2('vel',svel_op,svel)
       freq,freq_c=convert2('freq',freq_op,freq)

       
       try:
        wave=(wvel-svel)/freq
       except:
         
          context={
          'freq':"0",
          'svel':svel,
          'wvel':wvel,
           
           'message':'Frequency Cannot be 0',

          'svel1':svel1,
          'wvel1':wvel1,
          'freq1':freq1,
          
          'wvel_op':wvel_op,
          'freq_op':freq_op,
          'svel_op':svel_op,
          
          'given_data':given_data,

          'freq_c':freq_c,
          'svel_c':svel_c,
          'wvel_c':wvel_c
          }       
          return render(request,'dopplershiftcalculator.html',context)




       if not( (wvel>=1 and wvel<=10000) or (round(wvel,3)!=0 and round(wvel,3)!=0.001 and wvel<=10000)):
            if wvel != 0:  
              base1,power1=Roundoff(wvel)
              wvel=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               wvel='0'  
       else:
              wvel=round(wvel,4)
       
       if not( (svel>=1 and svel<=10000) or (round(svel,3)!=0 and round(svel,3)!=0.001 and svel<=10000)):
            if svel != 0:  
              base1,power1=Roundoff(svel)
              svel=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              svel='0'  
       else:
              svel=round(svel,4)

       if not( (wave>=1 and wave<=10000) or (round(wave,3)!=0 and round(wave,3)!=0.001 and wave<=10000)):
            if wave != 0:
              base1,power1=Roundoff(wave)
              wave=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              wave='0'  
       else:
              wave=round(wave,4)
       
       if not( (freq>=1 and freq<=10000) or (round(freq,3)!=0 and round(freq,3)!=0.001 and freq<=10000)):
            if freq != 0:
              base1,power1=Roundoff(freq)
              freq=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              freq='0'  
       else:
              freq=round(freq,4)
       

       context={
          'wave':wave,
          'svel':svel,
          'wvel':wvel,
          'freq':freq,
           'freq1':freq1,
          'svel1':svel1,
          'wvel1':wvel1,
          'wvel_op':wvel_op,
          'freq_op':freq_op,
          'id':1,
          'given_data':given_data,
          'svel_op':svel_op,
          'wvel_c':wvel_c,
          'freq_c':freq_c,
          'svel_c':svel_c
          }       
       return render(request,'dopplershiftcalculator.html',context)

     elif given_data=='form2' and form:    
       
       #Conversion
       wave,wave_c=convert2('len',wave_op,wave)
       svel,svel_c=convert2('vel',svel_op,svel)
       freq,freq_c=convert2('freq',freq_op,freq)

       wvel=wave*freq+svel



       if not( (wvel>=1 and wvel<=10000) or (round(wvel,3)!=0 and round(wvel,3)!=0.001 and wvel<=10000)):
            if wvel != 0:  
              base1,power1=Roundoff(wvel)
              wvel=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               wvel='0'  
       else:
              wvel=round(wvel,4)
       
       if not( (svel>=1 and svel<=10000) or (round(svel,3)!=0 and round(svel,3)!=0.001 and svel<=10000)):
            if svel != 0:  
              base1,power1=Roundoff(svel)
              svel=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              svel='0'  
       else:
              svel=round(svel,4)

       if not( (wave>=1 and wave<=10000) or (round(wave,3)!=0 and round(wave,3)!=0.001 and wave<=10000)):
            if wave != 0:
              base1,power1=Roundoff(wave)
              wave=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              wave='0'  
       else:
              wave=round(wave,4)
       
       if not( (freq>=1 and freq<=10000) or (round(freq,3)!=0 and round(freq,3)!=0.001 and freq<=10000)):
            if freq != 0:
              base1,power1=Roundoff(freq)
              freq=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              freq='0'  
       else:
              freq=round(freq,4)
       

       context={
          'wave':wave,
          'svel':svel,
          'wvel':wvel,
          'freq':freq,
           'freq1':freq1,
          'svel1':svel1,
          'wave1':wave1,
          'wave_op':wave_op,
          'freq_op':freq_op,
          'id':1,
          'given_data':given_data,
          'svel_op':svel_op,
          'wave_c':wave_c,
          'freq_c':freq_c,
          'svel_c':svel_c
          }       
       return render(request,'dopplershiftcalculator.html',context)

     elif given_data=='form3' and form:    
       #Conversion
       wave,wave_c=convert2('len',wave_op,wave)
       wvel,wvel_c=convert2('vel',wvel_op,wvel)
       freq,freq_c=convert2('freq',freq_op,freq)

       svel=wvel-wave*freq

       if not( (wvel>=1 and wvel<=10000) or (round(wvel,3)!=0 and round(wvel,3)!=0.001 and wvel<=10000)):
            if wvel != 0:  
              base1,power1=Roundoff(wvel)
              wvel=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               wvel='0'  
       else:
              wvel=round(wvel,4)
       
       if not( (svel>=1 and svel<=10000) or (round(svel,3)!=0 and round(svel,3)!=0.001 and svel<=10000)):
            if svel != 0:  
              base1,power1=Roundoff(svel)
              svel=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              svel='0'  
       else:
              svel=round(svel,4)

       if not( (wave>=1 and wave<=10000) or (round(wave,3)!=0 and round(wave,3)!=0.001 and wave<=10000)):
            if wave != 0:
              base1,power1=Roundoff(wave)
              wave=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              wave='0'  
       else:
              wave=round(wave,4)
       
       if not( (freq>=1 and freq<=10000) or (round(freq,3)!=0 and round(freq,3)!=0.001 and freq<=10000)):
            if freq != 0:
              base1,power1=Roundoff(freq)
              freq=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              freq='0'  
       else:
              freq=round(freq,4)
       

       context={
          'wave':wave,
          'svel':svel,
          'wvel':wvel,
          'freq':freq,
           
          'freq1':freq1,
          'wvel1':wvel1,
          'wave1':wave1,
          
          'wvel_op':wvel_op,
          'wave_op':wave_op,
          'freq_op':freq_op,
          
          'id':1,
          'given_data':given_data,

          'wave_c':wave_c,
          'freq_c':freq_c,
          'wvel_c':wvel_c
          }       
       return render(request,'dopplershiftcalculator.html',context)
     

     elif given_data=='form4' and form:    
       
       #Conversion
       wave,wave_c=convert2('len',wave_op,wave)
       wvel,wvel_c=convert2('vel',wvel_op,wvel)
       svel,svel_c=convert2('vel',svel_op,svel)
       
       try:
        freq=(wvel-svel)/wave
       except:
         
          context={
          'wave':"0",
          'svel':svel,
          'wvel':wvel,
           
           'message':'Wavelength cannot be 0',

          'svel1':svel1,
          'wvel1':wvel1,
          'wave1':wave1,
          
          'wvel_op':wvel_op,
          'wave_op':wave_op,
          'svel_op':svel_op,
          
          'given_data':given_data,

          'wave_c':wave_c,
          'svel_c':svel_c,
          'wvel_c':wvel_c
          }       
          return render(request,'dopplershiftcalculator.html',context)


       

       if not( (wvel>=1 and wvel<=10000) or (round(wvel,3)!=0 and round(wvel,3)!=0.001 and wvel<=10000)):
            if wvel != 0:  
              base1,power1=Roundoff(wvel)
              wvel=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               wvel='0'  
       else:
              wvel=round(wvel,4)
       
       if not( (svel>=1 and svel<=10000) or (round(svel,3)!=0 and round(svel,3)!=0.001 and svel<=10000)):
            if svel != 0:  
              base1,power1=Roundoff(svel)
              svel=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              svel='0'  
       else:
              svel=round(svel,4)

       if not( (wave>=1 and wave<=10000) or (round(wave,3)!=0 and round(wave,3)!=0.001 and wave<=10000)):
            if wave != 0:
              base1,power1=Roundoff(wave)
              wave=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              wave='0'  
       else:
              wave=round(wave,4)
       
       if not( (freq>=1 and freq<=10000) or (round(freq,3)!=0 and round(freq,3)!=0.001 and freq<=10000)):
            if freq != 0:
              base1,power1=Roundoff(freq)
              freq=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              freq='0'  
       else:
              freq=round(freq,4)
       

       context={
          'wave':wave,
          'svel':svel,
          'wvel':wvel,
          'freq':freq,
           
          'svel1':svel1,
          'wvel1':wvel1,
          'wave1':wave1,
          
          'wvel_op':wvel_op,
          'wave_op':wave_op,
          'svel_op':svel_op,
          
          'id':1,
          'given_data':given_data,

          'wave_c':wave_c,
          'svel_c':svel_c,
          'wvel_c':wvel_c
          }       
       return render(request,'dopplershiftcalculator.html',context)


     else:
       return render(request,'dopplershiftcalculator.html',{'given_data':given_data})
   
   else:
     return render(request,'dopplershiftcalculator.html',{'given_data':'form1'})




#FUNCTION FOR THE clausius clapeyron equation calculator 
def clausiusclapeyronequationcalculator(request):
  if request.method=='POST':
     given_data=request.POST.get('given_data')
     
     #FOR GETTING THE Ipressure VELOCITY
     if request.POST.get('Itemp')!=None and request.POST.get('Itemp')!='' :
              Itemp_op=request.POST.get('Itemp_op')     
              inp=str(request.POST.get('Itemp'))
              if inp.isdigit():
                  Itemp=int(request.POST.get('Itemp'))
              else:
                  Itemp=float(request.POST.get('Itemp'))
              Itemp1=Itemp    
     else:
       Itemp=None
     
     #FOR GETTING THE SOURCE VELOCITY
     if request.POST.get('Ftemp')!=None and request.POST.get('Ftemp')!='' :
              Ftemp_op=request.POST.get('Ftemp_op')     
              inp=str(request.POST.get('Ftemp'))
              if inp.isdigit():
                  Ftemp=int(request.POST.get('Ftemp'))
              else:
                  Ftemp=float(request.POST.get('Ftemp'))
              Ftemp1=Ftemp   
     else:
       Ftemp=None

     #FOR GETTING THE IpressureLENGTH
     if request.POST.get('Ipressure')!=None and request.POST.get('Ipressure')!='' :
              Ipressure_op=request.POST.get('Ipressure_op')     
              inp=str(request.POST.get('Ipressure'))
              if inp.isdigit():
                  Ipressure=int(request.POST.get('Ipressure'))
              else:
                  Ipressure=float(request.POST.get('Ipressure'))
              Ipressure1=Ipressure    
     else:
       Ipressure=None

     #FOR GETTING THE FpressureUENCY        
     if request.POST.get('Fpressure')!=None and request.POST.get('Fpressure')!='' :
              Fpressure_op=request.POST.get('Fpressure_op')     
              inp=str(request.POST.get('Fpressure'))
              if inp.isdigit():
                  Fpressure=int(request.POST.get('Fpressure'))
              else:
                  Fpressure=float(request.POST.get('Fpressure'))
              Fpressure1=Fpressure    
     else:
       Fpressure=None  

     if request.POST.get('Ipressure')!=None and request.POST.get('Ipressure')!='' :
              Ipressure_op=request.POST.get('Ipressure_op')     
              inp=str(request.POST.get('Ipressure'))
              if inp.isdigit():
                  Ipressure=int(request.POST.get('Ipressure'))
              else:
                  Ipressure=float(request.POST.get('Ipressure'))
              Ipressure1=Ipressure    
     else:
       Ipressure=None

     if request.POST.get('enthalphy')!=None and request.POST.get('enthalphy')!='' :
              enthalphy_op=request.POST.get('enthalphy_op')     
              inp=str(request.POST.get('enthalphy'))
              if inp.isdigit():
                  enthalphy=int(request.POST.get('enthalphy'))
              else:
                  enthalphy=float(request.POST.get('enthalphy'))
              enthalphy1=enthalphy    
     else:
       enthalphy=None  
      
  

     #TO CHECK WHETHER THE FORM IS SUBMITTED OR NOT
     form= False
     if "f1" in request.POST:
       form=True

     if given_data=='form1' and form:    
       
       #Conversion
       Ftemp_c=""
       Itemp_c=""
       if Itemp_op != 'K':
         Itemp,Itemp_c=convert2('temp',Itemp_op,Itemp)
         Itemp+=273.15
         Itemp_c+="+273.15"
       
       if Ftemp_op != 'K':
         Ftemp,Ftemp_c=convert2('temp',Ftemp_op,Ftemp)
         Ftemp+=273.15
         Ftemp_c+="+273.15"
       
       Ipressure,Ipressure_c=convert2('pressure',Ipressure_op,Ipressure)
       Fpressure,Fpressure_c=convert2('pressure',Fpressure_op,Fpressure)
       
       try:  
         enthalphy=math.log(Ipressure/Fpressure)*8.314/(1/Ftemp-1/Itemp)
       except:
          message=""
          if Fpressure<=0:
            message="Final pressure cannot be zero and negative"
            Fpressure='0'
          
          if Ipressure<=0:
            message="Intial pressure cannot be  negative"
            Ipressure='0'  
          
          if Itemp==0:
            message="Initial temperature cannot be zero"
            Itemp='0'
          
          if Ftemp==0:
            message="Final temperature cannot be zero"
            Ftemp='0'  


          context={
          'Itemp':Itemp,
          'Ipressure':Ipressure,
          'Ftemp':Ftemp,
          'Fpressure':Fpressure,
           
           'message':message,

          'Ipressure1':Ipressure1,
          'Ftemp1':Ftemp1,
          'Itemp1':Itemp1,
          'Fpressure1':Fpressure1,

          
          'Ftemp_op':Ftemp_op,
          'Itemp_op':Itemp_op,
          'Ipressure_op':Ipressure_op,
          'Fpressure_op':Fpressure_op,

          
          'given_data':given_data,

          'Itemp_c':Itemp_c,
          'Ipressure_c':Ipressure_c,
          'Ftemp_c':Ftemp_c,
          'Fpressure_c':Fpressure_c,

          }       
          return render(request,'clausiusclapeyronequationcalculator.html',context)


       

       if not( (Ftemp>=1 and Ftemp<=10000) or (round(Ftemp,3)!=0 and round(Ftemp,3)!=0.001 and Ftemp<=10000)):
            if Ftemp != 0:  
              base1,power1=Roundoff(Ftemp)
              Ftemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               Ftemp='0'  
       else:
              Ftemp=round(Ftemp,4)
       
       if not( (Ipressure>=1 and Ipressure<=10000) or (round(Ipressure,3)!=0 and round(Ipressure,3)!=0.001 and Ipressure<=10000)):
            if Ipressure != 0:  
              base1,power1=Roundoff(Ipressure)
              Ipressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Ipressure='0'  
       else:
              Ipressure=round(Ipressure,4)

       if not( (Itemp>=1 and Itemp<=10000) or (round(Itemp,3)!=0 and round(Itemp,3)!=0.001 and Itemp<=10000)):
            if Itemp != 0:
              base1,power1=Roundoff(Itemp)
              Itemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Itemp='0'  
       else:
              Itemp=round(Itemp,4)
       
       if not( (enthalphy>=1 and enthalphy<=10000) or (round(enthalphy,3)!=0 and round(enthalphy,3)!=0.001 and enthalphy<=10000)):
            if enthalphy != 0:
              base1,power1=Roundoff(enthalphy)
              enthalphy=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              enthalphy='0'  
       else:
              enthalphy=round(enthalphy,4)
       
       
       if not( (Fpressure>=1 and Fpressure<=10000) or (round(Fpressure,3)!=0 and round(Fpressure,3)!=0.001 and Fpressure<=10000)):
            if Fpressure != 0:  
              base1,power1=Roundoff(Fpressure)
              Fpressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               Fpressure='0' 
       else:
              Fpressure=round(Fpressure,4)
       
       
       context={
          'Itemp':Itemp,
          'Ipressure':Ipressure,
          'Ftemp':Ftemp,
          'enthalphy':enthalphy,
          'Fpressure':Fpressure,
           
          'Ipressure1':Ipressure1,
          'Ftemp1':Ftemp1,
          'Itemp1':Itemp1,
          'Fpressure1':Fpressure1,

          'Ftemp_op':Ftemp_op,
          'Itemp_op':Itemp_op,
          'Ipressure_op':Ipressure_op,
          'Fpressure_op':Fpressure_op,

          'id':1,
          'given_data':given_data,

          'Itemp_c':Itemp_c,
          'Ipressure_c':Ipressure_c,
          'Ftemp_c':Ftemp_c,
          'Fpressure_c':Fpressure_c,
          }       
       return render(request,'clausiusclapeyronequationcalculator.html',context)


     elif given_data=='form2' and form:    
       
       #Conversion
       if Itemp != 'K':
         Itemp,Itemp_c=convert2('temp',Itemp_op,Itemp)
         Itemp_c+="+273.15"
         Itemp+=273.15

       enthalphy,enthalphy_c=convert2('energy',enthalphy_op,enthalphy)
       Ipressure,Ipressure_c=convert2('pressure',Ipressure_op,Ipressure)
       Fpressure,Fpressure_c=convert2('pressure',Fpressure_op,Fpressure)
       
       try:
        #enthalphy=math.log(Ipressure/Fpressure)*8.314/(1/Ftemp-1/Itemp)
        t=math.log(Ipressure/Fpressure)*8.3145/enthalphy
        t+=1/Itemp
        Ftemp=1/t

       except:
          message=""
          if Fpressure<=0:
            message="Final pressure cannot be negative and zero"
            Fpressure='0'
          
          if Itemp==0:
            message="Intial pressure cannot be  zero"
            Itemp='0'
          
          if enthalphy==0:
            message="Enthaphy cannot be  zero"
            enthalphy='0'  

          
          if Ipressure<0:
            message="Initial pressure cannot be  negative"
            Ipressure='0'    


          context={
          'Itemp':Itemp,
          'Ipressure':Ipressure,
          'enthalphy':enthalphy,
          'Fpressure':Fpressure,
           
           'message':message,

          'Ipressure1':Ipressure1,
          'enthalphy1':enthalphy1,
          'Itemp1':Itemp1,
          'Fpressure1':Fpressure1,

          
          'enthalphy_op':enthalphy_op,
          'Itemp_op':Itemp_op,
          'Ipressure_op':Ipressure_op,
          'Fpressure_op':Fpressure_op,

          
          'given_data':given_data,

          'Itemp_c':Itemp_c,
          'Ipressure_c':Ipressure_c,
          'enthalphy_c':enthalphy_c,
          'Fpressure_c':Fpressure_c,

          }       
          return render(request,'clausiusclapeyronequationcalculator.html',context)


       if not( (Ftemp>=1 and Ftemp<=10000) or (round(Ftemp,3)!=0 and round(Ftemp,3)!=0.001 and Ftemp<=10000)):
            if Ftemp != 0:  
              base1,power1=Roundoff(Ftemp)
              Ftemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               Ftemp='0'  
       else:
              Ftemp=round(Ftemp,4)
       
       if not( (Ipressure>=1 and Ipressure<=10000) or (round(Ipressure,3)!=0 and round(Ipressure,3)!=0.001 and Ipressure<=10000)):
            if Ipressure != 0:  
              base1,power1=Roundoff(Ipressure)
              Ipressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Ipressure='0'  
       else:
              Ipressure=round(Ipressure,4)

       if not( (Itemp>=1 and Itemp<=10000) or (round(Itemp,3)!=0 and round(Itemp,3)!=0.001 and Itemp<=10000)):
            if Itemp != 0:
              base1,power1=Roundoff(Itemp)
              Itemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Itemp='0'  
       else:
              Itemp=round(Itemp,4)
       
       if not( (enthalphy>=1 and enthalphy<=10000) or (round(enthalphy,3)!=0 and round(enthalphy,3)!=0.001 and enthalphy<=10000)):
            if enthalphy != 0:
              base1,power1=Roundoff(enthalphy)
              enthalphy=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              enthalphy='0'  
       else:
              enthalphy=round(enthalphy,4)
       
       
       if not( (Fpressure>=1 and Fpressure<=10000) or (round(Fpressure,3)!=0 and round(Fpressure,3)!=0.001 and Fpressure<=10000)):
            if Fpressure != 0:  
              base1,power1=Roundoff(Fpressure)
              Fpressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Fpressure='0' 
       else:
         Fpressure=round(Fpressure,4)
       
       context={
          'Itemp':Itemp,
          'Ipressure':Ipressure,
          'enthalphy':enthalphy,
          'Ftemp':Ftemp,
           'Fpressure':Fpressure,

          'Ipressure1':Ipressure1,
          'enthalphy1':enthalphy1,
          'Itemp1':Itemp1,
           'Fpressure1':Fpressure1,
          
          'enthalphy_op':enthalphy_op,
          'Itemp_op':Itemp_op,
          'Ipressure_op':Ipressure_op,
           'Fpressure_op':Fpressure_op,

          'id':1,
          'given_data':given_data,

          'Itemp_c':Itemp_c,
          'Ipressure_c':Ipressure_c,
          'enthalphy_c':enthalphy_c,
           'Fpressure_c':Fpressure_c,
          }       
       return render(request,'clausiusclapeyronequationcalculator.html',context)
    
    
     elif given_data=='form3' and form:    
       
       #Conversion
       if Ftemp != 'K':
         Ftemp,Ftemp_c=convert2('temp',Ftemp_op,Ftemp)
         Ftemp_c+="+273.15"
         Ftemp+=273.15

       enthalphy,enthalphy_c=convert2('energy',enthalphy_op,enthalphy)
       Ipressure,Ipressure_c=convert2('pressure',Ipressure_op,Ipressure)
       Fpressure,Fpressure_c=convert2('pressure',Fpressure_op,Fpressure)
       
       try:
        #enthalphy=math.log(Ipressure/Fpressure)*8.314/(1/Ftemp-1/Itemp)
        t=1/Ftemp-math.log(Ipressure/Fpressure)*8.314/enthalphy
        Itemp=1/t

       except:
          message=""
          if Fpressure<=0:
            message="Final pressure cannot be negtive and zero"
            Fpressure='0'
          
          if Ipressure<=0:
            message="Initial pressure cannot be negative "
            Fpressure='0'

          if Ftemp==0:
            message="Final temperature cannot be zero"
            Ftemp='0'

          if enthalphy==0:
            message="Enthalphy cannot be zero"
            enthalphy='0'
            


          context={
          'Ftemp':Ftemp,
          'Ipressure':Ipressure,
          'enthalphy':enthalphy,
          'Fpressure':Fpressure,
           
           'message':message,

          'Ipressure1':Ipressure1,
          'enthalphy1':enthalphy1,
          'Ftemp1':Ftemp1,
          'Fpressure1':Fpressure1,

          
          'enthalphy_op':enthalphy_op,
          'Ftemp_op':Ftemp_op,
          'Ipressure_op':Ipressure_op,
          'Fpressure_op':Fpressure_op,

          
          'given_data':given_data,

          'Ftemp_c':Ftemp_c,
          'Ipressure_c':Ipressure_c,
          'enthalphy_c':enthalphy_c,
          'Fpressure_c':Fpressure_c,

          }       
          return render(request,'clausiusclapeyronequationcalculator.html',context)


       if not( (Ftemp>=1 and Ftemp<=10000) or (round(Ftemp,3)!=0 and round(Ftemp,3)!=0.001 and Ftemp<=10000)):
            if Ftemp != 0:  
              base1,power1=Roundoff(Ftemp)
              Ftemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               Ftemp='0'  
       else:
              Ftemp=round(Ftemp,4)
       
       if not( (Ipressure>=1 and Ipressure<=10000) or (round(Ipressure,3)!=0 and round(Ipressure,3)!=0.001 and Ipressure<=10000)):
            if Ipressure != 0:  
              base1,power1=Roundoff(Ipressure)
              Ipressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Ipressure='0'  
       else:
              Ipressure=round(Ipressure,4)

       if not( (Itemp>=1 and Itemp<=10000) or (round(Itemp,3)!=0 and round(Itemp,3)!=0.001 and Itemp<=10000)):
            if Itemp != 0:
              base1,power1=Roundoff(Itemp)
              Itemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Itemp='0'  
       else:
              Itemp=round(Itemp,4)
       
       if not( (enthalphy>=1 and enthalphy<=10000) or (round(enthalphy,3)!=0 and round(enthalphy,3)!=0.001 and enthalphy<=10000)):
            if enthalphy != 0:
              base1,power1=Roundoff(enthalphy)
              enthalphy=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              enthalphy='0'  
       else:
              enthalphy=round(enthalphy,4)
       
       
       if not( (Fpressure>=1 and Fpressure<=10000) or (round(Fpressure,3)!=0 and round(Fpressure,3)!=0.001 and Fpressure<=10000)):
            if Fpressure != 0:  
              base1,power1=Roundoff(Fpressure)
              Fpressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Fpressure='0' 
       else:
         Fpressure=round(Fpressure,4)
       
       context={
          'Itemp':Itemp,
          'Ipressure':Ipressure,
          'enthalphy':enthalphy,
          'Ftemp':Ftemp,
           'Fpressure':Fpressure,

          'Ipressure1':Ipressure1,
          'enthalphy1':enthalphy1,
          'Ftemp1':Ftemp1,
           'Fpressure1':Fpressure1,
          
          'enthalphy_op':enthalphy_op,
          'Ftemp_op':Ftemp_op,
          'Ipressure_op':Ipressure_op,
           'Fpressure_op':Fpressure_op,

          'id':1,
          'given_data':given_data,

          'Ftemp_c':Ftemp_c,
          'Ipressure_c':Ipressure_c,
          'enthalphy_c':enthalphy_c,
           'Fpressure_c':Fpressure_c,
          }       
       return render(request,'clausiusclapeyronequationcalculator.html',context) 



     
     elif given_data=='form4' and form:    
       
       #Conversion
       if Ftemp != 'K':
         Ftemp,Ftemp_c=convert2('temp',Ftemp_op,Ftemp)
         Ftemp_c+="+273.15"
         Ftemp+=273.15
      
       if Itemp != 'K':
         Itemp,Itemp_c=convert2('temp',Itemp_op,Itemp)
         Itemp_c+="+273.15"
         Itemp+=273.15   

       enthalphy,enthalphy_c=convert2('energy',enthalphy_op,enthalphy)
       Fpressure,Fpressure_c=convert2('pressure',Fpressure_op,Fpressure)
       
       try:
        #enthalphy=math.log(Ipressure/Fpressure)*8.314/(1/Ftemp-1/Itemp)
        Ipressure = (2.718**(enthalphy*(1/Ftemp-1/Itemp)/8.314))*Fpressure
       except:
          message=""
          
          if Ftemp==0:
            message="Final temperature cannot be zero"
            Ftemp='0'

          if Itemp==0:
            message="Initial temperature cannot be zero"
            Itemp='0'  
          
          context={
          'Ftemp':Ftemp,
          'Itemp':Itemp,
          'enthalphy':enthalphy,
          'Fpressure':Fpressure,
           
           'message':message,

          'Itemp1':Itemp1,
          'enthalphy1':enthalphy1,
          'Ftemp1':Ftemp1,
          'Fpressure1':Fpressure1,

          
          'enthalphy_op':enthalphy_op,
          'Ftemp_op':Ftemp_op,
          'Itemp_op':Itemp_op,
          'Fpressure_op':Fpressure_op,

          
          'given_data':given_data,

          'Ftemp_c':Ftemp_c,
          'Itemp_c':Itemp_c,
          'enthalphy_c':enthalphy_c,
          'Fpressure_c':Fpressure_c,

          }       
          return render(request,'clausiusclapeyronequationcalculator.html',context)


       if not( (Ftemp>=1 and Ftemp<=10000) or (round(Ftemp,3)!=0 and round(Ftemp,3)!=0.001 and Ftemp<=10000)):
            if Ftemp != 0:  
              base1,power1=Roundoff(Ftemp)
              Ftemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               Ftemp='0'  
       else:
              Ftemp=round(Ftemp,4)
       
       if not( (Ipressure>=1 and Ipressure<=10000) or (round(Ipressure,3)!=0 and round(Ipressure,3)!=0.001 and Ipressure<=10000)):
            if Ipressure != 0:  
              base1,power1=Roundoff(Ipressure)
              Ipressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Ipressure='0'  
       else:
              Ipressure=round(Ipressure,4)

       if not( (Itemp>=1 and Itemp<=10000) or (round(Itemp,3)!=0 and round(Itemp,3)!=0.001 and Itemp<=10000)):
            if Itemp != 0:
              base1,power1=Roundoff(Itemp)
              Itemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Itemp='0'  
       else:
              Itemp=round(Itemp,4)
       
       if not( (enthalphy>=1 and enthalphy<=10000) or (round(enthalphy,3)!=0 and round(enthalphy,3)!=0.001 and enthalphy<=10000)):
            if enthalphy != 0:
              base1,power1=Roundoff(enthalphy)
              enthalphy=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              enthalphy='0'  
       else:
              enthalphy=round(enthalphy,4)
       
       
       if not( (Fpressure>=1 and Fpressure<=10000) or (round(Fpressure,3)!=0 and round(Fpressure,3)!=0.001 and Fpressure<=10000)):
            if Fpressure != 0:  
              base1,power1=Roundoff(Fpressure)
              Fpressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Fpressure='0' 
       else:
         Fpressure=round(Fpressure,4)
       
       context={
          'Itemp':Itemp,
          'Ipressure':Ipressure,
          'enthalphy':enthalphy,
          'Ftemp':Ftemp,
           'Fpressure':Fpressure,

          'Itemp1':Itemp1,
          'enthalphy1':enthalphy1,
          'Ftemp1':Ftemp1,
           'Fpressure1':Fpressure1,
          
          'enthalphy_op':enthalphy_op,
          'Ftemp_op':Ftemp_op,
          'Itemp_op':Itemp_op,
           'Fpressure_op':Fpressure_op,

          'id':1,
          'given_data':given_data,

          'Ftemp_c':Ftemp_c,
          'Itemp_c':Itemp_c,
          'enthalphy_c':enthalphy_c,
           'Fpressure_c':Fpressure_c,
          }       
       return render(request,'clausiusclapeyronequationcalculator.html',context) 

     
     elif given_data=='form5' and form:    
       
       #Conversion
       if Ftemp != 'K':
         Ftemp,Ftemp_c=convert2('temp',Ftemp_op,Ftemp)
         Ftemp_c+="+273.15"
         Ftemp+=273.15
      
       if Itemp != 'K':
         Itemp,Itemp_c=convert2('temp',Itemp_op,Itemp)
         Itemp_c+="+273.15"
         Itemp+=273.15   
       
       enthalphy,enthalphy_c=convert2('energy',enthalphy_op,enthalphy)
       Ipressure,Ipressure_c=convert2('pressure',Ipressure_op,Ipressure)
       
       try:
        #enthalphy=math.log(Ipressure/Fpressure)*8.314/(1/Ftemp-1/Itemp)
        t=(2.718**((1/Ftemp-1/Itemp)/8.314*enthalphy))
        Fpressure=Ipressure/t 
       
       except:
          message=""
          if Ipressure==0:
            message="Intial pressure cannot be zero"
            Ipressure='0'
          
          if Ftemp==0:
            message="Final temperature cannot be zero"
            Ftemp='0'

          if Itemp==0:
            message="Intial temperature cannot be zero"
            Itemp='0'  
          
         

          context={
          'Ftemp':Ftemp,
          'Itemp':Itemp,
          'enthalphy':enthalphy,
          'Ipressure':Ipressure,
           
           'message':message,

          'Itemp1':Itemp1,
          'enthalphy1':enthalphy1,
          'Ftemp1':Ftemp1,
          'Ipressure1':Ipressure1,

          
          'enthalphy_op':enthalphy_op,
          'Ftemp_op':Ftemp_op,
          'Itemp_op':Itemp_op,
          'Ipressure_op':Ipressure_op,

          
          'given_data':given_data,

          'Ftemp_c':Ftemp_c,
          'Itemp_c':Itemp_c,
          'enthalphy_c':enthalphy_c,
          'Ipressure_c':Ipressure_c,

          }       
          return render(request,'clausiusclapeyronequationcalculator.html',context)


       if not( (Ftemp>=1 and Ftemp<=10000) or (round(Ftemp,3)!=0 and round(Ftemp,3)!=0.001 and Ftemp<=10000)):
            if Ftemp != 0:  
              base1,power1=Roundoff(Ftemp)
              Ftemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
               Ftemp='0'  
       else:
              Ftemp=round(Ftemp,4)
       
       if not( (Ipressure>=1 and Ipressure<=10000) or (round(Ipressure,3)!=0 and round(Ipressure,3)!=0.001 and Ipressure<=10000)):
            if Ipressure != 0:  
              base1,power1=Roundoff(Ipressure)
              Ipressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Ipressure='0'  
       else:
              Ipressure=round(Ipressure,4)

       if not( (Itemp>=1 and Itemp<=10000) or (round(Itemp,3)!=0 and round(Itemp,3)!=0.001 and Itemp<=10000)):
            if Itemp != 0:
              base1,power1=Roundoff(Itemp)
              Itemp=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Itemp='0'  
       else:
              Itemp=round(Itemp,4)
       
       if not( (enthalphy>=1 and enthalphy<=10000) or (round(enthalphy,3)!=0 and round(enthalphy,3)!=0.001 and enthalphy<=10000)):
            if enthalphy != 0:
              base1,power1=Roundoff(enthalphy)
              enthalphy=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              enthalphy='0'  
       else:
              enthalphy=round(enthalphy,4)
       
       
       if not( (Fpressure>=1 and Fpressure<=10000) or (round(Fpressure,3)!=0 and round(Fpressure,3)!=0.001 and Fpressure<=10000)):
            if Fpressure != 0:  
              base1,power1=Roundoff(Fpressure)
              Fpressure=f"{base1} X 10 "+add_tags('sup',power1)
            else:
              Fpressure='0' 
       else:
         Fpressure=round(Fpressure,4)
       
       context={
          'Itemp':Itemp,
          'Ipressure':Ipressure,
          'enthalphy':enthalphy,
          'Ftemp':Ftemp,
           'Fpressure':Fpressure,

          'Itemp1':Itemp1,
          'enthalphy1':enthalphy1,
          'Ftemp1':Ftemp1,
           'Ipressure1':Ipressure1,
          
          'enthalphy_op':enthalphy_op,
          'Ftemp_op':Ftemp_op,
          'Itemp_op':Itemp_op,
           'Ipressure_op':Ipressure_op,

          'id':1,
          'given_data':given_data,

          'Ftemp_c':Ftemp_c,
          'Itemp_c':Itemp_c,
          'enthalphy_c':enthalphy_c,
           'Ipressure_c':Ipressure_c,
          }       
       return render(request,'clausiusclapeyronequationcalculator.html',context) 

           
     else:
       return render(request,'clausiusclapeyronequationcalculator.html',{'given_data':given_data})
  else:  
   return render(request,'clausiusclapeyronequationcalculator.html',{'given_data':'form1'})




def matrixcalculator(request):
  
  if request.method=='POST': 
  
    #FOR CHANGING THE DIMENSION OF MATRIX A
    if 'addA' in request.POST or 'subA' in request.POST:
        
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        if "addA" in request.POST:
          dimensionA+=1
        
        if "subA" in request.POST:
          dimensionA-=1

        if dimensionA<=0:
          dimensionA=1   
        
        dataA=[]
        dataB=[]

        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(i*dimensionA+j+1)
            dataA.append(t)  

        B1=request.POST.getlist('matB')

        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),2)
           else:
             B1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionB):
            t=[]

            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1

            dataB.append(t)
        changes=request.POST.get('changes')    
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
           'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)

    #FOR ADDING OR DELETING THE ROW IN MATRIXB
    elif 'addB' in request.POST or 'subB' in request.POST:
        
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        if "addB" in request.POST:
          dimensionB+=1
        
        if "subB" in request.POST:
          dimensionB-=1

        if dimensionB<=0:
          dimensionB=1   
        
        dataA=[]
        dataB=[]

        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(i*dimensionB+j+1)
            dataB.append(t)  

        A1=request.POST.getlist('matA')

        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),2)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]

            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1

            dataA.append(t)
        changes=request.POST.get('changes')    
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)
    
    #FOR DETERMINANAT OF MATRIX A or MATRIX B
    elif ('detA' in request.POST) or ('detB' in request.POST) :   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        #FOR MATRIX B 
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),2)
           else:
             B1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),2)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
        
        if 'detA' in request.POST: 
           name='A'
           det=int(np.linalg.det(dataA))
        else:
           name='B'
           det=int(np.linalg.det(dataB))

        changes=request.POST.get('changes')        
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'det':det,
          'id':'det',
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  
    
  
    #FOR TRANSPOSE OF MATRIX A or MATRIX B
    elif ('TransposeA' in request.POST ) or ('TransposeB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        #FOR MATRIX B 
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),2)
           else:
             B1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),2)
           else:
             A1[i]=int(temp)  
          
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
        
        det=[]
        if 'TransposeA' in request.POST: 
           name='A'
           det=np.transpose(dataA)
        else:
           name='B'
           det=np.transpose(dataB)

        changes=request.POST.get('changes')        
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'det':det,
          'id':'Transpose',
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  

    
    #FOR INVERSE OF MATRIX A or MATRIX B
    elif ('inverseA' in request.POST ) or ('inverseB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        #FOR MATRIX B 
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),2)
           else:
             B1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),2)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
        
        det=[]
        determinant=1
        
        if 'inverseA' in request.POST: 
           name='A'
           
           if int(np.linalg.det(dataA))==0:
              context={
              'dataA':dataA,
              'dataB':dataB,
              'dimensionA':dimensionA,
              'dimensionB':dimensionB,
              'name':name,
              'message':"Cannot Find Inverse as |A| = 0"
              }
              return render(request,'matrixcalculator.html',context)  
           else:
             det=np.linalg.inv(dataA)
             determinant=float(np.linalg.det(dataA))
        
        else: 
           name='B'
           if int(np.linalg.det(dataB))==0:
              context={
              'dataA':dataA,
              'dataB':dataB,
              'dimensionA':dimensionA,
              'dimensionB':dimensionB,
              'name':name,
              'message':"Cannot Find Inverse as |B| = 0"
              }
              return render(request,'matrixcalculator.html',context)  
           else:
             det=np.linalg.inv(dataB)
             determinant=float(np.linalg.det(dataB))
        
        d1=[]
        for i in range(0,len(det)):
          col=[]
          for j in range(0,len(det[i])):
            col.append(round(det[i][j],5))
          d1.append(col)
        changes=request.POST.get('changes')
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'det':det,
          'd1':d1,
          'id':'inverse',
          'changes':changes,      
        }
        return render(request,'matrixcalculator.html',context)  


    
    #FOR RANK OF MATRIX A or MATRIX B
    elif ('rankA' in request.POST ) or ('rankB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        #FOR MATRIX B 
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),2)
           else:
             B1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),2)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
        


        rank=1
        if 'rankA' in request.POST: 
           name='A'
           rank=np.linalg.matrix_rank(dataA)
        else: 
           name='B'
           rank=np.linalg.matrix_rank(dataB)
        changes=request.POST.get('changes')
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'rank':rank,
          'id':'rank',
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  

    #FOR MULTIPLYING AN INTEGER  IN MATRIX A or MATRIX B
    elif ('multiplyA' in request.POST ) or ('multiplyB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        ansA=[]
        ansB=[]

        name=''
        val=2 
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),2)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),2)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
         
        if "multiplyA" in request.POST:
            mulA=str(request.POST.get("mulA"))
            name='A'
            if '.' in mulA:
                mulA=round(float(mulA),5)
            else:
                mulA=int(mulA)
            
            if mulA !=0:
             val=mulA 
            else:
              val='0'
     
 
            for i in range(0,dimensionA):
               t=[]
               for j in range(0,dimensionA):
                  t.append(round(dataA[i][j]*mulA,5))
               ansA.append(t)   
                   
        else:
            mulB=str(request.POST.get("mulB"))            
            name='B'
            if '.' in mulB:
                mulB=float(mulB)
            else:
                mulB=int(mulB)    
            
            if mulB !=0:
              val=mulB 
            else:
              val='0'

            for i in range(0,dimensionB):
               t=[]
               for j in range(0,dimensionB):
                   t.append(round(dataB[i][j]*mulB,5))
               ansB.append(t)    
        changes=request.POST.get('changes')
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'ansA':ansA,
          'ansB':ansB,
          'id':'mul',
          'val':val,
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  
    

    
    #FOR POWER FOR  AN INTEGER  IN MATRIX A or MATRIX B
    elif ('raiseA' in request.POST ) or ('raiseB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        ansA=[]
        ansB=[]

        name=''
        Raise=2 
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
         
        if "raiseA" in request.POST:
            raA=str(request.POST.get("raA"))
            name='A'
            if '.' in raA:
                raA=round(float(raA),5)
            else:
                raA=int(raA)
            
            ansA=np.linalg.matrix_power(dataA,raA)

            if raA !=0:
              Raise=raA 
            else:
              Raise='0'
            

                   
        else:
            raB=str(request.POST.get("raB"))            
            name='B'

            if '.' in raB:
                raB=float(raB)
            else:
                raB=int(raB)    
            
            ansB=np.linalg.matrix_power(dataB,raB)

            if raB !=0:
              Raise=raB 
            else:
              Raise='0'

        changes=request.POST.get('changes') 
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'ansA':ansA,
          'ansB':ansB,
          'id':"raise",
          'Raise':Raise,
          'id':"raise",
           'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  
    
    
    #FOR LU DECOMPPOSITION MATRIX A or MATRIX B
    elif ('LuA' in request.POST ) or ('LuB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        p=[]
        l=[]
        u=[]

        name=''
        Raise=2 
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
         
        if "LuA" in request.POST:
           name='A'
           p, l, u = scipy.linalg.lu(dataA)
                   
        else:            
            name='B'
            p, l, u = scipy.linalg.lu(dataB)

        for i in range(0,len(l)):
          for j in range(0,len(l[i])):
              l[i][j]=round(l[i][j],5)

        for i in range(0,len(u)):
          for j in range(0,len(u[i])):
              u[i][j]=round(u[i][j],5)
                
        changes=request.POST.get('changes')
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'l':l,
          'u':u,
          'id':"lu",
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  

    
    #FOR CHOLESKY MATRIX A or MATRIX B
    elif ('chomA' in request.POST ) or ('chomB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        p=[]
        l=[]
        u=[]

        name=''
        Raise=2 
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
         
        if "chomA" in request.POST:
         name='A'
         try:  
           l = scipy.linalg.cholesky(dataA,lower=True)
           u = scipy.linalg.cholesky(dataA,lower=False)
         except:
            context={
              'dataA':dataA,
              'dataB':dataB,
              'dimensionA':dimensionA,
              'dimensionB':dimensionB,
              'name':name,
              'message':"Matrix need to be symmetric and positive definite"
              }
            return render(request,'matrixcalculator.html',context)  
    


                   
        else:            
            name='B'
            try:  
                l = scipy.linalg.cholesky(dataB,lower=True)
                u = scipy.linalg.cholesky(dataB,lower=False)
            except:
              context={
                'dataA':dataA,
                'dataB':dataB,
                'dimensionA':dimensionA,
                'dimensionB':dimensionB,
                'name':name,
                'message':"Matrix need to be symmetric and positive definite"
                }
              return render(request,'matrixcalculator.html',context)  
      
        for i in range(0,len(l)):
          for j in range(0,len(l[i])):
              l[i][j]=round(l[i][j],5)

        for i in range(0,len(u)):
          for j in range(0,len(u[i])):
              u[i][j]=round(u[i][j],5)
                
        changes=request.POST.get('changes') 
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'l':l,
          'u':u,
          'id':"cholesky",
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  


    
    #FOR TRIANGULAR FORM OF  MATRIX A or MATRIX B
    elif ('triangleA' in request.POST ) or ('triangleB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        ansA=[]
        ansB=[]

        name=''
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
         
        if "triangleA" in request.POST:
            name='A'
            ansA=TriangularMatrix(dataA)  
        else:            
            name='B'
            ansB=TriangularMatrix(dataB)  
      
        for i in range(0,len(ansA)):
          for j in range(0,len(ansA[i])):
              ansA[i][j]=round(ansA[i][j],5)

        for i in range(0,len(ansB)):
          for j in range(0,len(ansB[i])):
              ansB[i][j]=round(ansB[i][j],5)
                
        changes=request.POST.get('changes')
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'ansB':ansB,
          'ansA':ansA,
          'id':"Triangular",
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  
     
    #FOR Diagonal FORM OF  MATRIX A or MATRIX B
    elif ('diagonalA' in request.POST ) or ('diagonalB' in request.POST):   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]
        p=[]
        D=[]
        p_inv=[]

        name=''
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)
         
        if "diagonalA" in request.POST:
            name='A'
            eigenValues,p=np.linalg.eig(dataA)
            D=np.zeros((dimensionA,dimensionA))
            
            for i in range(dimensionA):
              D[i,i]=eigenValues[i]
            
            p_inv=np.linalg.inv(p)  
             
        else:            
            name='B'
            eigenValues,p=np.linalg.eig(dataB)
            D=np.zeros((dimensionB,dimensionB))
            
            for i in range(dimensionB):
              D[i,i]=eigenValues[i]
            
            p_inv=np.linalg.inv(p)  
      
        for i in range(0,len(p)):
          for j in range(0,len(p[i])):
              p[i][j]=round(p[i][j],5)
              p_inv[i][j]=round(p_inv[i][j],5)
              D[i][j]=round(D[i][j],5)

        changes=request.POST.get('changes')
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':name,
          'p':p,
          'D':D,
          'p_inv':p_inv,
          'id':"diagonal",
          'changes':changes,
        }
        return render(request,'matrixcalculator.html',context)  
     
     #FOR CHANGES   MATRIX A or MATRIX B
    elif 'change' in request.POST:   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]

        name=''
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)

        changes=int(request.POST.get('changes'))
        if changes == 1:
          changes=2
        else:
         changes=1      
        print(changes) 
        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'changes':changes,

        }
        return render(request,'matrixcalculator.html',context)  
    
     #FOR ADDING  MATRIX A and  MATRIX B
    elif 'addAB' in request.POST:   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]

        name=''
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)

        if dimensionA != dimensionB:
          context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':'AB',
          'message':"Dimension of matrix A and B are not equal"
          }
          return render(request,'matrixcalculator.html',context)

        x= np.add(dataA,dataB)
        changes=request.POST.get('changes')

        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'id':'AddAB',
           'x':x,
           'changes':changes,
        }

        return render(request,'matrixcalculator.html',context)  
   
     #FOR SUBTRACTING  MATRIX A and  MATRIX B
    elif 'minusAB' in request.POST:   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]

        name=''
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)

        if dimensionA != dimensionB:
          context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':'AB',
          'message':"Dimension of matrix A and B are not equal"

          }
          return render(request,'matrixcalculator.html',context)
        
        changes=int(request.POST.get('changes'))
        x=[]
        if changes == 2:
         x= np.subtract(dataB,dataA)
        else:
         x= np.subtract(dataA,dataB)


        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'id':'subAB',
           'x':x,
           'changes':changes,
        }

        return render(request,'matrixcalculator.html',context)  
    
     #FOR MULTIPLYING  MATRIX A and  MATRIX B
    elif 'mulAB' in request.POST:   
        dimensionA=int(request.POST.get('dimensionA'))  
        dimensionB=int(request.POST.get('dimensionB'))

        dataA=[]
        dataB=[]

        name=''
        #FOR MATRIX B
        B1=request.POST.getlist('matB')
        for i in range(0,len(B1)):
           temp=str(B1[i])
           if '.' in temp:
             B1[i]=round(float(temp),5)
           else:
             B1[i]=int(temp)  
        
        k=0
        for i in range(0,dimensionB):
            t=[]
            for j in range(0,dimensionB):
              t.append(B1[k])
              k+=1
            dataB.append(t)

        #FOR MATRIX A
        A1=request.POST.getlist('matA')
        for i in range(0,len(A1)):
           temp=str(A1[i])
           if '.' in temp:
             A1[i]=round(float(temp),5)
           else:
             A1[i]=int(temp)  
        
        
        k=0
        for i in range(0,dimensionA):
            t=[]
            for j in range(0,dimensionA):
              t.append(A1[k])
              k+=1
            dataA.append(t)

        if dimensionA != dimensionB:
          context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'name':'AB',
          'message':"Dimension of matrix A and B are not equal"
          }
          return render(request,'matrixcalculator.html',context)
        
        changes=int(request.POST.get('changes'))
        x=[]
        if changes == 2:
         x= np.dot(dataB,dataA)
        else:
         x= np.dot(dataA,dataB)


        context={
          'dataA':dataA,
          'dataB':dataB,
          'dimensionA':dimensionA,
          'dimensionB':dimensionB,
          'id':'mulAB',
           'x':x,
           'changes':changes,
        }

        return render(request,'matrixcalculator.html',context)  
   

    #CODE FOR RESETING THE MATRIX
    elif ("resetA" in request.POST) or ("resetB" in request.POST):
      
      dimensionA=int(request.POST.get('dimensionA'))  
      dimensionB=int(request.POST.get('dimensionB'))
      
      dataA=[]
      dataB=[]

      if   "resetA" in request.POST:
            dataA=[[1,2,3],[4,5,6],[7,8,9]]
            dimensionA=3
            #FOR MATRIX B 
            B1=request.POST.getlist('matB')
            for i in range(0,len(B1)):
              B1[i]=int(B1[i])
            
            k=0
            for i in range(0,dimensionB):
                t=[]
                for j in range(0,dimensionB):
                  t.append(B1[k])
                  k+=1
                dataB.append(t)
      else:
            dataB=[[1,2,3],[4,5,6],[7,8,9]]
            dimensionB=3
            #FOR MATRIX B 
            B1=request.POST.getlist('matA')
            for i in range(0,len(B1)):
              B1[i]=int(B1[i])
            
            k=0
            for i in range(0,dimensionA):
                t=[]
                for j in range(0,dimensionA):
                  t.append(B1[k])
                  k+=1
                dataA.append(t)

      
      context={
        'dataA':dataA,
        'dataB':dataB,
        'dimensionA':dimensionA,
        'dimensionB':dimensionB,
          
      }
      return render(request,'matrixcalculator.html',context)    
                   
            
  else:
    dataA=[[1,2,3],[4,5,6],[7,8,9]]
    dataB=[[1,2,3],[4,5,6],[7,8,9]]
    
    context={
      'dataA':dataA,
      'dataB':dataB
    }
    return render(request,'matrixcalculator.html',context)

def recursivesequencecalculator(request):
  if request.method=='POST':
     given_data=request.POST.get('given_data')

     if request.POST.get('F')!=None and request.POST.get('F')!='' :  
      inp=str(request.POST.get('F'))
      if inp.isdigit():
          F=int(request.POST.get('F'))
      else:
          F=float(request.POST.get('F'))
     else:
        F=None

     if request.POST.get('First')!=None and request.POST.get('First')!='' :  
      inp=str(request.POST.get('First'))
      if inp.isdigit():
          First=int(request.POST.get('First'))
      else:
          First=float(request.POST.get('First'))
     else:
        First=None 
      

     if request.POST.get('CD')!=None and request.POST.get('CD')!='' :  
      inp=str(request.POST.get('CD'))
      if inp.isdigit():
          CD=int(request.POST.get('CD'))
      else:
          CD=float(request.POST.get('CD'))
     else:
        CD=None
     

     if request.POST.get('CR')!=None and request.POST.get('CR')!='' :  
      inp=str(request.POST.get('CR'))
      if inp.isdigit():
          CR=int(request.POST.get('CR'))
      else:
          CR=float(request.POST.get('CR'))
     else:
        CR=None

    
     if given_data=="form1" and F:
      
      F1=F


      def recur_fibo(n):
       if n <= 1:
         return n
       else:
         return(recur_fibo(n-1) + recur_fibo(n-2))

      l = [] 
      for i in range(1,F1+1):
        l.append(recur_fibo(i-1))
     
      context={
         'F1':F1,
        
         'given_data':given_data,
         'l':l,
       }
     
      return render(request,'recursivesequencecalculator.html',context) 

     elif given_data=="form2" and First==0 and CD==0:
       j = []
       for _ in range(F):
         j.append("0")
       
       context={
         'First1':"0",
         'CD1':"0",
         'given_data':given_data,
         'J':j,
         'F1':F,
         
       }

       return render(request,'recursivesequencecalculator.html',context)

     elif given_data=="form2" and First==0  and CD:
       Fir = First
       j = []
       for _ in range(F):
         j.append(First)
         First+=CD
       
       context={
         'First1':Fir,
         'CD1':CD,
         'given_data':given_data,
         'J':j,
         'F1':F,
         
       }

       return render(request,'recursivesequencecalculator.html',context)

        
      
     elif given_data=="form2" and First:
      if CD == 0:
        j = []
        for _ in range(F):
          j.append(First)
        context={
         'First1':First,
         'CD1':CD,
         'given_data':given_data,
         'J':j,
         'F1':F,
         
       }
      
      
        return render(request,'recursivesequencecalculator.html',context)
  
      
      j = []
      F2 = First
      for _ in range(F):
        j.append(First)
        First = First + CD

      context={
         'First1':F2,
         'CD1':CD,
         'given_data':given_data,
         'J':j,
         'F1':F,
          
       }
      
      
      return render(request,'recursivesequencecalculator.html',context)



     elif given_data=="form3" and First==0:
      j = []
      for _ in range(F):
        j.append("0")
       
      context={
         'First1':"0",
         'CR1':CR,
         'given_data':given_data,
         'J':j,
         'F1':F,
         
       }

      return render(request,'recursivesequencecalculator.html',context) 

     elif given_data=="form3" and CR==0:
      j = [First]
      for _ in range(F-1):
        j.append("0")
       
      context={
         'First1':First,
         'CR1':CR,
         'given_data':given_data,
         'J':j,
         'F1':F,
         
       }

      return render(request,'recursivesequencecalculator.html',context) 
 


     elif given_data=="form3" and First and CR:
       
      First1 = First
      F2 = First1
      
      

      
      j = []
      for _ in range(F):
        j.append(F2)
        F2=F2*CR

      context={
         'First1':First1,
         'CR1':CR,
         'given_data':given_data,
         'J':j,
         'F1':F,
       }
      
      return render(request,'recursivesequencecalculator.html',context) 

     else:
       return render(request,'recursivesequencecalculator.html',{'given_data':given_data})
      
      
  else:
    return render(request,'recursivesequencecalculator.html',{'given_data':'form1'})


# from sympy import *
# def convergenceanddivergencecalculator(request):

#   if request.method=='POST':
#     n = symbols('n')
#     F=request.POST.get('F')
#     # print(repr(F))
#     # print(latex(repr(F)))
#     eq = latex(F)
#     print(eq)
#     r = limit(sympify(F),n,oo)
#     if r==oo or r==-oo:
#       context ={
#         'R':r,
#         'First':'First',
#         'F1':F,
#         'Equation':eq
#         }
#       # print(context)
#       return render(request,"convergenceanddivergencecalculator.html",context)
#   else:
#     return render(request,"convergenceanddivergencecalculator.html")


from sympy import *
import math
def sequenceofpartialsumscalculator(request):
  if request.method=='POST':
    F = int(request.POST.get('F')) #assigning user inputs to variables
    U = int(request.POST.get('U')) #assigning user inputs to variables
    S = request.POST.get('S') #assigning user inputs to variables
    
    if math.isnan(F) or math.isnan(U) or int(F) > int(U):
      return render(request,'sequenceofpartialsumscalculator.html',{'message':"From and Upto must be a number and Upto must be bigger than From"})

    if F or U:
      try:
        n = symbols('n')
        expr = sympify(S)
        l = [] #empty list for storing items of generated sequence
        su = [] #this list will contain the sum of sequence of l
        for i in range(int(F),int(U)+1):
          r = limit(expr,n,i)
          l.append(r) #storing items in l.
          su.append(sum(l)) #generating sum of sequence of list l
          # print(r,l)
        context = {
          'F1':F, #lower limit of sequence
          'U1':U, #upper limit of sequence
          'S1':S, #user entered sequence(input)
          'L':l, #list of sequence
          'SU':su, #Sequence of partial sums list
          }
        return render(request,'sequenceofpartialsumscalculator.html',context)
      except (SympifyError,TypeError): #handling errors
        return render(request,'sequenceofpartialsumscalculator.html',{'message':"Please use'*' for multiplication. Exp=> 2n or 2(n) should be written as 2*n and (n+1)(n) should be written as (n+1)*(n+2)"})

    return render(request,'sequenceofpartialsumscalculator.html')
  else:
    return render(request,'sequenceofpartialsumscalculator.html')



def volumetriccalculator(request):
  if request.method == "POST":
    given_data=request.POST.get('given_data')
    if request.POST.get('P')!=None and request.POST.get('P')!='' :  
      inp=str(request.POST.get('P'))
      if inp.isdigit():
          P=int(request.POST.get('P'))
      else:
          P=float(request.POST.get('P'))
    else:
        P=None

    if request.POST.get('W')!=None and request.POST.get('W')!='' :  
      inp=str(request.POST.get('W'))
      if inp.isdigit():
          W=int(request.POST.get('W'))
      else:
          W=float(request.POST.get('W'))
    else:
        W=None

    if request.POST.get('L')!=None and request.POST.get('L')!='' :  
      inp=str(request.POST.get('L'))
      if inp.isdigit():
          L=int(request.POST.get('L'))
      else:
          L=float(request.POST.get('L'))
    else:
        L=None

    if request.POST.get('H')!=None and request.POST.get('H')!='' :  
      inp=str(request.POST.get('H'))
      if inp.isdigit():
          H=int(request.POST.get('H'))
      else:
          H=float(request.POST.get('H'))
    else:
        H=None

    if given_data == "form2" and P:
      try:
        VolumetricWeight = (W*L*H)/6000
        TotalVolumetricWeight = ((W*L*H)/6000)*P
      except TypeError:
        return render(request,'volumetriccalculator.html',{"message":"Please enter inputs"})

      context = {
      "VM":VolumetricWeight,
      "TVM":TotalVolumetricWeight,
      "W1":W,
      "L1":L,
      "H1":H,
      "P1":P,
      'given_data':given_data,
      }
      return render(request,"volumetriccalculator.html",context)
    elif given_data == "form1" and P:
      try:
        VolumetricWeight = (W*L*H)/366
        TotalVolumetricWeight = ((W*L*H)/366)*P
      except TypeError:
        return render(request,'volumetriccalculator.html',{"message":"Please enter inputs"})

      context = {
      "VM":VolumetricWeight,
      "TVM":TotalVolumetricWeight,
      "W1":W,
      "L1":L,
      "H1":H,
      "P1":P,
      'given_data':given_data,
      }
      return render(request,"volumetriccalculator.html",context)
    else:
      return render(request,'volumetriccalculator.html',{'given_data':given_data})
  else:
    return render(request,'volumetriccalculator.html',{'given_data':'form1'})



def freightclasscalculator(request):
  
  def convertToFeet(value, unit):
    """function that converts inches, centimeters and meters to feet"""
    if unit == "Inches": return (value/12)
    elif unit == "Centimeters": return (value/30.48)
    elif unit == "Meters": return (value*3.281)
    else: return value



  if request.method == "POST":
    
    if request.POST.get('L')!=None and request.POST.get('L')!='' :  
      inp=str(request.POST.get('L'))
      if inp.isdigit():
          L=int(request.POST.get('L'))
      else:
          L=float(request.POST.get('L'))
    else:
        L=None

    if request.POST.get('W')!=None and request.POST.get('W')!='' :  
      inp=str(request.POST.get('W'))
      if inp.isdigit():
          W=int(request.POST.get('W'))
      else:
          W=float(request.POST.get('W'))
    else:
        W=None

    if request.POST.get('H')!=None and request.POST.get('H')!='' :  
      inp=str(request.POST.get('H'))
      if inp.isdigit():
          H=int(request.POST.get('H'))
      else:
          H=float(request.POST.get('H'))
    else:
        H=None

    if request.POST.get('TW')!=None and request.POST.get('TW')!='' :  
      inp=str(request.POST.get('TW'))
      if inp.isdigit():
          TW=int(request.POST.get('TW'))
      else:
          TW=float(request.POST.get('TW'))
    else:
        TW=None

    L_op = request.POST.get('L_op')
    W_op = request.POST.get('W_op')
    H_op = request.POST.get('H_op')
    TW_op = request.POST.get('TW_op')

    if (L or L == 0) and (W or W == 0) and (H or H == 0):
      LC = convertToFeet(L,L_op)
      WC = convertToFeet(W,W_op)
      HC = convertToFeet(H,H_op)
      
      volume = LC*WC*HC
      volumeM = (LC*WC*HC)/35.3
    
      if volume == 0:
        density = 'Infinity'
        densityM = 'Infinity'
      else:
        if TW_op == "Lbs":
          density = TW/volume
          densityM = density*16.0185
        else:
          density = (TW*2.205)/volume
          densityM = density*16.0185

      if volume == 0: EFC = " 50"
      elif density < 1: EFC = " 500"
      elif density >= 1 and density < 2: EFC = " 400"
      elif density >=2 and density <3: EFC = " 300"
      elif density >=3 and density <4: EFC = " 250"
      elif density >=4 and density <5: EFC = " 200"
      elif density >=5 and density <6: EFC = " 175"
      elif density >=6 and density <7: EFC = " 150"
      elif density >=7 and density <8: EFC = " 125"
      elif density >=8 and density <9: EFC = " 110"
      elif density >=9 and density <10.5: EFC = " 100"
      elif density >=10.5 and density <12: EFC = " 92.5"
      elif density >=12 and density <13.5: EFC = " 85"
      elif density >=13.5 and density <15: EFC = " 77.5"
      elif density >=15 and density <22.5: EFC = " 70"
      elif density >=22.5 and density <30: EFC = " 65"
      elif density >=30 and density <35: EFC = " 60"
      elif density >=35 and density <50: EFC = " 55"
      else: EFC = " 50"


      context = {
        "L1": L,
        "W1": W,
        "H1": H,
        "TW1": TW,
        "L_op": L_op,
        "W_op": W_op,
        "H_op": H_op,
        "TW_op": TW_op,
        "volume": volume,
        "volumeM": volumeM,
        "density": density,
        "densityM": densityM,
        "EFC": EFC,
      }
      
      return render(request, "freightclasscalculator.html", context)


    return render(request,"freightclasscalculator.html")
  else:
    return render(request,"freightclasscalculator.html")




def repeatingdecimaltofractioncalculator(request):
  from fractions import Fraction #imported Fraction so that output can be generated as fraction
  
  if request.method == "POST":

    if request.POST.get('NR')!=None and request.POST.get('NR')!='' :  
      NRinp=str(request.POST.get('NR'))
      lnr = len(NRinp) #storing length of input
      if NRinp.isdigit():
          NR=int(request.POST.get('NR'))
      else:
          NR=float(request.POST.get('NR'))
    else:
        NR=None

    if request.POST.get('R')!=None and request.POST.get('R')!='' :  
      Rinp=str(request.POST.get('R'))
      lr = len(Rinp) #storing length of input
      if Rinp.isdigit():
          R=int(request.POST.get('R'))
      else:
          R=float(request.POST.get('R'))
    else:
        R=None

    if NR == None and R == None: #runs if both the inputs are blank
      return render(request, "repeatingdecimaltofractioncalculator.html", {"message":"Please input numbers"})

    if (NR or NR==0) and (R or R==0): #runs if both input values are provided
      a = int(str(1)+"0"*lnr)
      a1 = Fraction(NR)/Fraction(a)
      b = int("9"*lr+"0"*lnr)
      a2 = Fraction(R)/Fraction(b) #output in fraction
      result = a1 + a2

      context = {
        "NR1":NRinp, #input stored as string so that initial zeros of input can be preserved
        "R1":Rinp, #input stroed as string so that initial zeros of input can be preserved
        "result":result, #required result for user
      }
      return render(request, "repeatingdecimaltofractioncalculator.html",context)

    if NR or NR == 0: #runs if only one input NR is provided
      a = int(str(1)+"0"*lnr)
      a1 = Fraction(NR)/Fraction(a)
      
      context = {
        "NR1":NRinp, #input stored as string so that initial zeros of input can be preserved
        "R1":"Not Given",
        "result":a1, #required result for user
      }
      return render(request, "repeatingdecimaltofractioncalculator.html",context)

    if R or R == 0: #runs if only one input R is provided
      b = int("9"*lr)
      a2 = Fraction(R)/Fraction(b)
      
      context ={
        "NR1":"Not Given",
        "R1":Rinp, #input stored as string so that initial zeros of input can be preserved
        "result":a2 #required result for user
      }
      return render(request, "repeatingdecimaltofractioncalculator.html",context)
    return render(request, "repeatingdecimaltofractioncalculator.html")
  else:
    return render(request,"repeatingdecimaltofractioncalculator.html") 




def alternativefuelsconversioncalculator(request):
  
  if request.method == "POST":
    if request.POST.get('NU')!=None and request.POST.get('NU')!='' :     
      inp=str(request.POST.get('NU'))
      if inp.isdigit():
          NU=int(request.POST.get('NU'))
      else:
          NU=float(request.POST.get('NU'))
    else:
      NU=None

    NU_op = request.POST.get('NU_op')
    
    if NU == None:
      return render(request, "alternativefuelsconversioncalculator.html",{"message":"please enter input"})

    if NU or NU == 0:
      context = {
      "NU1": NU,
      "NU_op": NU_op,
      "a": NU,
      "b": NU*1.066,
      "c": NU*0.191,
      "d": NU*0.239,
      "e": NU*0.287,
      "f": NU*1.155,
      "g": NU*0.734,
      "h": NU*0.031,
      "i": NU*0.256,
      "j": NU*1.019,
      "k": NU*0.758,
      "l": NU*0.666,
    }
      return render(request, "alternativefuelsconversioncalculator.html",context)
    return render(request, "alternativefuelsconversioncalculator.html")
  else:
    return render(request, "alternativefuelsconversioncalculator.html")



def rgbhexcalculator(request):
  
  if request.method == "POST":
    given_data=request.POST.get('given_data')
    if request.POST.get('R')!=None and request.POST.get('R')!='' :     
      inp=str(request.POST.get('R'))
      if inp.isdigit():
          R=int(request.POST.get('R'))
      else:
          R=float(request.POST.get('R'))
    else:
      R=None

    if request.POST.get('G')!=None and request.POST.get('G')!='' :     
      inp=str(request.POST.get('G'))
      if inp.isdigit():
          G=int(request.POST.get('G'))
      else:
          G=float(request.POST.get('G'))
    else:
      G=None

    if request.POST.get('B')!=None and request.POST.get('B')!='' :     
      inp=str(request.POST.get('B'))
      if inp.isdigit():
          B=int(request.POST.get('B'))
      else:
          B=float(request.POST.get('B'))
    else:
      B=None

    if request.POST.get('H')!=None and request.POST.get('H')!='' :     
      H=str(request.POST.get('H'))
    else:
      H=None
      
    if given_data=="form1" and (isinstance(R, float) or isinstance(G, float) or isinstance(B, float)):
      return render(request, "rgbhexcalculator.html",{"message":"Please provide values without decimal point","given_data":given_data})
    
    if (R or R==0) and (G or G==0) and (B or B==0):

      def addZero(a):
        """adds zero before input if input is single digit"""
        if len(str(a)) == 1:
          a = "0"+str(a)
          return a
        return a

      R1 = hex(R).split("x")[-1] #converting input value to hexadecimal and splitting required output
      G1 = hex(G).split("x")[-1] #converting input value to hexadecimal and splitting required output
      B1 = hex(B).split("x")[-1] #converting input value to hecadecimal and splitting required output
      

      R1 = addZero(R1) #calling function to check if input is single digit if yes
      G1 = addZero(G1) #then add zero as string in front of them
      B1 = addZero(B1)
      

      result = str(R1)+str(G1)+str(B1) #required output for the user
      
      context = {
        "R":R,
        "G":G,
        "B":B,
        "given_data":given_data,
        "result":result
      }
      return render(request, "rgbhexcalculator.html",context)

    if given_data == "form2" and H:
      if len(H) != 6:
        return render(request, "rgbhexcalculator.html",{"message":"Hexadecimal values must be 6 digits long with numbers 0-9 and letters A-F", "given_data":given_data})
      
      for i in H:
        if i not in "0123456789abcdefABCDEF": #validating the user's input
          return render(request, "rgbhexcalculator.html",{"message":"Hexadecimal values must be 6 digits long with numbers 0-9 and letters A-F", "given_data":given_data,"H":H})
      
      l = []
      for i in range(0,len(H),2): #separating user inputs in two-two digints
        dec = int(H[i:i+2], 16) #converting Hex to RGB
        l.append(dec) # adding output in list l
      context ={
        "Red":l[0],
        "Green":l[1],
        "Blue":l[2],
        "H":H,
        "result":"result",
        "given_data":given_data
      }
      return render(request,"rgbhexcalculator.html",context)

    return render(request, "rgbhexcalculator.html",{'given_data':given_data})
  else:
    return render(request, "rgbhexcalculator.html",{'given_data':"form1"}) 




def insidecartemperaturecalculator(request):
  
  if request.method == "POST":
    if request.POST.get('T')!=None and request.POST.get('T')!='' :  
      #value for Temperature   
      inp=str(request.POST.get('T'))
      Tinp=inp #storing input as string so that user can see initial zeros in input
      if inp.isdigit():
        T=int(request.POST.get('T'))
      else:
        T=float(request.POST.get('T'))
    else:
      T=None

    if request.POST.get('M')!=None and request.POST.get('M')!='' :  
      #value for Time
      inp=str(request.POST.get('M'))
      Minp=inp #storing input as string so that user can see initial zeros in input
      if inp.isdigit():
        M=int(request.POST.get('M'))
      else:
        M=float(request.POST.get('M'))
    else:
      M=None

    if request.POST.get('TU')!=None and request.POST.get('TU')!='' :
      #value for temperature unit     
      TU=str(request.POST.get('TU'))
    else:
      TU=None

    
    if TU == "C": #converting input fahrenheit to celsius
      T = (T * 9/5) + 32
      
    if (T or T == 0) and (M or M == 0):
      if TU != "C":
        T = int(str(T).split('.')[0])
      M = int(str(M).split('.')[0])
      
      if M>=0 and M<=10:
        r = (M*1.9+T)
      elif M>=11 and M<=20:
        r = ((M+9)+T)
      elif M>=21 and M<=30:
        r = ((M*0.5)+T+19)
      elif M>=31 and M<=40:
        r = ((M*0.4)+T+22)
      elif M>=41 and M<=50:
        r = ((M*0.3)+T+26)
      elif M>=50 and M<=60:
        r = ((M*0.2)+T+31)
      elif M>60:
        j = 1
        for _ in range(60,M):
          r = 43+((1/30)*j)+T
          j += 1

      if TU == "C":
        r = (r - 32) * 5/9 # converting result into celsius
      
      context = {
        "TU":TU, #storing temperature unit
        "T1":Tinp, #input as string so that user can see the initial zeros in input
        "M1":Minp, #input as string so that user can see the initial zeros in input
        "result":r #required result after the calculation
      }
      return render(request, "insidecartemperaturecalculator.html", context)

    return render(request, "insidecartemperaturecalculator.html")
  else:
    return render(request, "insidecartemperaturecalculator.html")




def raintosnowcalculator(request):
  
  if request.method == "POST":
    #storing value for temperature
    if request.POST.get('T')!=None and request.POST.get('T')!='' :  
      inp=str(request.POST.get('T'))
      Tinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        T=int(request.POST.get('T'))
      else:
        T=float(request.POST.get('T'))
    else:
      T=None

    #storing value for Rainfall
    if request.POST.get('R')!=None and request.POST.get('R')!='' :  
      inp=str(request.POST.get('R'))
      Rinp=inp #storing input as string so that initial zeros in input can be preserved
      if inp.isdigit():
        R=int(request.POST.get('R'))
      else:
        R=float(request.POST.get('R'))
    else:
      R=None

    #storing value for Temperature Unit
    if request.POST.get('TU')!=None and request.POST.get('TU')!='' :
      TU=str(request.POST.get('TU'))
    else:
      TU=None

    #converting celsius to fahrenheit
    if TU == "C":
      T = (T * 9/5) + 32

    if (T or T == 0) and (R or R == 0):
      if T<=-21:
        SD = R*100
        SR = "1:100" 
      elif T<=-1 and T>=-20:
        SD = R*50
        SR = "1:50" 
      elif T>=0 and T<=9:
        SD = R*40
        SR = "1:40" 
      elif T>=10 and T<=14:
        SD = R*30
        SR = "1:30" 
      elif T>=15 and T<=19:
        SD = R*20
        SR = "1:20" 
      elif T>=20 and T<=27:
        SD = R*15
        SR = "1:15" 
      elif T>=28:
        SD = R*10
        SR = "1:10" 
      
      #creating dictionary for storing all the information that user needs to see
      context = {
        "TU":TU, #storing temperature unit
        "T1":Tinp, #input as string so that user can see the initial zeros in input
        "R1":Rinp, #input as string so that user can see the initial zeros in input
        "result":SD, #required result after the calculation in inches
        "SR":SR, # value will reflect the Snow Ratio
        "SD1":R*10, #Key:value pair created to pass data to frontend table
        "SD2":R*15, #Key:value pair created to pass data to frontend table
        "SD3":R*20, #Key:value pair created to pass data to frontend table
        "SD4":R*30, #Key:value pair created to pass data to frontend table
        "SD5":R*40, #Key:value pair created to pass data to frontend table
        "SD6":R*50, #Key:value pair created to pass data to frontend table
        "SD7":R*100, #Key:value pair created to pass data to frontend table
      }
      
      return render(request, "raintosnowcalculator.html", context)

    return render(request, "raintosnowcalculator.html")
  else:
    return render(request, "raintosnowcalculator.html")





def snowcalculator(request):

  def temperatureConversion(value, unit):
    """converts temperature into celsius"""
    if unit == "Kelvin": return value - 273.15
    elif unit == "Fahrenheit": return (value - 32) * 5/9
    else: return value


  def depthConversion(value, unit):
    """converts input into meters"""
    if unit == "Inches": return value * 0.0254
    elif unit == "Feet": return value * 0.3048
    elif unit == "Centimeters": return value * 0.01
    elif unit == "Yards": return value *  0.9144
    else: return value


  def areaConversion(value, unit):
    """converts input into square meters"""
    if unit == "Acres": return value * 4046.8564224
    elif unit == "Hectares": return value * 10000
    elif unit == "SCentimeters": return value * 0.0001
    elif unit == "SFeet": return value * 0.09290304
    elif unit == "SInches": return value * 0.00064516
    elif unit == "SKilometers": return value * 1000000
    elif unit == "SMiles": return value * 2589988.110336
    elif unit == "SMillimeters": return value * 0.000001	
    elif unit == "SYards": return value * 0.83612736
    else: return value


  if request.method == "POST":
    

    if request.POST.get('T')!=None and request.POST.get('T')!='' :  
      #value for Air Temperature
      inp=str(request.POST.get('T'))
      Tinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        T=int(request.POST.get('T'))
      else:
        T=float(request.POST.get('T'))
    else:
      T=None

    if request.POST.get('D')!=None and request.POST.get('D')!='' :  
      #value for Snow Depth
      inp=str(request.POST.get('D'))
      Dinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        D=int(request.POST.get('D'))
      else:
        D=float(request.POST.get('D'))
    else:
      D=None

    if request.POST.get('A')!=None and request.POST.get('A')!='' : 
      #value for Area 
      inp=str(request.POST.get('A'))
      Ainp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        A=int(request.POST.get('A'))
      else:
        A=float(request.POST.get('A'))
    else:
      A=None

    T_op = request.POST.get('T_op') #grabbing temperature unit
    D_op = request.POST.get('D_op') #grabbing snow-depth unit
    A_op = request.POST.get('A_op') #grabbing area unit

    T = temperatureConversion(T, T_op) #converting input into celcius
    D = depthConversion(D, D_op) #converting input into meters
    A = areaConversion(A, A_op) #converting input into square meters
    

    if T != None or T == 0:
      if T<=0:
        SD = 67.92 + 51.25 * (2.718282**(T/2.59)) #SD is snow density
      else:
        SD = min(200, (119.17 + 20 * T)) # SD is snow density
    

    if (D or D == 0) and (A or A == 0):
      SW = SD *(D * A) # Snow weight
      
      context = {
      "T1": Tinp, # temperature
      "D1": Dinp, #snow depth
      "A1": Ainp, #area 
      "T_op": T_op, # temperature unit
      "D_op": D_op, # snow depth unit
      "A_op": A_op, #air unit
      "SD": SD, #snow density
      "SW": SW, #snow weight
      }
      return render(request, "snowcalculator.html", context)


    return render(request, "snowcalculator.html",{"message":"Enter correct input values"})
  else:
    return render(request, "snowcalculator.html")







def rainwatercollectioncalculator(request):
  
  if request.method == "POST":
    #storing form value
    given_data = request.POST.get("given_data")

    if request.POST.get('A')!=None and request.POST.get('A')!='' :  
      #value for Rainwater Catchment Area
      inp=str(request.POST.get('A'))
      Ainp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        A=int(request.POST.get('A'))
      else:
        A=float(request.POST.get('A'))
    else:
      A=None

    if request.POST.get('RC')!=None and request.POST.get('RC')!='' :  
      #value for Runoff Coefficient
      inp=str(request.POST.get('RC'))
      RCinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        RC=int(request.POST.get('RC'))
      else:
        RC=float(request.POST.get('RC'))
    else:
      RC=None

    if request.POST.get('S')!=None and request.POST.get('S')!='' :  
      #value for Tank Size
      inp=str(request.POST.get('S'))
      Sinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        S=int(request.POST.get('S'))
      else:
        S=float(request.POST.get('S'))
    else:
      S=None

    if request.POST.get('V')!=None and request.POST.get('V')!='' :  
      #value for Tank Starting Volume
      inp=str(request.POST.get('V'))
      Vinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        V=int(request.POST.get('V'))
      else:
        V=float(request.POST.get('V'))
    else:
      V=None

    if request.POST.get('jan')!=None and request.POST.get('jan')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('jan'))
      janinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        jan=int(request.POST.get('jan'))
      else:
        jan=float(request.POST.get('jan'))
    else:
      jan=None

    if request.POST.get('feb')!=None and request.POST.get('feb')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('feb'))
      febinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        feb=int(request.POST.get('feb'))
      else:
        feb=float(request.POST.get('feb'))
    else:
      feb=None

    if request.POST.get('mar')!=None and request.POST.get('mar')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('mar'))
      marinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        mar=int(request.POST.get('mar'))
      else:
        mar=float(request.POST.get('mar'))
    else:
      mar=None

    if request.POST.get('apr')!=None and request.POST.get('apr')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('apr'))
      aprinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        apr=int(request.POST.get('apr'))
      else:
        apr=float(request.POST.get('apr'))
    else:
      apr=None

    if request.POST.get('may')!=None and request.POST.get('may')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('may'))
      mayinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        may=int(request.POST.get('may'))
      else:
        may=float(request.POST.get('may'))
    else:
      may=None

    if request.POST.get('jun')!=None and request.POST.get('jun')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('jun'))
      juninp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        jun=int(request.POST.get('jun'))
      else:
        jun=float(request.POST.get('jun'))
    else:
      jun=None

    if request.POST.get('jul')!=None and request.POST.get('jul')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('jul'))
      julinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        jul=int(request.POST.get('jul'))
      else:
        jul=float(request.POST.get('jul'))
    else:
      jul=None

    if request.POST.get('aug')!=None and request.POST.get('aug')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('aug'))
      auginp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        aug=int(request.POST.get('aug'))
      else:
        aug=float(request.POST.get('aug'))
    else:
      aug=None

    if request.POST.get('sep')!=None and request.POST.get('sep')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('sep'))
      sepinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        sep=int(request.POST.get('sep'))
      else:
        sep=float(request.POST.get('sep'))
    else:
      sep=None

    if request.POST.get('oct')!=None and request.POST.get('oct')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('oct'))
      octinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        oct=int(request.POST.get('oct'))
      else:
        oct=float(request.POST.get('oct'))
    else:
      oct=None

    if request.POST.get('nov')!=None and request.POST.get('nov')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('nov'))
      novinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        nov=int(request.POST.get('nov'))
      else:
        nov=float(request.POST.get('nov'))
    else:
      nov=None

    if request.POST.get('dec')!=None and request.POST.get('dec')!='' :  
      #value for Average Rainfall in month
      inp=str(request.POST.get('dec'))
      decinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        dec=int(request.POST.get('dec'))
      else:
        dec=float(request.POST.get('dec'))
    else:
      dec=None

    if request.POST.get('jan1')!=None and request.POST.get('jan1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('jan1'))
      jan1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        jan1=int(request.POST.get('jan1'))
      else:
        jan1=float(request.POST.get('jan1'))
    else:
      jan1=None

    if request.POST.get('feb1')!=None and request.POST.get('feb1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('feb1'))
      feb1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        feb1=int(request.POST.get('feb1'))
      else:
        feb1=float(request.POST.get('feb1'))
    else:
      feb1=None

    if request.POST.get('mar1')!=None and request.POST.get('mar1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('mar1'))
      mar1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        mar1=int(request.POST.get('mar1'))
      else:
        mar1=float(request.POST.get('mar1'))
    else:
      mar1=None

    if request.POST.get('apr1')!=None and request.POST.get('apr1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('apr1'))
      apr1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        apr1=int(request.POST.get('apr1'))
      else:
        apr1=float(request.POST.get('apr1'))
    else:
      apr1=None

    if request.POST.get('may1')!=None and request.POST.get('may1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('may1'))
      may1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        may1=int(request.POST.get('may1'))
      else:
        may1=float(request.POST.get('may1'))
    else:
      may1=None

    if request.POST.get('jun1')!=None and request.POST.get('jun1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('jun1'))
      jun1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        jun1=int(request.POST.get('jun1'))
      else:
        jun1=float(request.POST.get('jun1'))
    else:
      jun1=None

    if request.POST.get('jul1')!=None and request.POST.get('jul1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('jul1'))
      jul1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        jul1=int(request.POST.get('jul1'))
      else:
        jul1=float(request.POST.get('jul1'))
    else:
      jul1=None

    if request.POST.get('aug1')!=None and request.POST.get('aug1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('aug1'))
      aug1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        aug1=int(request.POST.get('aug1'))
      else:
        aug1=float(request.POST.get('aug1'))
    else:
      aug1=None

    if request.POST.get('sep1')!=None and request.POST.get('sep1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('sep1'))
      sep1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        sep1=int(request.POST.get('sep1'))
      else:
        sep1=float(request.POST.get('sep1'))
    else:
      sep1=None

    if request.POST.get('oct1')!=None and request.POST.get('oct1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('oct1'))
      oct1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        oct1=int(request.POST.get('oct1'))
      else:
        oct1=float(request.POST.get('oct1'))
    else:
      oct1=None

    if request.POST.get('nov1')!=None and request.POST.get('nov1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('nov1'))
      nov1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        nov1=int(request.POST.get('nov1'))
      else:
        nov1=float(request.POST.get('nov1'))
    else:
      nov1=None

    if request.POST.get('dec1')!=None and request.POST.get('dec1')!='' :  
      #value for Rainwater Usage in month
      inp=str(request.POST.get('dec1'))
      dec1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        dec1=int(request.POST.get('dec1'))
      else:
        dec1=float(request.POST.get('dec1'))
    else:
      dec1=None

    
    #value of the calculate button
    f1 = request.POST.get("f1") 

    
    if (A or A == 0) and (RC or RC == 0) and (S or S == 0) and (V or V == 0) and f1:

      RFsum = jan+feb+mar+apr+may+jun+jul+aug+sep+oct+nov+dec
      RWUsum = jan1+feb1+mar1+apr1+may1+jun1+jul1+aug1+sep1+oct1+nov1+dec1

      #CALCULATING RAINWATER HARVESTED IN EVERY MONTH
      RHjan = A * jan * RC * 0.623
      RHfeb = A * feb * RC * 0.623
      RHmar = A * mar * RC * 0.623
      RHapr = A * apr * RC * 0.623
      RHmay = A * may * RC * 0.623
      RHjun = A * jun * RC * 0.623
      RHjul = A * jul * RC * 0.623
      RHaug = A * aug * RC * 0.623
      RHsep = A * sep * RC * 0.623
      RHoct = A * oct * RC * 0.623
      RHnov = A * nov * RC * 0.623
      RHdec = A * dec * RC * 0.623
      RHsum = RHjan+RHfeb+RHmar+RHapr+RHmay+RHjun+RHjul+RHaug+RHsep+RHoct+RHnov+RHdec
      

      
      # CALCULATING TANK INFLOW/OUTFLOW FOR EVERY MONTH
      RUjan = RHjan - jan1
      RUfeb = RHfeb - feb1
      RUmar = RHmar - mar1
      RUapr = RHapr - apr1
      RUmay = RHmay - may1
      RUjun = RHjun - jun1
      RUjul = RHjul - jul1
      RUaug = RHaug - aug1
      RUsep = RHsep - sep1
      RUoct = RHoct - oct1
      RUnov = RHnov - nov1
      RUdec = RHdec - dec1
      RUsum = RUjan+RUfeb+RUmar+RUapr+RUmay+RUjun+RUjul+RUaug+RUsep+RUoct+RUnov+RUdec

      
      #CALCULATING TANK LEVEL FOR EVERY MONTH
      TLjan = min(S,max(0,V + RHjan - jan1))
      TLfeb = min(S,max(0,TLjan + RUfeb))
      TLmar = min(S,max(0,TLfeb + RUmar))
      TLapr = min(S,max(0,TLmar + RUapr))
      TLmay = min(S,max(0,TLapr + RUmay))
      TLjun = min(S,max(0,TLmay + RUjun))
      TLjul = min(S,max(0,TLjun + RUjul))
      TLaug = min(S,max(0,TLjul + RUaug))
      TLsep = min(S,max(0,TLaug + RUsep))
      TLoct = min(S,max(0,TLsep + RUoct))
      TLnov = min(S,max(0,TLoct + RUnov))
      TLdec = min(S,max(0,TLnov + RUdec))
      TLsum = TLjan+TLfeb+TLmar+TLapr+TLmay+TLjun+TLjul+TLaug+TLsep+TLoct+TLnov+TLdec

      
      #CALCULATING RAINWATER OVERFLOW FOR EVERY MONTH
      ROjan = abs(min(0,S - RUjan + V))
      ROfeb = max(0,TLjan + RUfeb - S)
      ROmar = max(0,TLfeb + RUmar - S)
      ROapr = max(0,TLmar + RUapr - S)
      ROmay = max(0,TLapr + RUmay - S)
      ROjun = max(0,TLmay + RUjun - S)
      ROjul = max(0,TLjun + RUjul - S)
      ROaug = max(0,TLjul + RUaug - S)
      ROsep = max(0,TLaug + RUsep - S)
      ROoct = max(0,TLsep + RUoct - S)
      ROnov = max(0,TLoct + RUnov - S)
      ROdec = max(0,TLnov + RUdec - S)
      ROsum = ROjan+ROfeb+ROmar+ROapr+ROmay+ROjun+ROjul+ROaug+ROsep+ROoct+ROnov+ROdec
      
      
      #CALCULATING WATER DEFICIT EVERY MONTH
      WDjan = abs(min(0, RHjan + V - jan1 + TLjan))
      WDfeb = abs(min(0,RHfeb - feb1 + TLjan))
      WDmar = abs(min(0,RHmar - mar1 + TLfeb))
      WDapr = abs(min(0,RHapr - apr1 + TLmar))
      WDmay = abs(min(0,RHmay - may1 + TLapr))
      WDjun = abs(min(0,RHjun - jun1 + TLmay))
      WDjul = abs(min(0,RHjul - jul1 + TLjun))
      WDaug = abs(min(0,RHaug - aug1 + TLjul))
      WDsep = abs(min(0,RHsep - sep1 + TLaug))
      WDoct = abs(min(0,RHoct - oct1 + TLsep))
      WDnov = abs(min(0,RHnov - nov1 + TLoct))
      WDdec = abs(min(0,RHdec - dec1 + TLnov))
      WDsum = WDjan+WDfeb+WDmar+WDapr+WDmay+WDjun+WDjul+WDaug+WDsep+WDoct+WDnov+WDdec
      

      

      context = {
        #THESE VALUES WILL BE VISIBLE IN THE INPUT FIELDS
        "A1":Ainp,
        "RC1":RCinp,
        "S1":Sinp,
        "V1":Vinp,

        #sum of total rainfall in inches of every month
        "RFsum":RFsum,

        #sum of total rainwater useage of every month
        "RWUsum":RWUsum,
        # VALUE FOR AVERAGE RAINFALL IN INCHES
        "jan":janinp,
        "feb":febinp,
        "mar":marinp,
        "apr":aprinp,
        "may":mayinp,
        "jun":juninp,
        "jul":julinp,
        "aug":auginp,
        "sep":sepinp,
        "oct":octinp,
        "nov":novinp,
        "dec":decinp,
        

        #VALUE FOR RAINWATER USAGE IN GALLONS
        "jan1":jan1inp,
        "feb1":feb1inp,
        "mar1":mar1inp,
        "apr1":apr1inp,
        "may1":may1inp,
        "jun1":jun1inp,
        "jul1":jul1inp,
        "aug1":aug1inp,
        "sep1":sep1inp,
        "oct1":oct1inp,
        "nov1":nov1inp,
        "dec1":dec1inp,

        #VALUE FOR RAINWATER HARVESTED
        "RHjan":RHjan,
        "RHfeb":RHfeb,
        "RHmar":RHmar,
        "RHapr":RHapr,
        "RHmay":RHmay,
        "RHjun":RHjun,
        "RHjul":RHjul,
        "RHaug":RHaug,
        "RHsep":RHsep,
        "RHoct":RHoct,
        "RHnov":RHnov,
        "RHdec":RHdec,
        "RHsum":RHsum,

        #VALUE FOR TANK INFLOW/OUTFLOW
        "TIOjan":RUjan,
        "TIOfeb":RUfeb,
        "TIOmar":RUmar,
        "TIOapr":RUapr,
        "TIOmay":RUmay,
        "TIOjun":RUjun,
        "TIOjul":RUjul,
        "TIOaug":RUaug,
        "TIOsep":RUsep,
        "TIOoct":RUoct,
        "TIOnov":RUnov,
        "TIOdec":RUdec,
        "TIOsum":RUsum,
        
        #VALUE FOR TANK LEVEL
        "TLjan":TLjan,
        "TLfeb":TLfeb,
        "TLmar":TLmar,
        "TLapr":TLapr,
        "TLmay":TLmay,
        "TLjun":TLjun,
        "TLjul":TLjul,
        "TLaug":TLaug,
        "TLsep":TLsep,
        "TLoct":TLoct,
        "TLnov":TLnov,
        "TLdec":TLdec,
        "TLsum":TLsum,

        #VALUE FOR RAINWATER OVERFLOW
        "ROjan":ROjan,
        "ROfeb":ROfeb,
        "ROmar":ROmar,
        "ROapr":ROapr,
        "ROmay":ROmay,
        "ROjun":ROjun,
        "ROjul":ROjul,
        "ROaug":ROaug,
        "ROsep":ROsep,
        "ROoct":ROoct,
        "ROnov":ROnov,
        "ROdec":ROdec,
        "ROsum":ROsum,

        #VALUE FOR WATER DEFICIT
        "WDjan":WDjan,
        "WDfeb":WDfeb,
        "WDmar":WDmar,
        "WDapr":WDapr,
        "WDmay":WDmay,
        "WDjun":WDjun,
        "WDjul":WDjul,
        "WDaug":WDaug,
        "WDsep":WDsep,
        "WDoct":WDoct,
        "WDnov":WDnov,
        "WDdec":WDdec,
        "WDsum":WDsum,

        #passing value for form
        "given_data":given_data,

        #passing value so that result can be seen
        "f1":f1,
      }
      
      return render(request, "rainwatercollectioncalculator.html",context)
      
    return render(request, "rainwatercollectioncalculator.html",{"given_data":given_data})
  else:
    return render(request, "rainwatercollectioncalculator.html",{'given_data':"form1"})






def estimatedtimeofarrivalcalculator(request):
  if request.method == "POST":
    
    # storing value of form
    given_data = request.POST.get("given_data")

    #value for Total Distance to Drive
    DT = request.POST.get("DT")

    #value for Scheduled Stops
    SS = request.POST.get("SS")

    #value for Avg time at each stop in hours
    ATH = request.POST.get("ATH")

    #value for Avg time at each stop in hours
    ATM = request.POST.get("ATM")

    #value of the calculate button
    f1 = request.POST.get("f1")


    if request.POST.get('D')!=None and request.POST.get('D')!='' :  
      #value for Total Distance To Drive
      inp=str(request.POST.get('D'))
      Dinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        D=int(request.POST.get('D'))
      else:
        D=float(request.POST.get('D'))
    else:
      D=None


    if request.POST.get('S')!=None and request.POST.get('S')!='' :  
      #value for Average Vehicle Speed
      inp=str(request.POST.get('S'))
      Sinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        S=int(request.POST.get('S'))
      else:
        S=float(request.POST.get('S'))
    else:
      S=None


    #Calculating estimated time of arrival by using user inputs
    if (D or D == 0) and (S or S == 0) and DT and f1:
     #calculation for Total Drive Time: =====
      #changing user inputs into hours
      TT = (D/S)+int(SS)*(int(ATH)+(int(ATM)*0.0166667))
      #Splitting Hours before decimal point
      Hour = str(TT).split(".")[0]
      #changing hours after decimal into minutes
      Minutes = float("0."+str(TT).split(".")[-1])*60
      

    #calculation for Estimated Date and Time of Arrival: =====
      import datetime
      #storing year, month and date in variables
      year, month, date = (int(i) for i in DT.split("T")[0].split("-"))
      #storing hour and minutes in variables
      hr, mn = (int(i) for i in DT.split("T")[1].split(":"))
      #storing date given by user into variables
      my_date = datetime.datetime(year, month, date, hr, mn)
      #adding date with the Total Drive Time and storing its value in variable
      my_date_minutes = my_date + datetime.timedelta(hours = int(Hour), minutes = Minutes)
      #formating the date to show for showing in the frontend
      resultDate = my_date_minutes.strftime("%A, %b %d, %Y, %I:%M %p")

      #creating dictionary to pass all the neccessare value to template
      context = {
        "S":Sinp, #value for Avg Vehicle Speed
        "D":Dinp, #value for Total Distance to Drive
        "DT":DT, #value for Departure Date and Time
        "SS":SS, #value for Scheduled Stops
        "ATH":ATH, #value for Avg Time @ Each Stop in hours
        "ATM":ATM, #value for Avg Time # Each Stop in minutes
        "f1":f1, #calculate Button value
        "Hour":Hour, #Required Result in Hours
        "Minutes":Minutes, #Required Result in Minutes
        "resultDate":resultDate, # Required Result with Date and Time
        "given_data":given_data, #passing form value
      }

      return render(request, "estimatedtimeofarrivalcalculator.html",context)

    #following code runs when Unit System in Changed  
    return render(request, "estimatedtimeofarrivalcalculator.html",{"given_data":given_data})
  else:
    return render(request, "estimatedtimeofarrivalcalculator.html",{'given_data':"form1"})









def englishlearningtimecalculator(request):
  if request.method == "POST":
    
    if request.POST.get('TH')!=None and request.POST.get('TH')!='' :  
      #value for Avg lesson time in hrs
      inp=str(request.POST.get('TH'))
      THinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH=int(request.POST.get('TH'))
      else:
        TH=float(request.POST.get('TH'))
    else:
      TH=None

    if request.POST.get('TM')!=None and request.POST.get('TM')!='' :  
      #value for Avg lesson time in minutes
      inp=str(request.POST.get('TM'))
      TMinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM=int(request.POST.get('TM'))
      else:
        TM=float(request.POST.get('TM'))
    else:
      TM=None

    if request.POST.get('TH1')!=None and request.POST.get('TH1')!='' :  
      #value for total weekly time in hours
      inp=str(request.POST.get('TH1'))
      TH1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH1=int(request.POST.get('TH1'))
      else:
        TH1=float(request.POST.get('TH1'))
    else:
      TH1=None

    if request.POST.get('TM1')!=None and request.POST.get('TM1')!='' :  
      #value for total weekly time in minutes
      inp=str(request.POST.get('TM1'))
      TM1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM1=int(request.POST.get('TM1'))
      else:
        TM1=float(request.POST.get('TM1'))
    else:
      TM1=None

    #storing value to calculate button
    f1 = request.POST.get("f1")
    
    if (TH == 0 and TM == 0) or (TH1 == 0 and TM1 == 0):
      return render(request, "englishlearningtimecalculator.html",{"message":"Both Hours and Minutes can't be zero"})

    # if TH1<TH:
    #   return render(request, "englishlearningtimecalculator.html",{"message":"Total time weekly must be greater than or equal to Avg lesson time"})

    if type(TH) == float or type(TM) == float or type(TH1) == float or type(TM1) == float:
      return render(request, "englishlearningtimecalculator.html",{"message":"Please enter inputs without decimal points"})

    if (TH or TH == 0) and (TM or TM == 0) and (TH1 or TH1 == 0) and (TM1 or TM1 == 0) and f1:
      #converting hours into minutes
      TH = TH * 60
      TH1 = TH1 * 60

      #storing average lesson time in minutes
      ALT = TH+TM

      #storing total time weekly in minutes
      TTW = TH1+TM1

      #storing value of total lessons per week
      LW = TTW/ALT
      
      A1ToA2 = max(0,1330/((TH1)+TM1*0.0166667))
      A2ToB1 = A1ToA2 * 2
      B1ToB2 = A1ToA2 * 2.9
      B2ToC1 = A1ToA2 * 3.9
      C1ToC2 = A1ToA2 * 5.8
      A1ToC2 = A1ToA2 * 15.6
      
      #dictionary created to pass all the necessary values to templates
      context = {
        "TH":THinp,
        "TM":TMinp,
        "TH1":TH1inp,
        "TM1":TM1inp,
        "LW":LW,
        "A1ToA2":A1ToA2,
        "A2ToB1":A2ToB1,
        "B1ToB2":B1ToB2,
        "B2ToC1":B2ToC1,
        "C1ToC2":C1ToC2,
        "A1ToC2":A1ToC2,
        "f1":f1,
      }
      
      return render(request, "englishlearningtimecalculator.html",context)
      
  
    return render(request, "englishlearningtimecalculator.html")
  else:
    return render(request, "englishlearningtimecalculator.html")








def meetingcostcalculator(request):
  if request.method == "POST":
    

    def salaryConversion(value, op):
      """converts salary as per hourly basis"""
      if op == "Week": return value * 0.025
      elif op == "Month": return value * 0.005769341718109963 
      elif op == "Year": return value * 0.0004807692307692308
      else: return value

    if request.POST.get('AS')!=None and request.POST.get('AS')!='' :  
      #value for Average salary
      inp=str(request.POST.get('AS'))
      ASinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        AS=int(request.POST.get('AS'))
      else:
        AS=float(request.POST.get('AS'))
    else:
      AS=None

    if request.POST.get('NA')!=None and request.POST.get('NA')!='' :  
      #value for Number of attendants
      inp=str(request.POST.get('NA'))
      NAinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        NA=int(request.POST.get('NA'))
      else:
        NA=float(request.POST.get('NA'))
    else:
      NA=None

    if request.POST.get('TH')!=None and request.POST.get('TH')!='' :  
      #value for Meeting duration in hours
      inp=str(request.POST.get('TH'))
      THinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH=int(request.POST.get('TH'))
      else:
        TH=float(request.POST.get('TH'))
    else:
      TH=None

    if request.POST.get('TM')!=None and request.POST.get('TM')!='' :  
      #value for Meeting duration in minutes
      inp=str(request.POST.get('TM'))
      TMinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM=int(request.POST.get('TM'))
      else:
        TM=float(request.POST.get('TM'))
    else:
      TM=None

    if request.POST.get('TH1')!=None and request.POST.get('TH1')!='' :  
      #value for Time spent on setting up the meeting in hours
      inp=str(request.POST.get('TH1'))
      TH1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH1=int(request.POST.get('TH1'))
      else:
        TH1=float(request.POST.get('TH1'))
    else:
      TH1=None

    if request.POST.get('TM1')!=None and request.POST.get('TM1')!='' :  
      #value for Time spent on setting up the meeting in minutes
      inp=str(request.POST.get('TM1'))
      TM1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM1=int(request.POST.get('TM1'))
      else:
        TM1=float(request.POST.get('TM1'))
    else:
      TM1=None

    if request.POST.get('SC')!=None and request.POST.get('SC')!='' :  
      #value for Supplementary cost per meeting
      inp=str(request.POST.get('SC'))
      SCinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        SC=int(request.POST.get('SC'))
      else:
        SC=float(request.POST.get('SC'))
    else:
      SC=None

    #storing value to calculate button
    f1 = request.POST.get("f1")

    #storing value of average salary operation
    AS_op = request.POST.get('AS_op')

    

    if (TH == 0 and TM == 0) or (TH1 == 0 and TM1 == 0):
      return render(request, "meetingcostcalculator.html",{"message":"Both Hours and Minutes can't be zero"})

   
    if type(TH) == float or type(TM) == float or type(TH1) == float or type(TM1) == float:
      return render(request, "meetingcostcalculator.html",{"message":"Please enter time without decimal points"})

    AS = salaryConversion(AS, AS_op)

    
    if (AS or AS == 0) and NA and f1:
      #converting minutes into hours
      TM = TM * 0.0166667
      TM1 = TM1 * 0.0166667

      #adding the minutes that has been converted into hours to actual hours
      TH = TH + TM
      TH1 = TH1 + TM1

      #Total cost of the meeting
      cost = AS * TH * NA + TH1 * AS + SC

      #dictionary for passing all the required values to the frontend
      context = {
        "AS":ASinp,
        "AS_op":AS_op,
        "NA":NAinp,
        "TH":THinp,
        "TM":TMinp,
        "TH1":TH1inp,
        "TM1":TM1inp,
        "SC":SCinp,
        "cost":cost,
        "ycost":cost * 262,
        "f1":f1,
      }

      return render(request, "meetingcostcalculator.html", context)

    return render(request, "meetingcostcalculator.html")
  else:
    return render(request, "meetingcostcalculator.html")






def leadtimecalculator(request):
  if request.method == "POST":
    
    #storing value of Lead Time form
    given_data = request.POST.get('given_data')

    if request.POST.get('YR')!=None and request.POST.get('YR')!='' :  
      #Storing Pre-Production time value in years
      inp=str(request.POST.get('YR'))
      YRinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        YR=int(request.POST.get('YR'))
      else:
        YR=float(request.POST.get('YR'))
    else:
      YR=None

    if request.POST.get('MO')!=None and request.POST.get('MO')!='' :  
      #Storing Pre-Production time value in months
      inp=str(request.POST.get('MO'))
      MOinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        MO=int(request.POST.get('MO'))
      else:
        MO=float(request.POST.get('MO'))
    else:
      MO=None

    if request.POST.get('DY')!=None and request.POST.get('DY')!='' :  
      #Storing Pre-Production time value in days
      inp=str(request.POST.get('DY'))
      DYinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        DY=int(request.POST.get('DY'))
      else:
        DY=float(request.POST.get('DY'))
    else:
      DY=None

    if request.POST.get('TH')!=None and request.POST.get('TH')!='' :  
      #Storing Pre-Production time value in hours
      inp=str(request.POST.get('TH'))
      THinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH=int(request.POST.get('TH'))
      else:
        TH=float(request.POST.get('TH'))
    else:
      TH=None

    if request.POST.get('TM')!=None and request.POST.get('TM')!='' :  
      #Storing Pre-Production time value in minutes
      inp=str(request.POST.get('TM'))
      TMinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM=int(request.POST.get('TM'))
      else:
        TM=float(request.POST.get('TM'))
    else:
      TM=None

    if request.POST.get('YR1')!=None and request.POST.get('YR1')!='' :  
      #Storing Production time value in years
      inp=str(request.POST.get('YR1'))
      YR1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        YR1=int(request.POST.get('YR1'))
      else:
        YR1=float(request.POST.get('YR1'))
    else:
      YR1=None

    if request.POST.get('MO1')!=None and request.POST.get('MO1')!='' :  
      #Storing Production time value in months
      inp=str(request.POST.get('MO1'))
      MO1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        MO1=int(request.POST.get('MO1'))
      else:
        MO1=float(request.POST.get('MO1'))
    else:
      MO1=None

    if request.POST.get('DY1')!=None and request.POST.get('DY1')!='' :  
      #Storing Production time value in days
      inp=str(request.POST.get('DY1'))
      DY1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        DY1=int(request.POST.get('DY1'))
      else:
        DY1=float(request.POST.get('DY1'))
    else:
      DY1=None

    if request.POST.get('TH1')!=None and request.POST.get('TH1')!='' :  
      #Storing Production time value in hours
      inp=str(request.POST.get('TH1'))
      TH1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH1=int(request.POST.get('TH1'))
      else:
        TH1=float(request.POST.get('TH1'))
    else:
      TH1=None

    if request.POST.get('TM1')!=None and request.POST.get('TM1')!='' :  
      #Storing Production time value in minutes
      inp=str(request.POST.get('TM1'))
      TM1inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM1=int(request.POST.get('TM1'))
      else:
        TM1=float(request.POST.get('TM1'))
    else:
      TM1=None

    if request.POST.get('YR2')!=None and request.POST.get('YR2')!='' :  
      #Storing POST-Production time value in years
      inp=str(request.POST.get('YR2'))
      YR2inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        YR2=int(request.POST.get('YR2'))
      else:
        YR2=float(request.POST.get('YR2'))
    else:
      YR2=None

    if request.POST.get('MO2')!=None and request.POST.get('MO2')!='' :  
      #Storing POST-Production time value in months
      inp=str(request.POST.get('MO2'))
      MO2inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        MO2=int(request.POST.get('MO2'))
      else:
        MO2=float(request.POST.get('MO2'))
    else:
      MO2=None

    if request.POST.get('DY2')!=None and request.POST.get('DY2')!='' :  
      #Storing POST-Production time value in days
      inp=str(request.POST.get('DY2'))
      DY2inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        DY2=int(request.POST.get('DY2'))
      else:
        DY2=float(request.POST.get('DY2'))
    else:
      DY2=None

    if request.POST.get('TH2')!=None and request.POST.get('TH2')!='' :  
      #Storing POST-Production time value in hours
      inp=str(request.POST.get('TH2'))
      TH2inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH2=int(request.POST.get('TH2'))
      else:
        TH2=float(request.POST.get('TH2'))
    else:
      TH2=None

    if request.POST.get('TM2')!=None and request.POST.get('TM2')!='' :  
      #Storing POST-Production time value in minutes
      inp=str(request.POST.get('TM2'))
      TM2inp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM2=int(request.POST.get('TM2'))
      else:
        TM2=float(request.POST.get('TM2'))
    else:
      TM2=None

    #Storing value of Date of placing an order
    DT = request.POST.get("DT")

    #Storing value of Date of receiving an order
    DT1 = request.POST.get("DT1")

    #Storing value of calculate button
    f1 = request.POST.get('f1')

    #Making sure that only integers are provided as inputs.
    if type(YR) == float or type(MO) == float or type(DY) == float or type(TH) == float or type(TM) == float or type(YR1) == float or type(MO1) == float or type(DY1) == float or type(TH1) == float or type(TM1) == float or type(YR2) == float or type(MO2) == float or type(DY2) == float or type(TH2) == float or type(TM2) == float:
      return render(request, "leadtimecalculator.html",{"message":"Please enter time without decimal points",'given_data':given_data})

    if given_data == "form1" and f1:

      #converting inputs into minutes
      TYR = (YR + YR1 + YR2) * 525600
      TMO = (MO + MO1 + MO2) * 43800
      TDY = (DY + DY1 + DY2) * 1440
      THR = (TH + TH1 + TH2) * 60
      TMIN = (TM + TM1 + TM2)
      
      #adding all inputs that has been converted into minutes
      TL = TYR + TMO + TDY + THR + TMIN

      #creating dictionary for passing all the necessary values to the template
      context = {
        "YR":YR,
        "YR1":YR1,
        "YR2":YR2,
        "MO":MO,
        "MO1":MO1,
        "MO2":MO2,
        "DY":DY,
        "DY1":DY1,
        "DY2":DY2,
        "TH":TH,
        "TH1":TH1,
        "TH2":TH2,
        "TH":TM,
        "TM1":TM1,
        "TM2":TM2,
        "result":TL,
        "given_data":given_data,
        "f1":f1,
      }
      return render(request, "leadtimecalculator.html",context)

    if given_data == "form2" and f1:  
      
      import datetime
      #storing year, month and date in variables
      year, month, date = (int(i) for i in DT.split("T")[0].split("-"))
      year1, month1, date1 = (int(i) for i in DT1.split("T")[0].split("-"))
      #storing hour and minutes in variables
      hr, mn = (int(i) for i in DT.split("T")[1].split(":"))
      hr1, mn1 = (int(i) for i in DT1.split("T")[1].split(":"))
      #storing date given by user into variables
      my_date = datetime.datetime(year = year,month = month,day = date,hour = hr,minute = mn)
      my_date1 = datetime.datetime(year = year1, month = month1,day = date1,hour = hr1,minute = mn1)
      #adding date with the Total Drive Time and storing its value in variable
      Tmy_date = my_date1 - my_date
      
      #creating dictionary for passing all the necessary values to the template
      context = {
        "DT":DT,
        "DT1":DT1,
        "result":Tmy_date,
        "given_data":given_data,
        "f1":f1
      }

      return render(request,  "leadtimecalculator.html",context)

    if given_data == "form3" and f1:

      #converting all inputs into minutes
      TYR = (YR + YR1) * 525600
      TMO = (MO + MO1) * 43800
      TDY = (DY + DY1) * 1440
      THR = (TH + TH1) * 60
      TMIN = (TM + TM1)

      #adding all inputs that has been converted into minutes
      TL = TYR + TMO + TDY + THR + TMIN
      

      #creating dictionary for passing all the necessary values to the template
      context = {
        "YR":YR,
        "YR1":YR1,
        "MO":MO,
        "MO1":MO1,
        "DY":DY,
        "DY1":DY1,
        "TH":TH,
        "TH1":TH1,
        "TM":TM,
        "TM1":TM1,
        "result":TL,
        "given_data":given_data,
        "f1":f1,
      }
      
      return render(request, "leadtimecalculator.html",context)
      
    return render(request, "leadtimecalculator.html",{'given_data':given_data})
  else:
    return render(request, "leadtimecalculator.html",{'given_data':"form1"}) 






def hairgrowthcalculator(request):
  if request.method == "POST":
    
    #storing value of Growth time in variable
    if request.POST.get('GT')!=None and request.POST.get('GT')!='' :  
      #Storing POST-Production time value in minutes
      inp=str(request.POST.get('GT'))
      GTinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        GT=int(request.POST.get('GT'))
      else:
        GT=float(request.POST.get('GT'))
    else:
      GT=None

    #storing value of Growth time operation
    GT_op = request.POST.get('GT_op')

    #storing value of calculate button
    f1 = request.POST.get('f1')

    if (GT or GT == 0) and GT_op == "Day" and f1:
      result = GT * 0.41725
      #dictionary to pass all the required values to the template
      context = {
      "GT":GTinp,
      "GT_op":GT_op,
      "result":result,
      "f1":f1,
      }
      return render(request, "hairgrowthcalculator.html", context)

    elif (GT or GT == 0) and GT_op == "Week" and f1:
      result = GT * 2.921
      #dictionary to pass all the required values to the template
      context = {
      "GT":GTinp,
      "GT_op":GT_op,
      "result":result,
      "f1":f1,
      }
      return render(request, "hairgrowthcalculator.html", context)

    elif (GT or GT == 0) and GT_op == "Month" and f1:
      result = GT * 12.7
      #dictionary to pass all the required values to the template
      context = {
      "GT":GTinp,
      "GT_op":GT_op,
      "result":result,
      "f1":f1,
      }
      return render(request, "hairgrowthcalculator.html", context)

    elif (GT or GT == 0) and GT_op == "Year" and f1:
      result = GT * 152.4
      #dictionary to pass all the required values to the template
      context = {
      "GT":GTinp,
      "GT_op":GT_op,
      "result":result,
      "f1":f1,
      }
      return render(request, "hairgrowthcalculator.html", context)

    return render(request, "hairgrowthcalculator.html")
  else:
    return render(request, "hairgrowthcalculator.html")





def showercostcalculator(request):
  if request.method == "POST":
  

    def conversionToLiter(value, unit): 
      """"converts vaule into liters"""
      if unit == "gallon(us)": return value * 3.78541
      elif unit == "gallon(uk)": return value * 4.54609
      else: return value

    def conversionToMoney(value, unit):
      """converts value into money"""
      if unit == "cubicmeter": return value / 1000
      elif unit == "gallon(us)": return value / 3.78
      elif unit == "gallon(uk)": return value / 4.54
      else: return value

    if request.POST.get('PH')!=None and request.POST.get('PH')!='' :  
      #Storing value for People in household
      inp=str(request.POST.get('PH'))
      PHinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        PH=int(request.POST.get('PH'))
      else:
        PH=float(request.POST.get('PH'))
    else:
      PH=None

    if request.POST.get('TH')!=None and request.POST.get('TH')!='' :  
      #Storing Average shower duration time value in hours
      inp=str(request.POST.get('TH'))
      THinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH=int(request.POST.get('TH'))
      else:
        TH=float(request.POST.get('TH'))
    else:
      TH=None

    if request.POST.get('TM')!=None and request.POST.get('TM')!='' :  
      #Storing Average shower duration time value in minutes
      inp=str(request.POST.get('TM'))
      TMinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM=int(request.POST.get('TM'))
      else:
        TM=float(request.POST.get('TM'))
    else:
      TM=None

    if request.POST.get('SP')!=None and request.POST.get('SP')!='' :  
      #Storing value for shower per person
      inp=str(request.POST.get('SP'))
      SPinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        SP=int(request.POST.get('SP'))
      else:
        SP=float(request.POST.get('SP'))
    else:
      SP=None

    if request.POST.get('WP')!=None and request.POST.get('WP')!='' :  
      #Storing value for water price
      inp=str(request.POST.get('WP'))
      WPinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        WP=int(request.POST.get('WP'))
      else:
        WP=float(request.POST.get('WP'))
    else:
      WP=None

    if request.POST.get('EP')!=None and request.POST.get('EP')!='' :  
      #Storing value for energy price
      inp=str(request.POST.get('EP'))
      EPinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        EP=int(request.POST.get('EP'))
      else:
        EP=float(request.POST.get('EP'))
    else:
      EP=None

    if request.POST.get('SFR')!=None and request.POST.get('SFR')!='' :  
      #Storing value for shower flow rate per minute
      inp=str(request.POST.get('SFR'))
      SFRinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        SFR=int(request.POST.get('SFR'))
      else:
        SFR=float(request.POST.get('SFR'))
    else:
      SFR=None

    WP_op = request.POST.get("WP_op")

    SFR_op = request.POST.get("SFR_op")

    f1 = request.POST.get("f1")

    #converting Average Shower Duration in minutes
    ASD = TH * 60 + TM

    WP = conversionToMoney(WP, WP_op)
    SFR = conversionToLiter(SFR, SFR_op)

    if (PH == 0) or (TH == 0 and TM == 0) or (SP == 0) or (WP == 0) or (EP == 0) or (SFR == 0):
      return render(request, "showercostcalculator.html",{"message":"Input values must be greater than 0."})


    if PH and SP and f1:
      #calculating Total water used value and storing it in TWU variable
      TWU = PH * SP * ASD * SFR
      #calculating Total shower cost value and storing it in TSC variable
      TSC = WP * TWU + ((TWU / SFR) * EP * 0.24)
      #calculating Single shower cost value and storing it in SSC variable
      SSC = TSC / (PH * SP)

      #dictionary to pass all the required data to the template
      context = {
        "PH":PHinp,
        "TH":THinp,
        "TM":TMinp,
        "SP":SPinp,
        "WP":WPinp,
        "EP":EPinp,
        "SFR":SFRinp,
        "WP_op":WP_op,
        "SFR_op":SFR_op,
        "TWU":TWU,
        "TSC":TSC,
        "SSC":SSC,
        "f1":f1,
      }
      return render(request, "showercostcalculator.html", context)

    
    return render(request, "showercostcalculator.html")
  else:
    return render(request, "showercostcalculator.html")

  





def sunscreencalculator(request):
  if request.method == "POST":
    
    if request.POST.get('W')!=None and request.POST.get('W')!='' :  
      #Storing value of Weight
      inp=str(request.POST.get('W'))
      Winp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        W=int(request.POST.get('W'))
      else:
        W=float(request.POST.get('W'))
    else:
      W=None

    if request.POST.get('H')!=None and request.POST.get('H')!='' :  
      #Storing value of Height
      inp=str(request.POST.get('H'))
      Hinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        H=int(request.POST.get('H'))
      else:
        H=float(request.POST.get('H'))
    else:
      H=None

    #value of weight unit
    W_op = request.POST.get("W_op")

    #value of height unit
    H_op = request.POST.get("H_op")

    #value of upper body clothes
    upr = request.POST.get("upr")

    #value of lower body clothes
    lwr = request.POST.get("lwr")

    #value of calculate button
    f1 = request.POST.get("f1")

    #if weight is in pounds, it converts the weight into kgs
    if W_op == "lb":
      W = W * 0.453592

    #converting height into centimeters
    if H_op == "mtr":
      H = H * 100
    elif H_op == "in":
      H = H * 2.54
    elif H_op == "ft":
      H = H * 30.48

    #Total Body area in cm2
    BA = (71.84 * (H**0.725) * (W**0.425) )

    #converting Body area by keeping in mind "2 mg/cm2" into ml.
    TBA = ((2 * BA) * 0.001)

    
    if upr == "Longsleeve":
      TBA = ((TBA * 47.19387390243167) * 0.01)
    elif upr == "Sleeveless":
      TBA = ((TBA  *64.355282594225) * 0.01)
    elif upr == "T-Shirt":
      TBA = ((TBA * 55.774578248328346) * 0.01)

    if lwr == "Shorts":
      TBA = ((TBA * 92.24257171838917) * 0.01)
    elif lwr == "Long":
      TBA = ((TBA * 64.355282594225) * 0.01)
    elif lwr == "Midi":
      TBA = ((TBA * 83.66186737249251) * 0.01)

    if (TBA or TBA == 0) and f1:
      #Dicionary to pass all the required values to the template
      context = {
        "W": Winp,
        "H": Hinp,
        "W_op": W_op,
        "H_op": H_op,
        "upr": upr,
        "lwr": lwr,
        "f1": f1,
        "TBA": TBA, #value of total sunscreen used
        "TS": TBA / 5, #value of teaspoons
      }
      
      return render(request, "sunscreencalculator.html", context)


    return render(request, "sunscreencalculator.html")
  else:
    return render(request, "sunscreencalculator.html")







def bathvsshowercalculator(request):
  if request.method == "POST":
    

    if request.POST.get('TH')!=None and request.POST.get('TH')!='' :  
      #Storing value of avg shower duration in hours
      inp=str(request.POST.get('TH'))
      THinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TH=int(request.POST.get('TH'))
      else:
        TH=float(request.POST.get('TH'))
    else:
      TH=None

    if request.POST.get('TM')!=None and request.POST.get('TM')!='' :  
      #Storing value of average shower duration in minutes
      inp=str(request.POST.get('TM'))
      TMinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TM=int(request.POST.get('TM'))
      else:
        TM=float(request.POST.get('TM'))
    else:
      TM=None

    if request.POST.get('SF')!=None and request.POST.get('SF')!='' :  
      #Storing value of Shower frequency per day
      inp=str(request.POST.get('SF'))
      SFinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        SF=int(request.POST.get('SF'))
      else:
        SF=float(request.POST.get('SF'))
    else:
      SF=None

    if request.POST.get('SFR')!=None and request.POST.get('SFR')!='' :  
      #Storing value of shower flow rate per minute
      inp=str(request.POST.get('SFR'))
      SFRinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        SFR=int(request.POST.get('SFR'))
      else:
        SFR=float(request.POST.get('SFR'))
    else:
      SFR=None

    if request.POST.get('BF')!=None and request.POST.get('BF')!='' :  
      #Storing value of bath frequency
      inp=str(request.POST.get('BF'))
      BFinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        BF=int(request.POST.get('BF'))
      else:
        BF=float(request.POST.get('BF'))
    else:
      BF=None

    if request.POST.get('W')!=None and request.POST.get('W')!='' :  
      #Storing value of Weight
      inp=str(request.POST.get('W'))
      Winp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        W=int(request.POST.get('W'))
      else:
        W=float(request.POST.get('W'))
    else:
      W=None

    SFR_op = request.POST.get("SFR_op")
    BTSinp = request.POST.get("BTS")
    likeinp = request.POST.get("like")
    BTS = float(request.POST.get("BTS"))
    like = float(request.POST.get("like"))
    W_op = request.POST.get("W_op")
    Iget = request.POST.get("Iget")
    f1 = request.POST.get("f1")
    

    if (TH == 0 and TM == 0):
      return render(request, "bathvsshowercalculator.html",{"message":"Both hours and minutes can't be 0."})
    
    if W < 34 and W_op == "lb":
      return render(request, "bathvsshowercalculator.html", {"message":"Weight should be more than 34 lbs"})
    elif W_op == "lb":
      W = W * 0.453592
    
    
    if SFR_op == "gallon(us)":
      SFR = SFR * 3.78541
    elif SFR_op == "gallon(uk)" :
      SFR = SFR * 4.54609
    

    if Iget == "after":
      W = 0


    if f1:
      ShowerWU = (TH * 60 + TM) * SFR * SF

      BathWU = max(0,((BTS * like) - W) *  BF)

      context = {
        "f1":f1,
        'TH':THinp,
        "TM":TMinp,
        "SF":SFinp,
        "SFR":SFRinp,
        "SFR_op":SFR_op,
        "BTS":BTSinp,
        "like":likeinp,
        "Iget":Iget,
        "BF":BF,
        "W_op":W_op,
        "W":Winp,
        "ShowerWU":ShowerWU,
        "GShowerWU": ShowerWU * 0.264172,
        "BathWU":BathWU,
        "GBathWU":BathWU * 0.264172,

      }
      
      return render(request, "bathvsshowercalculator.html", context)

    return render(request, "bathvsshowercalculator.html")
  else:
    return render(request, "bathvsshowercalculator.html")





def jeanssizecalculator(request):
  if request.method == "POST":
    

    if request.POST.get('W')!=None and request.POST.get('W')!='' :  
      #Storing value of Weight
      inp=str(request.POST.get('W'))
      Winp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        W=int(request.POST.get('W'))
      else:
        W=float(request.POST.get('W'))
    else:
      W=None

    if request.POST.get('L')!=None and request.POST.get('L')!='' :  
      #Storing value of Length
      inp=str(request.POST.get('L'))
      Linp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        L=int(request.POST.get('L'))
      else:
        L=float(request.POST.get('L'))
    else:
      L=None

    #storing value of "I am measuring" input from frontend
    given_data = request.POST.get("given_data")

    #storing value of Sex
    Sex = request.POST.get("Sex")

    #storing value of width or waist unit
    W_op = request.POST.get("W_op")

    #storing value of lenght unit
    L_op = request.POST.get("L_op")

    #storing value of calculate button
    f1 = request.POST.get("f1")

    #converting width or waist in inches if it's in cms
    if W_op == "cm" and W !=None:
      W = W * 0.393701

    #converting width or waist in inches if it's in cms
    if L_op == "cm" and L !=None:
      L = L * 0.393701
    

    
    #applying validation on width or waist
    if W !=None and W <= 7.5:
      return render(request, "jeanssizecalculator.html",{"message":"Waist or Width must be greater than 7.5 inches (20 cm).","given_data":given_data,"Sex":Sex})

    #applying validation on Length
    if L !=None and L <= 15:
      return render(request, "jeanssizecalculator.html",{"message":"Length must be greater than 15 inches (40 cm).","given_data":given_data,"Sex":Sex})

    if given_data == "form2" and W !=None:
      W = W * 2

    if (given_data == "form1" or given_data == "form2") and Sex == "Male" and f1 and W !=None and L !=None:
      try:
        if W <= 28 and L <=30:
          India = "28"
          US = "28/30, 30, or XS"
          European = "40"
          UK = "30"
        elif W <= 29 and L <=30:
          India = "30"
          US = "29/30, 32, or XS"
          European = "42"
          UK = "32"
        elif (W > 29 and W <= 30) and L <=32:
          India = "30"
          US = "30/32, 34, or S"
          European = "44"
          UK = "34"
        elif (W > 30 and W <= 32) and L <=32:
          India = "32"
          US = "32/32, 36, or S"
          European = "46"
          UK = "36"
        elif (W > 32 and W <= 33) and L <=32:
          India = "34"
          US = "33/32, 38, or M"
          European = "48"
          UK = "38"
        elif (W > 33 and W <= 34) and L <=32:
          India = "34"
          US = "34/32, 40, or M"
          European = "50"
          UK = "40"
        elif (W > 34 and W <= 36) and L <=34:
          India = "36"
          US = "36/34, 42, or L"
          European = "52"
          UK = "42"
        elif (W > 36 and W <= 38) and L <=34:
          India = "38"
          US = "38/34, 44, or L"
          European = "54"
          UK = "44"
        elif (W > 38 and W <= 40) and L <=34:
          India = "40"
          US = "40/34, 46, or XL"
          European = "56"
          UK = "46"
        elif (W > 40 and W <= 42) and L <=34:
          India = "42"
          US = "42/34, 48, or XL"
          European = "58"
          UK = "48"
        elif (W > 42 and W <= 44) and L <=34:
          India = "44"
          US = "44/34, 50, or XXL"
          European = "60"
          UK = "50"
        
        
        context = {
          "given_data":given_data,
          "f1":f1,
          "W":Winp,
          "L":Linp,
          "Sex":Sex,
          "W_op":W_op,
          "L_op":L_op,
          "India":India,
          "US":US,
          "European":European,
          "UK":UK,
        }
        
        return render(request, "jeanssizecalculator.html", context)
      except:
        context = {
        "given_data":given_data,
        "f1":f1,
        "W":Winp,
        "L":Linp,
        "Sex":Sex,
        "W_op":W_op,
        "L_op":L_op,
        "er":"Ooops, we're sorry, but we couldn't find a specific size for you. It seems that you have a very unique body shape - you'll have to try them on yourself!",
        }
        
        return render(request, "jeanssizecalculator.html", context)


    

    

    if (given_data == "form1" or given_data == "form2") and Sex == "Female" and f1 and W !=None and L !=None:
      try:
        if W <= 25 and L <=32:
          India = "26"
          US = "25/32, 0, or XXS"
          European = "32"
          UK = "4"
        elif W <= 26 and L <=32:
          India = "36"
          US = "26/32, 2, or XS"
          European = "34"
          UK = "6"
        elif W <= 27 and L <=32:
          India = "28"
          US = "27/32, 4, or XS"
          European = "36"
          UK = "8"
        elif W <= 28 and L <=32:
          India = "28"
          US = "28/32, 6, or S"
          European = "38"
          UK = "10"
        elif W <= 29 and L <=32:
          India = "30"
          US = "29/32, 8, or S"
          European = "40"
          UK = "12"
        elif W <= 30 and L <=32:
          India = "30"
          US = "30/32, 10, or M"
          European = "42"
          UK = "14"
        elif W <= 31 and L <=32:
          India = "32"
          US = "31/32, 12, or M"
          European = "44"
          UK = "16"
        elif W <= 32 and L <=32:
          India = "32"
          US = "32/32, 14, or L"
          European = "46"
          UK = "18"
        elif W <= 33 and L <=32:
          India = "34"
          US = "33/32, 16, or L"
          European = "48"
          UK = "20"
        elif W <= 34 and L <=32:
          India = "34"
          US = "34/32, 18, or XL"
          European = "50"
          UK = "22"
        elif W <= 35 and L <=32:
          India = "36"
          US = "35/32, 20, or XL"
          European = "52"
          UK = "24"
        elif W <= 36 and L <=32:
          India = "36"
          US = "36/32, 22, or XXL"
          European = "54"
          UK = "26"
        elif W <= 37 and L <=32:
          India = "38"
          US = "37/32, 24, or XXL"
          European = "56"
          UK = "28"
        elif W <= 38 and L <=32:
          India = "38"
          US = "38/32, 26, or XXXL"
          European = "58"
          UK = "30"
        elif W <= 39 and L <=32:
          India = "40"
          US = "39/32, 28, or XXXL"
          European = "60"
          UK = "32"

        context = {
        "given_data":given_data,
        "f1":f1,
        "W":Winp,
        "L":Linp,
        "Sex":Sex,
        "W_op":W_op,
        "L_op":L_op,
        "India":India,
        "US":US,
        "European":European,
        "UK":UK,
        }
        
        return render(request, "jeanssizecalculator.html", context)
        
      except:
        context = {
        "given_data":given_data,
        "f1":f1,
        "W":Winp,
        "L":Linp,
        "Sex":Sex,
        "W_op":W_op,
        "L_op":L_op,
        "er":"Ooops, we're sorry, but we couldn't find a specific size for you. It seems that you have a very unique body shape - you'll have to try them on yourself!",
        }
        
        return render(request, "jeanssizecalculator.html", context)

      
    if (given_data == "form1" or given_data == "form2") and f1 and W !=None and L !=None:
      
      return render(request, "jeanssizecalculator.html",{"er":"Ooops, we're sorry, but we couldn't find a specific size for you. It seems that you have a very unique body shape - you'll have to try them on yourself!","given_data":given_data,"Sex":Sex})

    
    return render(request, "jeanssizecalculator.html",{"given_data":given_data,"Sex":Sex})
  else:
    return render(request, "jeanssizecalculator.html", {"given_data":"form1"})




def lostsockscalculator(request):
  if request.method == "POST":
    

    if request.POST.get('PH')!=None and request.POST.get('PH')!='' :  
      #Storing value of People in Household
      inp=str(request.POST.get('PH'))
      PHinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        PH=int(request.POST.get('PH'))
      else:
        PH=float(request.POST.get('PH'))
    else:
      PH=None

    if request.POST.get('PT')!=None and request.POST.get('PT')!='' :  
      #Storing value of Precautions taken
      inp=str(request.POST.get('PT'))
      PTinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        PT=int(request.POST.get('PT'))
      else:
        PT=float(request.POST.get('PT'))
    else:
      PT=None

    if request.POST.get('TW')!=None and request.POST.get('TW')!='' :  
      #Storing value of Types of washes per week
      inp=str(request.POST.get('TW'))
      TWinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TW=int(request.POST.get('TW'))
      else:
        TW=float(request.POST.get('TW'))
    else:
      TW=None

    if request.POST.get('NW')!=None and request.POST.get('NW')!='' :  
      #Storing value of Number of washes
      inp=str(request.POST.get('NW'))
      NWinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        NW=int(request.POST.get('NW'))
      else:
        NW=float(request.POST.get('NW'))
    else:
      NW=None

    if request.POST.get('TS')!=None and request.POST.get('TS')!='' :  
      #Storing value of Total socks washed
      inp=str(request.POST.get('TS'))
      TSinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TS=int(request.POST.get('TS'))
      else:
        TS=float(request.POST.get('TS'))
    else:
      TS=None

    def conversionToWeek(days, unit):
      """converts the days into weeks"""
      if unit == "day": return days * 7
      elif unit == "month": return days * 0.2299795
      elif unit == "year": return days * 0.01916496
      else: return days

    #storing value of Number of washes unit
    NW_op = request.POST.get("NW_op")

    #storing value of Attitude towards doing laundry
    AT = request.POST.get("AT")

    #storing value of Total Socks washed unit
    TS_op = request.POST.get("TS_op")

    #storing value of calculate button
    f1 = request.POST.get("f1")

    
    NW = conversionToWeek(NW, NW_op)
    TS = conversionToWeek(TS, TS_op)
    

    
    #Runs if calculate button is pressed
    if f1:
      lost = max(0, 0.38 + ((0.005 * PH*NW) + (0.0012 * TW * TS)) - (0.0159 * PT * int(AT)))

      #dictionary to pass all the required values to the template
      context = {
        "PH":PHinp,
        "PT":PTinp,
        "TW":TWinp,
        "NW":NWinp,
        "NW_op":NW_op,
        "AT":AT,
        "TS":TSinp,
        "TS_op":TS_op,
        "f1":f1,
        "lost":lost, #passing the value of Socks lost
        "Chance":lost * 100, #passing the value of Chance of losing a sock per week
      }
      return render(request, "lostsockscalculator.html", context)


    return render(request, "lostsockscalculator.html")
  else:
    return render(request, "lostsockscalculator.html")






def pleatedskirtcalculator(request):
  if request.method == "POST":


    if request.POST.get('WA')!=None and request.POST.get('WA')!='' :  
      #Storing value of Waist
      inp=str(request.POST.get('WA'))
      WAinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        WA=int(request.POST.get('WA'))
      else:
        WA=float(request.POST.get('WA'))
    else:
      WA=None

    if request.POST.get('SA')!=None and request.POST.get('SA')!='' :  
      #Storing value of Seam allowance
      inp=str(request.POST.get('SA'))
      SAinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        SA=int(request.POST.get('SA'))
      else:
        SA=float(request.POST.get('SA'))
    else:
      SA=None

    if request.POST.get('L')!=None and request.POST.get('L')!='' :  
      #Storing value of Desired skirt length
      inp=str(request.POST.get('L'))
      Linp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        L=int(request.POST.get('L'))
      else:
        L=float(request.POST.get('L'))
    else:
      L=None

    if request.POST.get('N')!=None and request.POST.get('N')!='' :  
      #Storing value of Number of pleats
      inp=str(request.POST.get('N'))
      Ninp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        N=int(request.POST.get('N'))
      else:
        N=float(request.POST.get('N'))
    else:
      N=None

    if request.POST.get('WT')!=None and request.POST.get('WT')!='' :  
      #Storing value of Waistband thickness
      inp=str(request.POST.get('WT'))
      WTinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        WT=int(request.POST.get('WT'))
      else:
        WT=float(request.POST.get('WT'))
    else:
      WT=None

    def conversionToCm(value, unit):
      if unit == "mtr": return value * 100
      elif unit == "inch": return value * 2.54
      else: return value


    WA_op = request.POST.get("WA_op")
    SA_op = request.POST.get("SA_op")
    PT = request.POST.get("PT")
    L_op = request.POST.get("L_op")
    WT_op = request.POST.get("WT_op")
    f1 = request.POST.get("f1")

    WA = conversionToCm(WA, WA_op)
    SA = conversionToCm(SA, SA_op)
    L = conversionToCm(L, L_op)
    WT = conversionToCm(WT, WT_op)

    if PT == "Knife" and WA !=None and SA !=None and N !=None and f1:
      neededFabricWidth = (WA * 2) + SA
      pleatWidth = (WA / N) * 2
      

    if PT == "Box" and WA !=None and SA !=None and N !=None and f1:
      neededFabricWidth = (WA * 3) + SA
      pleatWidth = (WA / N) * 3
      
    neededFabricLength = SA * 2 + L
    neededFabricWid = WA + (SA * 3)
    neededfabricLen = WT * 2 + SA * 2
    
    
    try:
      context = {
        "WA":WAinp,
        "WA_op":WA_op,
        "SA":SAinp,
        "SA_op":SA_op,
        "PT":PT,
        "L":Linp,
        "L_op":L_op,
        "N":Ninp,
        "WT":WTinp,
        "WT_op":WT_op,
        "f1":f1,
        "neededFabricWidth":neededFabricWidth,
        "pleatWidth":pleatWidth,
        "neededFabricLength":neededFabricLength,
        "neededFabricWid":neededFabricWid,
        "neededfabricLen":neededfabricLen,
      }
      return render(request, "pleatedskirtcalculator.html", context)
    except:
      return render(request, "pleatedskirtcalculator.html",{"message":"Something is missing."})

  else:
    return render(request, "pleatedskirtcalculator.html")






def quiltbindingcalculator(request):
  if request.method == "POST":
    

    if request.POST.get('W')!=None and request.POST.get('W')!='' :  
      #Storing value of Quild Width
      inp=str(request.POST.get('W'))
      Winp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        W=int(request.POST.get('W'))
      else:
        W=float(request.POST.get('W'))
    else:
      W=None

    if request.POST.get('L')!=None and request.POST.get('L')!='' :  
      #Storing value of Quilt Length
      inp=str(request.POST.get('L'))
      Linp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        L=int(request.POST.get('L'))
      else:
        L=float(request.POST.get('L'))
    else:
      L=None

    if request.POST.get('BW')!=None and request.POST.get('BW')!='' :  
      #Storing value of Binding Widtho of Straps
      inp=str(request.POST.get('BW'))
      BWinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        BW=int(request.POST.get('BW'))
      else:
        BW=float(request.POST.get('BW'))
    else:
      BW=None

    if request.POST.get('F')!=None and request.POST.get('F')!='' :  
      #Storing value of Binding Width of Fabric
      inp=str(request.POST.get('F'))
      Finp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        F=int(request.POST.get('F'))
      else:
        F=float(request.POST.get('F'))
    else:
      F=None

    

    W_op = request.POST.get("W_op")
    L_op = request.POST.get("L_op")
    BW_op = request.POST.get("BW_op")
    F_op = request.POST.get("F_op")
    f1 = request.POST.get("f1")

    def conversionToCm(value, unit):
      if unit == "mtr": return value * 100
      elif unit == "inch": return value * 2.54
      else: return value

    W = conversionToCm(W, W_op)
    L = conversionToCm(L, L_op)
    BW = conversionToCm(BW, BW_op)
    F = conversionToCm(F, F_op)

    if W != None and L != None and BW != None and F != None and f1:
      lenOfBinding = (2 * W) + (2 * L) + 25.4
      strips = lenOfBinding / F
      pieceofFabric = strips * BW 
      bi = lenOfBinding * BW
      biArea = bi / F

      context = {
        "W": Winp,
        "L": Linp,
        "BW": BWinp,
        "F": Finp,
        "W_op":W_op,
        "L_op":L_op,
        "BW_op":BW_op,
        "F_op":F_op,
        "J": F,
        "f1":f1,
        "lenOfBinding": lenOfBinding,
        "strips": strips,
        "pieceofFabric": pieceofFabric,
        "pieceofFabricInInches": pieceofFabric * 0.393701,
        "bi": bi,
        "biInches": bi * 0.155,
        "biArea": biArea,
        "FInch": F * 0.393701,
        "biAreaInch": biArea * 0.393701,
      }
      return render(request, "quiltbindingcalculator.html", context)

    
    return render(request, "quiltbindingcalculator.html")
  else:
    return render(request, "quiltbindingcalculator.html")





def quiltcalculator(request):
  if request.method == "POST":
    

    if request.POST.get('W')!=None and request.POST.get('W')!='' :  
      #Storing value of Width
      inp=str(request.POST.get('W'))
      Winp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        W=int(request.POST.get('W'))
      else:
        W=float(request.POST.get('W'))
    else:
      W=None

    if request.POST.get('L')!=None and request.POST.get('L')!='' :  
      #Storing value of Length
      inp=str(request.POST.get('L'))
      Linp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        L=int(request.POST.get('L'))
      else:
        L=float(request.POST.get('L'))
    else:
      L=None

    if request.POST.get('BW')!=None and request.POST.get('BW')!='' :  
      #Storing value of Bolt Width
      inp=str(request.POST.get('BW'))
      BWinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        BW=int(request.POST.get('BW'))
      else:
        BW=float(request.POST.get('BW'))
    else:
      BW=None

    if request.POST.get('A')!=None and request.POST.get('A')!='' :  
      #Storing value of Additional Coverage
      inp=str(request.POST.get('A'))
      Ainp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        A=int(request.POST.get('A'))
      else:
        A=float(request.POST.get('A'))
    else:
      A=None

    W_op = request.POST.get("W_op")
    L_op = request.POST.get("L_op")
    BW_op = request.POST.get("BW_op")
    A_op = request.POST.get("A_op")
    f1 = request.POST.get("f1")

    def conversionToInches(value, unit):
      if unit == "mtr": return value * 39.3701
      elif unit == "cm": return value * 0.393701
      else: return value

    W = conversionToInches(W, W_op)
    L = conversionToInches(L, L_op)
    BW = conversionToInches(BW, BW_op)
    A = conversionToInches(A, A_op)

    if W > L:
      context = {
      "L":Linp,
      "W":Winp,
      "BW":BWinp,
      "A":Ainp,
      "W_op":W_op,
      "L_op":L_op,
      "BW_op":BW_op,
      "A_op":A_op,
      
      "message":"Width should be the shorter edge of the quilt top, and length - the longer."
      }
      return render(request, "quiltcalculator.html",context)

    if BW <= 8:
      context = {
      "L":Linp,
      "W":Winp,
      "BW":BWinp,
      "A":Ainp,
      "W_op":W_op,
      "L_op":L_op,
      "BW_op":BW_op,
      "A_op":A_op,
      
      "message":"Sorry! The width of the bolt of fabric must be longer than 8 inches (20.4 cm)."
      }
      return render(request, "quiltcalculator.html",context)

    if L != None and W != None and BW != None and A != None and f1:
      L = (L + 8) + (2 * A)
      W = (W + 8) + (2 * A)
      

    if W > BW * 5 and f1:
      
      
      context = {
      "L":Linp,
      "W":Winp,
      "BW":BWinp,
      "A":Ainp,
      "W_op":W_op,
      "L_op":L_op,
      "BW_op":BW_op,
      "A_op":A_op,
      
      "message":"You will need more than 5 pieces of fabric. We recommend that you buy a bigger bolt of fabric."
      }
      return render(request, "quiltcalculator.html",context)

    #for backing and directional
    if W > BW:
      for i in range(1,6):
        if BW * i >= W:
          pieces = i
          
          break
    elif W <= BW: 
      pieces = 1
      

    neededFabric = L * pieces * 0.0254
    neededWidth = W / pieces
    

    try:
      context = {
        "L":Linp,
        "W":Winp,
        "BW":BWinp,
        "A":Ainp,
        "W_op":W_op,
        "L_op":L_op,
        "BW_op":BW_op,
        "A_op":A_op,
        "f1":f1,
        "pieces":pieces,
        "neededFabric":neededFabric,
        "resultL":L,
        "CMresultL":L * 2.54,
        "yard":neededFabric * 1.094,
        "neededWidth":neededWidth,
        "CMneededWidth":neededWidth * 2.54,
        "NonneededFabric":W * pieces * 0.0254,
        "Nonyard":W * pieces * 0.0254 * 1.094,
        "Nonwidth":L / pieces,
        "CMNonwidth":(L / pieces) * 2.54,
        "NoW":W,
        "CMW": W * 2.54,
      }
      
      return render(request, "quiltcalculator.html",context)
    except:
      return render(request, "quiltcalculator.html")
    
  else:
    return render(request, "quiltcalculator.html")





def cashbackorlowinterestcalculator(request):
  if request.method == "POST":
    print(request.POST)

    if request.POST.get('CA')!=None and request.POST.get('CA')!='' :  
      #Storing value of Cash Back Amount
      inp=str(request.POST.get('CA'))
      CAinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        CA=int(request.POST.get('CA'))
      else:
        CA=float(request.POST.get('CA'))
    else:
      CA=None

    if request.POST.get('IRH')!=None and request.POST.get('IRH')!='' :  
      #Storing value of Interest Rate High
      inp=str(request.POST.get('IRH'))
      IRHinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        IRH=int(request.POST.get('IRH'))
      else:
        IRH=float(request.POST.get('IRH'))
    else:
      IRH=None

    if request.POST.get('IRL')!=None and request.POST.get('IRL')!='' :  
      #Storing value of Interest Rate Low
      inp=str(request.POST.get('IRL'))
      IRLinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        IRL=int(request.POST.get('IRL'))
      else:
        IRL=float(request.POST.get('IRL'))
    else:
      IRL=None

    if request.POST.get('AP')!=None and request.POST.get('AP')!='' :  
      #Storing value of Auto Price
      inp=str(request.POST.get('AP'))
      APinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        AP=int(request.POST.get('AP'))
      else:
        AP=float(request.POST.get('AP'))
    else:
      AP=None

    if request.POST.get('LT')!=None and request.POST.get('LT')!='' :  
      #Storing value of Loan Term
      inp=str(request.POST.get('LT'))
      LTinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        LT=int(request.POST.get('LT'))
      else:
        LT=float(request.POST.get('LT'))
    else:
      LT=None

    if request.POST.get('DP')!=None and request.POST.get('DP')!='' :  
      #Storing value of Down Payment
      inp=str(request.POST.get('DP'))
      DPinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        DP=int(request.POST.get('DP'))
      else:
        DP=float(request.POST.get('DP'))
    else:
      DP=None

    if request.POST.get('TV')!=None and request.POST.get('TV')!='' :  
      #Storing value of Trade-in Value
      inp=str(request.POST.get('TV'))
      TVinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        TV=int(request.POST.get('TV'))
      else:
        TV=float(request.POST.get('TV'))
    else:
      TV=None

    if request.POST.get('ST')!=None and request.POST.get('ST')!='' :  
      #Storing value of Sales Tax
      inp=str(request.POST.get('ST'))
      STinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        ST=int(request.POST.get('ST'))
      else:
        ST=float(request.POST.get('ST'))
    else:
      ST=None

    if request.POST.get('OF')!=None and request.POST.get('OF')!='' :  
      #Storing value of Other Fees
      inp=str(request.POST.get('OF'))
      OFinp=inp #storing input as string so that the initial zeros in input can be preserved
      if inp.isdigit():
        OF=int(request.POST.get('OF'))
      else:
        OF=float(request.POST.get('OF'))
    else:
      OF=None

    IAF = request.POST.get("IAF")
    f1 = request.POST.get("f1")

    if IRH <= IRL and f1:
      context = {
        "CA":CAinp,
        "IRH":IRHinp,
        "IRL":IRLinp,
        "AP":APinp,
        "LT":LTinp,
        "DP":DPinp,
        "TV":TVinp,
        "ST":STinp,
        "OF":OFinp,
        "IAF":IAF,
        # "f1":f1,
        "message":"Since the interest rate with cash back offer is not lower. So it is always good to take the cash back offer."
      }
      return render(request, "cashbackorlowinterestcalculator.html", context)
    try:
      SaleTax = ((AP - TV) * ST)/100
      print(SaleTax)

      if IAF == "Yes" and f1:
        TotalLoanAmount = AP - DP - TV + SaleTax + OF
        CBTotalLoanAmount = AP - DP - TV + SaleTax + OF - CA
        UpfrontPayment = DP
        MonthlyPay = TotalLoanAmount * (IRL/1200) * (((IRL/1200)+1)**LT)/((((IRL/1200)+1)**LT)-1)
        CBMonthlyPay = CBTotalLoanAmount * (IRH/1200) *(((IRH/1200)+1)**LT)/((((IRH/1200)+1)**LT)-1)
        TotalPayments = MonthlyPay * LT
        CBTotalPayments = CBMonthlyPay * LT
        TotalInterest = TotalPayments - TotalLoanAmount
        CBTotalInterest = CBTotalPayments - CBTotalLoanAmount
        TotalCost = TotalPayments + UpfrontPayment + TV
        CBTotalCost = CBTotalPayments + UpfrontPayment + TV
        print("TotalLoanAmount= ",TotalLoanAmount,"CBTotalLoanAmount= ", CBTotalLoanAmount,"UpfrontPayment= ", UpfrontPayment,"MonthlyPay= ",MonthlyPay,"CBMonthlyPay= ",CBMonthlyPay,"TotalPayments= ",TotalPayments,"CBTotalPayments= ",CBTotalPayments,"TotalInterest= ",TotalInterest,"CBTotalInterest= ",CBTotalInterest,"TotalCost= ",TotalCost,"CBTotalCost= ",CBTotalCost, sep="\n")
      elif IAF == "NO" and f1:
        TotalLoanAmount = AP - DP - TV 
        CBTotalLoanAmount = AP - DP - TV - CA
        UpfrontPayment = DP + SaleTax + OF
        MonthlyPay = TotalLoanAmount * (IRL/1200) * (((IRL/1200)+1)**LT)/((((IRL/1200)+1)**LT)-1)
        CBMonthlyPay = CBTotalLoanAmount * (IRH/1200) *(((IRH/1200)+1)**LT)/((((IRH/1200)+1)**LT)-1) 
        TotalPayments = MonthlyPay * LT
        CBTotalPayments = CBMonthlyPay * LT  
        TotalInterest = TotalPayments - TotalLoanAmount
        CBTotalInterest = CBTotalPayments - CBTotalLoanAmount 
        TotalCost = TotalPayments + UpfrontPayment + TV
        CBTotalCost = CBTotalPayments + UpfrontPayment + TV
        print("TotalLoanAmount= ",TotalLoanAmount,"CBTotalLoanAmount= ", CBTotalLoanAmount,"UpfrontPayment= ", UpfrontPayment,"MonthlyPay= ",MonthlyPay,"CBMonthlyPay= ",CBMonthlyPay,"TotalPayments= ",TotalPayments,"CBTotalPayments= ",CBTotalPayments,"TotalInterest= ",TotalInterest,"CBTotalInterest= ",CBTotalInterest,"TotalCost= ",TotalCost,"CBTotalCost= ",CBTotalCost,sep="\n")

      if TotalCost < CBTotalCost:
        result = "The Low Interest Rate Offer is Better!" 
        result1 = f"The low rate will save you {CBTotalCost - TotalCost} in interest, which is larger than the cash back of {CAinp}."
        print(result, result1)
      elif TotalCost > CBTotalCost:
        result = "The Cash Back Offer is Better!" 
        result1 = f"The low rate will save you only {TotalCost - CBTotalCost} in interest, which is larger than the cash back of {CAinp}."
        print(result, result1)
      elif TotalCost ==  CBTotalCost:
        result = "Both offers save same amount of money!" 
        result1 = "Choose options as per your convenience"
        print(result, result1)

      context = {
          "CA":CAinp,
          "IRH":IRHinp,
          "IRL":IRLinp,
          "AP":APinp,
          "LT":LTinp,
          "DP":DPinp,
          "TV":TVinp,
          "ST":STinp,
          "OF":OFinp,
          "IAF":IAF,
          "f1":f1,
          "SaleTax":SaleTax,
          "TotalLoanAmount":TotalLoanAmount,
          "CBTotalLoanAmount":CBTotalLoanAmount,
          "UpfrontPayment":UpfrontPayment,
          "MonthlyPay":MonthlyPay,
          "CBMonthlyPay":CBMonthlyPay,
          "TotalPayments":TotalPayments,
          "CBTotalPayments":CBTotalPayments,
          "TotalInterest":TotalInterest,
          "CBTotalInterest":CBTotalInterest,
          "TotalCost":TotalCost,
          "CBTotalCost":CBTotalCost,
          "result":result,
          "result1":result1,
        }
      return render(request, "cashbackorlowinterestcalculator.html", context)
    except:
      return render(request, "cashbackorlowinterestcalculator.html",{"message":"Sorry, could not calculate the results."})
  else:
    return render(request, "cashbackorlowinterestcalculator.html")





