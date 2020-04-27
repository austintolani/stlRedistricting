# St. Louis 2020 Ward Redistricting



In 2012, voters in the City of St. Louis passed a proposition https://www.stlouis-mo.gov/internal-apps/legislative/upload/committee-substitute/BB31CS3.pdf to redraw the city's ward boundaries following the 2020 census, reducing the number of wards from 28 to 14. This website contains a result of a project that aimed to research redistricting methods, produce a workflow for generating new ward boundaries and produce sample boundaries based on current American Community Survey data. 



The background [link] section of the site provides information on the aforementioned proposition  and discusses the importance of redrawing the ward boundaries in a fair manner. 

The redistricting criteria [link] section of the site lists the various criteria used in this project to evaluate new ward boundaries. 



The redistricting methods [link] section of the site explains the various methods and tools used to create new ward boundaries. 



The results [link] section of the site shows several new ward boundaries created by the various redistricting methods. 



The feedback [link] section of the site allows you to leave feedback on what you think about redistricting criteria. 



The about [link] section of the site gives more information about this project. 



## Background

[INSERT MAP OF CURRENT BOUNDARIES]

Since the 1950's, the City of St. Louis has experience significant population decline, losing over half of its population.  Despite this population loss, St. Louis is still governed by 28 alderpersons who represent 28 wards. In 2012, voters in the City of St. Louis passed Proposition R, a measure to reduce the number of wards (and consequently alderpersons) from 28 to 14. This measure is now known as St. Louis City Ordinance #69185 https://www.stlouis-mo.gov/government/city-laws/ordinances/ordinance.cfm?ord=69185. This ordinance stipulates that beginning January 1, 2022, the city will be divided into 14 wards and such ward boundaries will be based on the 2020 Census. In addition, the ordinance states that the ward boundaries "shall comprise as nearly as practicable, compact and contiguous territory within straight lines, and contain as nearly as may be the same number of inhabitants".

Alderpeople play an extremely important role in St. Louis politics. The Board of Aldermen is responsible for passing legislation, monitoring city agencies, making decisions on land use and various other issues. An alderperson influences numerous decisions in their ward, ranging from zoning changes to business licensing. Given the importance of alderpeople, it is crucial that the wards are redrawn in a way that is fair and represented of St. Louis and its people. The next section, Redistricting Criteria [link], lists the various criteria used when considering new ward boundaries to ensure they are fair. 



## Redistricting Criteria



Ordinance #69185 https://www.stlouis-mo.gov/government/city-laws/ordinances/ordinance.cfm?ord=69185 stipulates that the new ward boundaries "shall comprise as nearly as practicable, compact and contiguous territory within straight lines, and contain as nearly as may be the same number of inhabitants." In addition to these criteria, there are other criteria identified by Supreme Court case law, namely preserving communities of interest, preserving existing political and geographical boundaries,  and respect for minority representation. For more information, the Brennan Center for Justice's A Citizen's Guide to Redsitricting [https://www.brennancenter.org/sites/default/files/legacy/CGR%20Reprint%20Single%20Page.pdf](https://www.brennancenter.org/sites/default/files/legacy/CGR Reprint Single Page.pdf) is a useful resource. Below I have listed all of the criteria considered in my analysis along with tangible measures of them (if applicable).



| Criteria                                                     | Description                                                  | Measure                                                      | Value Needed to Satisfy Criteria               |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------------- |
| Equal population                                             | Ward populations should be roughly equal in number.          | Total population deviation between wards must not be greater than 10%. To check this, we can calculate the deviation for each ward and ensure that there is no difference in deviations between wards greater than 10%. | Total population deviation < 10%               |
| Contiguity                                                   | Every part of the ward must be reachable from every other part without crossing the ward boundary. | This can be easily assessed visually.                        | All wards must be contiguous.                  |
| Compactness                                                  | Every ward should have a regular shape with constituents living relatively close to each other. | This can be measured using the Polsby-Popper test [https://en.wikipedia.org/wiki/Polsby%E2%80%93Popper_test](https://en.wikipedia.org/wiki/Polsby–Popper_test). This is a mathematical measure of compactness. The value of this test will always fall between 0 and 1, where a score of 0 indicates a lack of compactness (a straight line) while a score of 1 indicates maximal compactness (a circle). | Polsby-Popper score > 0.3                      |
| Preservation of Minority Voting Power                        | Minority voting power should be preserved. This means that minority groups should have an effective opportunity to win a ward based on the region's total population. | St. Louis is 46.2% African American. Therefore, 46.2% of the wards (7 wards) should allow for African Americans to have an effective opportunity to elect a candidate of their choosing. An effective opportunity means having more than 50% minority population in a given ward. While St. Louis does have other minority populations, none have large enough of a population where they require a ward with an effective opportunity to elect a candidate of their choosing. | 7 wards with > 50% African American population |
| Preservation of Communities of Interest and Political and Geographic Boundaries | Communities of interest and political and geographic boundaries should be preserved where possible. Wards should not split up such boundaries. Neighborhoods in St. Louis represent communities of interest. Political boundaries in St. Louis include Special Business Districts, Tax Increment Financing Districts, Transit Orientated Development Districts and Community Improvement Districts. Geographic boundaries include parks. | For a given community of interest, political or geographic boundary, we can calculate what percentage of it falls within each ward. We consider the largest of these percentages for each ward and take the average for all features. For the purposes of this project, we call this the "Cohesion Score". In summary, this score represents the percentage, on average, that each feature in a community of interest or political or geographic boundary, falls within the ward it is most within. | Average Cohesion Score > 80%                   |



For each of the ward boundaries created by the redistricting methods [link] described in the next section, the above criteria will be used for evaluation. 



## Redistricting Methods

I used three different methods to generate new ward boundaries: 

- Manual redistricting (drawing new ward boundaries by hand)
- Use of Auto-Redistrict http://autoredistrict.org/, a computer program that automatically create fair and compact electoral districts. 
- Use of BARD: Better Automated Redistricting https://www.jstatsoft.org/article/view/v042i04, an open source software package for general redistricting and redistricting analysis. 

For all of these methods, I used census block groups as the geographical unit of analysis and used the most recent (2018) American Community Survey estimates for demographic data. This page provides a general outline of the redistricting methods used, for more specifics on the workflow, see the workflow section [LINK].

**Manual Redistricting**

To draw the ward boundaries by hand, I used Esri's Districting extension for ArcMap/ArcCatalog. This useful extension allows you to draw boundaries while summarizing various statistics relevant to redistricting. When drawing the ward boundaries, I carefully examined demographic data and boundaries of interest to iteratively improve the boundaries until I reached a reasonable solution. 

**Auto-Redistrict**

As mentioned, Auto-Redistrict http://autoredistrict.org/ is a computer program that automatically creates fair and compact electoral district. It uses a heuristic search algorithm to evaluate potential solutions based on criteria like equal population, contiguity, compactness, minimal splitting and minimal racial gerrymandering. Once I imported the data for St. Louis and configured how the program prioritized different criteria, I was able to export a solution for St. Louis. 

**BARD: Better Automated Redistricting**

BARD is a software package for general redistricting and redistricting analysis. It supports automated generation of redistricting plans by assigning different weights to various criteria. Once using this package in the way described in the workflow section [link] I was able to output a solution. 





For the later two methods, I took the solutions and manually tweaked them. As a result, I ended up with 5 different solutions: the result from manual redistricting, from Auto-Redistrict, from Auto-Redistrict after manual tweaking, from BARD, and from BARD after manual tweaking. To view these results, see the result section [link]. 





 