# Fluff-Plus-Plus
A better way to code on your Casio Calculator

*Let me start by saying I didn't know the .fpp extension was already dedicated to Fortran*

Fluff++ is a transpiled language thats makes programming on your casio. It basically looks cleaner (especially with its Notepad++ custom syntax highlighting), and enables you to name variables.

## General structure

The code is divided in two parts: 
1. Variable declaration
2. Script 


Your code will always look like this:  

```
init
  (declare some variables here, and import libraries)
begin
  (write your script here)
end
```

Please note that any variable used in your script **must** be declared in the `init` block !

## Variables

There are 5 different types of variables:

-`var`, complex numbers  
-`lst`, lists of `var` (unfortunately, indexing starts at 1, 0 being the name of the list)  
-`mat`, matrices of `var`  
-`str`, strings  
-`const`, constants which can store any of the previous types (more on that later) 

### How to declare a variable ?

If you don't want to give it a value yet, just give its type and name:

```
init
  var age
  str name
begin
  ...
 ```
 
 You can also give it an initial value:
 
 ```
 init
  var age = 420
  str name = "Snoop"
begin
  ...
```

If you want to make sure your Calculator will use a specific name for one of your variable, you can use the `as` keyword:  
  
  ```
  init
    var i as I
    var age as A = 420
    str name as 3 = "Snoop"
    mat matrix as M
  begin
    ...
  ```
 Upon transpiling, Fluff++ will make sure `i` appears as the variable `I` in the Basic Casio code. `age` will appear as `A`, `Str 3` will be used for `name` and `Mat M` will be used for `matrix`.  
 For variable that are declared without the `as` keyword, their Basic Casio counterpart will be picked from the remaining numbers (for lists and strings) or letters (vars and matrices) in numerical/alphabetical order.  
 The `as` keyword is especially useful if you want to use the same variable in different programms. If you're using a programm to generate a level (using a matrix), and another programm in which you can explore said level,you can use `mat map as M` in both programms to make sure they'll use the same matrix.
 
 You can use commas to declare multiple variables of the same type:  
 
   ```
  init
    var k, i as I, age as A = 20, pi = 3.14
    str text1 = "Hello World !", name as N = "Hamster_Furtif"
    ...
  begin
    ...
  ```
 
 ### Special cases: declaring lists and matrices
 
 When declaring a list or a matrix, you can describe its content:  
 ```
 init
  lst fibonnaci as 1 = {1, 1, 2, 3, 5}
  mat identity = [[1,0,0][0,1,0][0,0,1]]
 begin
  ...
 ```
 
 (Although please use the `identity` function from the `matrix` library if you ever need the identity matrix...)  
   
 You can also set the dimensions of your list/matrix when delcaring it:  
 ```
 init
  lst my_list_of_length_7 = 7
  mat my_matrix_with_5_rows_and_9_columns = {5,9}
begin
  ...
```
**WARNING** This will reset your list/matrix (fill it with 0s)
 
 ### Constants
 
 Upon declaring a `const`, you must give it a value, as it cannot be changed later. A `const` will be replaced by the value you have given it upon transpiling.    
 The following code  
   
 ```
 init
  const HP = 1, MANA = 2, STAMINA = 3
  const MAX_HP = 100
  lst player as 5 = 3 
 begin
  player[HP] = MAX_HP
  player[MANA] = 20
  player[STAMINA] = 50
 end
 ```
 will transpile into this:
 ```
 3→Dim List 5
 100→List 5[1]
 20→List 5[2]
 50→List 5[3]
 ```
 
 ### Limitations
 
 When declaring a lot of variable, please make sure you stay in bounds of what the calculator can support:  
   
  -You can only have up to 26 `var`, and the `as` keyword must be followed by a capital letter A→Z  
  -You can only have up to 26 `lst`, and the `as` keyword must be followed by a number 1→26  
  -You can only have up to 26 `mat`, and the `as` keyword must be followed by a capital letter A→Z  
  -You can only have up to 20 `str,`and the `as` keyword must be followed by a number 1→20  
