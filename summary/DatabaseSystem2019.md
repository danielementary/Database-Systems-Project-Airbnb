##Introduction to Database System
####2019
####Sophie Ammann
---------
###Lecture 1

#####1.1 Terminology :
* **Data** : facts, basis for reasoning, useful or irrelevant (only 10% of data is useful). Must be *processed* to be meaningful. "Everything that can be mathematicaly defined is data"
* **Information** : meaning, relevant to the problem
* **Database (DB)** : large, integrated, structured collection of data
* **Database Management System (DBMS)** : software system designed to store,
manage and facilitate access to databases (connected bridge btw user and database)
* **Data model** : collection of concepts for describing data (relational, hierarchical, graph,...)
* **Relational data model** : set of records represented by a table.


#####1.2 Relational data model
* **Relation** : table with row and columns
* **Schema** : Describes the structure (columns) of a relation

#####1.3 Logical and physical data independence
Data independence is the ability to change the schema at one level of the database system without changing the schema at the next higher level

* **Logical data independence** : capacity to change the conceptual schema without changing the user views
* **Physical data independence** : capacity to change the internal schema without having to change the conceptual schema or user views

---------
###Lecture 2 : ER model
#####2.1 Conceptual design
ER model = entity-relationship model <br>
* **Entity** : real-world object, distinguishable from other objects. <br>
**Attributes** are used to describe an entity. (defined in a domain)
* **Entity set** : A collection of similar entities. E.g., all employees<br>
**Key** : each entity set has a key
* **Relationship** : association between entities, can have their own attributes.
#####2.2 Constraints
######2.2.1 Key constraints

![key](images/key_constraints.png "key")
* Many-to-many : <br>
an employee can work in many departments; a department can have many employees

* One-to-many : <br>
each department has at most one manager

* One-to-one : <br>
each driver can drive at most one vehicle and each vehicle will have at most one driver.

######2.2.2 Participation constraints
![participation](images/participation_constraints.png "key")
* Total participation : <br>
Every employee should work in
at least one department.<br>
Every department should have
at least one employee.

* Participation + key constraint :<br>
There could be some employees
who are not managers.<br>
Every department should have at
least one manager.

* Partial participation : <br>
There could be some customers
who do not buy any products. <br>
There could be some products
which are not bought by any
customers.<br>

#####2.3 Weak entities
Entity that can be identified uniquely only by considering the primary key of another entity (owner).
![weak](images/weak_entity.png "weak")
There has to be a one-to-many relationship (one owner, many weak entities).<br>
The weak entity set must have total participation

#####2.4 Ternary relationships
![weak](images/ternary_relation.png "weak")

#####2.5 ISA ('is a') hierarchies
Attributes inherited
![weak](images/isa_hierarchie.png "weak")
######2.5.1 **Constraints** :
* **Overlap cosntraints** :
*Can a student be a master as well as a doctorate entity? (Allowed/Disallowed)*
* **Covering constraints** : *Does every Employees entity also have to be an Hourly_Emps or a Contract_Emps entity? (Yes/No)*
![weak](images/example_hierarchie.png "weak")

#####2.6 Aggregation :
Can treat a relationship set as an entity set.
![weak](images/aggregation.png "weak")


---------
###Lecture 3 : Data model
**SQL** = Structured Query Language
#####3.1 Creating relations in SQL
![table](images/sql_creation.png "key")

#####3.2 Key
* **superkey** : <br>
Set of attributes for which no two distinct tuples can have same values in all key fields . Can be all the attributes, or just a few.
* **key** :<br>
 minimal superkey (no subset of the fields is a superkey)
* **candidate key** :<br>
 if there are multiple keys, then each of them is referred to as candidate key
* **primary key** : <br>
one of the candidate key is chosen

*Example :*
![key](images/candidate_keys.png "key")
* *UNIQUE* keyword indicates a candidate key that is not the primary key.
* *PRIMARY* keyword indicates the primary key.

#####3.3 Integrity constraints (ICs)
* **IC** = condition that must be true for any instance of the database (the domain constraints)<br>
* **legal instance** : satisfies all the specified ICs.<br>
//TODO ...

---------
###Lecture 4 : Relational algebra
#####4.1 Introduction
relation algebra = operational, useful for representing execution plans <br>
* query is applied to *relation instances*, the result is also a *relation instance*.
* Schema of the input relations for a query is **fixed** (but query will run over any legal instance)
* Schema of output (result) of a given query is also **fixed**

#####4.2 Basic operations
* **selection** $\sigma$ :<br>
  selects *rows* from a relation (horizontal) <br>
  $\leftrightarrow$ *WHERE* in SQL

  *example :*
  ![selection](images/selection.png "sel")

* **projection** $\pi$ : <br>
  retains only wanted *columns* from a relation (vertical) <br>
  $\leftrightarrow$ *SELECT* in SQL

  *example :*
  ![proj](images/projection.png "proj")
* **cross-product** $\times$ :<br>
  combines two relations

  *example :*
  ![cross_product](images/cross_prod.png "cross")

* **set-difference** $-$ : <br>
  tuples in $R_1$ but not in $R_2$<br>

  $R_1$ and $R_2$ must be *union compatible* (same number of fields and fields of same type)

  *example :*
  ![set_diff](images/set_diff.png "set_diff")

* **union** $\cup$ : <br>
  tuples in $R_1$ and/or in $R_2$<br>

  $R_1$ and $R_2$ must be *union compatible* (same number of fields and fields of same type)

  *example :*
  ![union](images/union.png "sel")


#####4.3 Renaming operator $\rho$
renames the list of attributes :<br>
$<oldname> \longrightarrow <newname>$<br>
or<br>
$<position> \longrightarrow <newname>$<br>, where *position* starts at 1!

*example :*
![rename](images/rename.png "rename")

#####4.4 Compound operators
######4.4.1 Natural join $\Join$
*idea* : <br>
* compute $R \times S$
* select rows where attributes that appear in both relations have equal values
* project all unique attributes and one copy of the common ones <br>

*example :*
![natJoin](images/nat_join.png "natJoin")

######4.4.2 Condition join or theta-join $\Join_c$

$R\Join_c S = \sigma_c (R \times S)$

######4.4.3 Equi-join
special case of the theta-join : condition *c* contains only conjunction of equality conditions<br>

*example :*<br>
good way of finding all pairs of sailors in $S_1\times S_2$ who have the same age : <br>
$$
  \sigma_{sid_1 < sid_2}(S_1 \Join_{age = age_2}\rho _{age \rightarrow age2, sid \rightarrow sid2}(S_2))
$$

######4.4.3 Division
$A/B$ contains all $x$ tuples such that for every tuple in $B$, there is an $(x,y)$ tuple in $A$.<br>
($B$ is a proper subset of $A$)
