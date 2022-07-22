# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 23:14:00 2022
@author: hanna
"""
from  numpy import *
from  matplotlib.pyplot import *

#This is a project about sparse matrices

class SparseMatrix:#Har ej orkat raisa exceptions
    
    def __init__(self, matrix, *tol):
        """
        Creates a sparse matrix from matrix matrix with 

        """
        self.intern_represent='CSR'
        self.number_of_nonzero=0
        self.size=(len(matrix), len(matrix[0]))#För att kunna skapa rätt storlek på ny matris.
        if len(tol)==0:
            self.tol=1.e-200
        else:#Antar att man nt skickar in nåt annat dumt.
            self.tol=tol[0]
            
        self.set_intern_represent('CSR', matrix)
        self.number_of_nonzero=len(self.values)#behlvs ej vid byte av repr. därför har jag den här.
    
    def changeVal(self, row, col, newVal):
        """
        Inserts newValue in position row, col in the sparse matrix.

        """
        row_start=self.row_index[row]#Tar ut elementen mellan dessa radindex från el-vek och col-vek
        row_end=self.row_index[row+1]
        cols=self.col_index[row_start:row_end]
    
            
        for i in range(len(cols)):#Om det redan finns ett värde i aktuell kolumn
            if cols[i]==col:
                if newVal>self.tol:
                    self.values[row_start+i]=newVal#Behöver ej ändra i col_index:)
                    return 
                else:
                    self.values.pop(row_start+i)
                    self.col_index.pop(row_start+i)
                    self.update_row('-', row)
                    return
        
        if newVal>self.tol:
            new_row=row_start
            for i in range(len(cols)):#Om det inte redan finns ett värde i aktuell kolumn.
                if col<cols[i]:
                    new_row=new_row+i
                    break
            self.col_index.insert(new_row, col)
            self.values.insert(new_row, newVal)
            self.update_row('+', row)
        else:
            return
    
    def CSR_to_CSC(self):
        """
        Needed in the equals method. Otherwise the internal representation changed when comparing matrices.

        """
        CSC_matrix=zeros(self.size)
        count=0
        for i in range(len(self.row_index)-1):#Gör ny matris.
            if count<len(self.row_index)-1:
                for j in range(self.row_index[count], self.row_index[count+1]):
                    CSC_matrix[count][self.col_index[j]]=self.values[j]
                count=count+1
        
        self.set_intern_represent('CSC', CSC_matrix)
        
    
    def CSC_to_CSR(self):
        CSR_matrix=zeros(self.size)
        count=0
        for i in range(len(self.col_index)-1):#Gör ny matris.
            if count<len(self.col_index)-1:
                for j in range(self.col_index[count], self.col_index[count+1]):
                    CSR_matrix[self.row_index[j]][count]=self.values[j]
                count=count+1
        
        self.set_intern_represent('CSR', CSR_matrix)
        
    
    def __eq__(self, other):#Detta är säkert också väldigt dumt men funkar:)
        """
        Checks whether the matrices are exactly equal.
        """
        changed_other=False
        changed_self=False
        if other.intern_represent=='CSR':
            other.CSR_to_CSC()
            changed_other=True
            
        if self.intern_represent=='CSR':
            self.CSR_to_CSC()
            changed_self=True
        
        if other.values==self.values and other.row_index==self.row_index and other.col_index==self.col_index:
            if changed_other:
                other.CSC_to_CSR()
            if changed_self:
                self.CSC_to_CSR()
            return True
        if changed_other:
          other.CSC_to_CSR()
        if changed_self:
            self.CSC_to_CSR()
        return False
    
    #Egenimplementerade metoder.
    
    def __repr__(self):
        return (f"Values: {self.values} \nRowIndex: {self.row_index} \nColIndex: {self.col_index}")
                
    
    def set_intern_represent(self, intRep, matrix):
        """
        Creates a sparseMatrix from the matrix matrix with internal representation intRep
        """
        self.values=[]
        self.row_index=[]
        self.col_index=[]
        if intRep=='CSR':
            first_it_length=len(matrix)#Itererar över raderna först.
            second_it_length=len(matrix[0])#Sen kolonnerna.
            self.row_index.append(0)#För att få med nollan som första tal i rad-vektorn.
        else:
            first_it_length=len(matrix[0])#Itererar över kolonnerna först.
            second_it_length=len(matrix)#Sen raderna.
            self.col_index.append(0)#För att få med nollan som första tal i kolonn-vektorn.
        
        value_counts=0#Dåligt namn, är egentligen det som säger när man ska byta rad i värdesmatrisen.
        for i in range(first_it_length):#Kör det som står i WIKI.
            for j in range(second_it_length):
                if intRep=='CSR':
                    element=matrix[i][j]
                else:
                    element=matrix[j][i]
                    
                if element>self.tol:
                    self.values.append(element)
                    if intRep=='CSR':
                        self.col_index.append(j)
                    else:
                        self.row_index.append(j)
                    value_counts=value_counts+1
            if intRep=='CSR':
                self.row_index.append(value_counts)
            else:
                self.col_index.append(value_counts)
        
        self.intern_represent=intRep
    
    
    def update_row(self, sign, row):#Används då man lägger till eller tar bort tal. 
        """
        Increases row_index and changes number of nonzeros.
        """
        if sign=='+':
            add_or_delete=1#Om tillagt tal på tidigare nolla
        elif sign=='-':
            add_or_delete=-1#Om tillagd nolla på tidigare tal
        for i in range(row+1, len(self.row_index)):#Uppdaterar raderna.
            self.row_index[i]=self.row_index[i]+add_or_delete
        self.number_of_nonzero=self.number_of_nonzero+add_or_delete#Uppdaterar antalet nonzeroes.
        
        





#Testing

matrix1=array([[1,2,3],#Påhittad, verkar ok
                [0,0,0],
                [0,2,3]])#Antar att det är ok att ha två treor efter varandra i row_index.
sparseMatrix1=SparseMatrix(matrix1)

matrix2=diag([5,8,3,0])+diag([0,6], -2)#Den första på Wiki
sparseMatrix2=SparseMatrix(matrix2)

matrix3=array([[10,20,0,0,0,0],#Den andra på Wiki
                [0,30,0,40,0,0],
                [0,0,50,60,70,0],
                [0,0,0,0,0,80]])
sparseMatrix3=SparseMatrix(matrix3)

matrix4=array([[1,2,3],#För att testa likhet mellan olika objekt.
                [0,0,0],
                [0,2,3]])
sparseMatrix4=SparseMatrix(matrix4)

# print(sparseMatrix1)
# print(sparseMatrix2)
# print(sparseMatrix3)

#Testar changeVal
# sparseMatrix1.changeVal(1,2,3)#Om det ej finns värden i raden innan!OK

# sparseMatrix1.changeVal(1,1,0)#Inga värden i raden och lägger till nolla

# sparseMatrix1.changeVal(2,2,10)#Om det redan finns värde

# sparseMatrix1.changeVal(2,2,0)#Om det redan finns värde och lägger till nolla

# sparseMatrix1.changeVal(2,0,1)#Om det inte finns värde i kolumnen men i raden

# sparseMatrix1.changeVal(2,0,0)#Om det inte finns värde i kolumnen men i raden, lägger till 0

# sparseMatrix1.CSR_to_CSC()#Funkar men väldigt ineffektiv.
# sparseMatrix1.CSC_to_CSR()#Har ej fixat error om typen redan är csr.
# sparseMatrix2.CSR_to_CSC()
# sparseMatrix3.CSR_to_CSC()

# print(sparseMatrix1==sparseMatrix2)#Testar equals
# print(sparseMatrix1==sparseMatrix1)
# print(sparseMatrix1==sparseMatrix4)#Funkar

print(sparseMatrix1)
# print(sparseMatrix2)
# print(sparseMatrix3)