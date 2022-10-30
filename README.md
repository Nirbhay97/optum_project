# Optum Project

* Following visible successes on a wide range of predictive tasks, machine learning techniques are attracting substantial interest from 
  medical researchers and clinicians.
* With the use of machine learning algorithms our application uses parent’s medical history and records, to predict the probability of 
  various diseases in their children, providing the parents with early information for appropriate medical support required since childrens are not expressive about the problems they have.

## Inspiration 
* Infants with genetic disorders, including chromosomal abnormalities (aneuploidy syndromes or chromosomal deletion or duplication disorders) and
 monogenic  Mendelian disorders (caused by variants in single genes) contribute considerably to mortality in neonatal intensive care units (NICUs). 
* In the United States, major congenital malformations, affecting approximately 2% of births, are also reported to be the leading cause of infant   mortality,though the underlying etiology of these malformations may or may not be genetic.
* Moreover the data gathered from out appliacation has lot of valuable insights that can help researchers in medical industries and can give early on insights on product development and demand, correlations etc, thus creating lasting business values.
* Main foucs lies around increasing health value.
 

 ## What it does ? 
  Our application uses parent’s medical history and records, to predict the probability of various diseases in their children, providing the 
  parents with early information for appropriate medical support required. It thrives to build an healthcare social ecosystem (USP) with three features: 
  * Tweets section
  * prediction
  * getting insigths from gathered data for creating business values to firm
  
  
 ## how we built it ?  
We used Machine learning algorithms to predtict the chances of inheritance and recommendations. Worked on different algorithms and kept the one which gave ous least error(r2 score). We used Flask to intergrate our model with web app. We worked on different part like design, documentation and development.

## Challenges Faced  
Unavailibily of organized data was the major challenge. We used kaggle and synthetic medical data generator to form dataset. We removed outliers, null values, filtered data using appropriate techniques. 
    
  
## what we learnt  
 We learnt about the integration of various machine learning models to along with webapp. 
 It also gave us insights on the importance of data analysis and machine learning and sector and how data is GOLD.
 We also learnt flask and working with sqlaclhemy and improved documentation reading skills.
  
## What could be the next move
 * The more the data we have, the better. Collection of more personlized data will allow our model to produce more personlized results. 
 * Inclusion of more parameters about the parents medical history can be used to give more optimized results.
 * We can train our model in reverse way, wherein we will be studying behaviour of child along with medical history of parents and accordingly predict the childs probability of getting a disease.
 
 ## Technologies
Project is created with:
* Flask version: 2.2.2
* Flask-SQLAlchemy version: 3.0.2
* SQLAlchemy version: 1.4.42
* Sqlite3
 These are the main dependecies, rest are available in requirements.txt file.
 
## Setup
To run this project do the following steps:
Create a python virtual environment 

```
$ conda create -n envname python=x.x anaconda
$ conda activate envname

```
Clone the repo in the desired directory in the newly created environment:

```
$ git clone https://github.com/Nirbhay97/optum_project.git

```

running the application:

```
$ cd to/path/optum_project
$ python run.py

```
This establishes a server at port http://127.0.0.1:5000 . U can access it on any browser.


