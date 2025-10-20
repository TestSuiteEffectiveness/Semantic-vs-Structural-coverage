import os
import subprocess
import shutil

mutants_dir='Survived'
target='src/main/java/org/apache/commons/math3/util/FastMathAA.java'
for filename in os.listdir(mutants_dir):
    source = os.path.join(mutants_dir, filename)
    
    mutant_name=filename.split('.java')[0]
    if os.path.isfile(source):
        print(source)
        shutil.copyfile(source, target)
        subprocess.run(['mvn','clean','compile','test', '-Drat.numUnapprovedLicenses=100'], capture_output=True, shell=True, text=True)
        print(filename)
        os.rename('outputTest/T0.txt', 'outputTest/M'+mutant_name+'.txt')
        
