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
