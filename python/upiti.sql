select count(Title) from dmoz_categories 
where Topic like '%/Sports/%' and categoryDepth = 4 and filterOut=0

select count(Title), categoryDepth from dmoz_categories where filterOut=0 group by categoryDepth

select Title, catid from dmoz_categories where categoryDepth = 1 and filterOut = 0

select count(*),categoryDepth from dmoz_categories where Description != "" and filterOut = 0 group by categoryDepth

select Title, catid from dmoz_categories where Topic like '%/Arts/%' and Description != '' and categoryDepth >=1 and categoryDepth <= 14 and filterOut = 0

select count(*) from dmoz_categories where Topic like '%/Arts/%' and filterOut = 0 and Description = ''

select max(categoryDepth) from dmoz_categories

select distinct(fatherid), categoryDepth from dmoz_categories 
where Topic like '%/Arts/%' and filterOut = 0 and categoryDepth > 1 and categoryDepth < 15 
group by categoryDepth