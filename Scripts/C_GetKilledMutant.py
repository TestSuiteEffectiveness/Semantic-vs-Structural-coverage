
def loadMutant(filename):
    file=open('m/'+filename+'.txt');
    lines=file.readlines();
    data={};
    for line in lines:
        line=line.strip().split(",");
        if line[0]=='':
            continue
        test=line[0].strip();
        output=line[1].strip();
        data[test]=output;
    count=len(data);
    if count!=133:
        print(filename,count);
    return data;

def isSame(res_a,res_b):
    for t in res_a:
        if res_a[t]!=res_b[t]:
            return False;
    return True;
mutants=[""]

'''nums = [
    125, 132, 133, 134, 135, 136, 137, 138, 140, 141,
    144, 145, 146, 149, 151, 152, 153, 155, 157, 158,
    163, 165, 166, 167, 168, 169, 170, 171, 173, 174,
    176, 177, 178, 179, 182, 184, 185, 186, 188, 190,
    191, 194, 196, 206, 218, 220, 227, 228, 229, 230
]

for x in nums:
    value="M"+str(x)
    mutants.append(value)

'''

for x in range(125,249):
    value="M"+str(x)
    mutants.append(value)


del mutants[0]


    

base_results=loadMutant('base'); #load the results of the base program
results={};
for m in mutants:
    results[m]=loadMutant(m); #load the results of each mutant (test number: test outcome)


d0={};
killedMutants=[];
SurvivedMutants=[];
for m in mutants:
    
    d0[m]=[];
    
    for t in results[m]:
        #for d0, we assume error is an output and we compare strings
        #d1 this is d1 we skip error
        print(m,t)
        if results[m][t]!=base_results[t] and base_results[t]!='class java.lang.Exception' and results[m][t]!='class java.lang.Exception': 
            d0[m].append(t)
       

writer=open("delta_analysis.csv",'w');
writer.write("Mutants,Killed Mutants\n");
for m in mutants:
    if len(d0[m])==0:
        d0[m]=["Empty"];
        SurvivedMutants.append(m)
    else:
        killedMutants.append(m)
    
    
    
    tmp=[m,";".join(d0[m]),"\n"];
    writer.write(",".join(tmp));
file=open('killedsurvived.txt','w')
file.writelines("survived mutants=")
file.writelines(str(len(SurvivedMutants)))
file.writelines("\n")

file.writelines(str(SurvivedMutants))
file.writelines("\n")
file.writelines("Killed mutants=")
file.writelines(str(len(killedMutants)))
file.writelines("\n")

file.writelines(str(killedMutants))

file.close()

writer.close();

print("survived mutants: ",SurvivedMutants);
print("killed mutants:",killedMutants);
