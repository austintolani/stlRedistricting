
#Import libraries and set environmental vairables
library("BARD")
setwd("C:/Users/austi/Desktop/GISClinic/BARD")
library("maptools")

#Import shapefile and set number of districts
stl.plan <- importBardShape("block_groups")
numDists <- 14
#Generate initial plan using weighted k-means
wkPlan <- createWeightedKmeansPlan(stl.plan,numDists, weightVar="TotalPop")

#Define score function
calcPopScore(wkPlan, predvar="TotalPop")
calcContiguityScore(wkPlan)
calcBBCompactScore(wkPlan)
calcRangeScore(wkPlan,predvar="Black_alon",predvar2="TotalPop",targrange=c(.50,.65))
myScore<-function(plan,...){
combineDynamicScores(plan,scorefuns=list(function(x,...)calcPopScore(x, predvar="TotalPop"),calcContiguityScore,calcBBCompactScore,function(x,...)calcRangeScore(x,predvar="Black_alon",predvar2="TotalPop",targrange=c(.50,.65))))

}
# Apply optimization algorithm to yield improved plan
improvedwkPlan <- refineGreedyPlan(plan=wkPlan, score.fun=myScore, displaycount=NULL, historysize=0, dynamicscoring=FALSE,   tracelevel=1, checkpointCount=0, resume=FALSE)

# Export plan
exportBardShape(wkPlan, "C:/Users/austi/Desktop/GISClinic/BARD/BARDOutput.shp", id = "BARDPlanID")