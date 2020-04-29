###########################################################################################
# User Defined variables:
import sys
import arcpy
import os
from tqdm import tqdm
PATH = r"C:\Users\austi\Desktop\GISClinic\AutoRedistrict2"
scratchGDB = r""
blockGroups = "BlockGroups.shp"
neighborhoods = "Neighborhoods.shp"
fieldNames = ["White_alon", "Black_alon", "Indian_Ala",
              "Asian_alon", "HawaiiPaci", "SomeOtherR", "TwoOrMore"]
parks = "Parks.shp"
numDists = 14
############################################################################################

"""calculatePopulations fills a dictionary with the total population and voting age population for each proposed ward
"""


def calculatePopulations():
    # Iterate through all wards
    wardCursor = arcpy.da.SearchCursor(candidateWards, [wardNameField])
    for ward in wardCursor:
        # Select BGs inside of ward
        query = wardNameField + " =" + str(ward[0])
        arcpy.MakeFeatureLayer_management(candidateWards, "tempLayer", query)
        arcpy.SelectLayerByLocation_management(
            "blockGroupLayer", "have_their_center_in", "tempLayer")
        # Calculate populations
        bgCursor = arcpy.da.SearchCursor(
            "blockGroupLayer", ["VotingAgeP", "TotalPop"])
        totalPopulation = 0
        votingAgePopulation = 0
        for bg in bgCursor:
            totalPopulation += bg[1]
            votingAgePopulation += bg[0]
        # Update dictionary
        Wards[str(ward[0])]["totalPopulation"] = totalPopulation
        Wards[str(ward[0])]["votingAgePopulation"] = votingAgePopulation
    del wardCursor
    del bgCursor
    # Add and update fields in shapefile
    arcpy.AddField_management(candidateWards, "totalPop", "LONG")
    arcpy.AddField_management(candidateWards, "votingPop", "LONG")
    wardCursor = arcpy.da.UpdateCursor(
        candidateWards, [wardNameField, "totalPop", "votingPop"])
    for ward in wardCursor:
        ward[1] = long(Wards[str(ward[0])]["totalPopulation"])
        ward[2] = long(Wards[str(ward[0])]["votingAgePopulation"])
        wardCursor.updateRow(ward)
    del wardCursor


"""calculateCompactness calculates the Polsby-Popper test for each proposed ward and updates each ward with the respective value
"""


def calculateCompactness():

    wardCursor = arcpy.da.SearchCursor(
        candidateWards, [wardNameField, "Shape_Leng", "Shape_Area"])
    for ward in wardCursor:
        # Calculate Polsby-Popper test
        ppValue = (4*math.pi*ward[2])/(math.pow(ward[1], 2))
        Wards[str(ward[0])]["ppValue"] = ppValue
    del wardCursor

    # Add and update fields in shapefile
    arcpy.AddField_management(candidateWards, "ppScore", "FLOAT")

    wardCursor = arcpy.da.UpdateCursor(
        candidateWards, [wardNameField, "ppScore"])

    for ward in wardCursor:
        ward[1] = float(Wards[str(ward[0])]["ppValue"])
        wardCursor.updateRow(ward)
    del wardCursor


"""calculateCohesion calculates the average number of times at which features in the input set are split by the proposed wards

Args:
    fileName (shapefile): input features to compare against wards
Returns:
    float: average number of splits for all input features
"""


def calculateCohesion(fileName):
    percentages = {}
    # Generate tabulate intersection table
    table = arcpy.TabulateIntersection_analysis(in_zone_features=fileName, zone_fields="FID", in_class_features=candidateWards, out_table=scratchGDB +
                                                "/TabulateIntersection", class_fields=wardNameField, sum_fields="", xy_tolerance="-1 Unknown", out_units="UNKNOWN")
    tableCursor = arcpy.da.SearchCursor(table, ["FID", "PERCENTAGE"])
    currentId = None
    # Based on tabulate intersection operation, calculate the total, then average number of splits
    for row in tableCursor:
        if (currentId is None or currentId != row[0]):
            currentId = row[0]
            percentages[currentId] = [row[1]]
        else:
            percentages[currentId].append(row[1])
    total = 0
    for row in percentages:
        numSplits = 0
        for percentage in percentages[row]:
            if (percentage) > 1:
                numSplits += 1

        total += numSplits

    return total*1.0/len(percentages)
    del tableCursor


"""calculateMinority determines if the proposed ward ensure sufficient representation for minority groups
Args:
    percentage (int): what percentage represents "sufficient representation"
    minWards (int): The minimum number of wards needed with sufficient representation
    minorityField(string) : The name of the field representing the minority group
Returns:
    boolean: represents if there is sufficient representation for minority groups
"""


def calculateMinority(percentage, minWards, minorityField):
    wardCursor = arcpy.da.SearchCursor(candidateWards, [wardNameField])
    wardPercentages = {}
    for ward in wardCursor:
        # Select BGs inside of ward
        query = wardNameField + " =" + str(ward[0])
        arcpy.MakeFeatureLayer_management(candidateWards, "tempLayer", query)
        arcpy.SelectLayerByLocation_management(
            "blockGroupLayer", "have_their_center_in", "tempLayer")

        # Calculate percentages
        bgCursor = arcpy.da.SearchCursor(
            "blockGroupLayer", ["TotalPop", minorityField])
        totalPop = 0
        totalBlack = 0
        for bg in bgCursor:
            totalPop += bg[0]
            totalBlack += bg[1]

        wardPercentages[str(ward[0])] = {
            "totalPopulation": totalPop, "totalBlack": totalBlack, "percentageBlack": 100*(float(totalBlack)/totalPop)}

    numMajorityBlack = 0
    for ward in wardPercentages:
        if wardPercentages[ward]["percentageBlack"] >= percentage:
            numMajorityBlack += 1
    if numMajorityBlack >= minWards:
        return True
    else:
        return False
    del bgCursor
    del wardCursor

    """updatePopulations a helper function that updates the war boundaries with attributes representing their total populations
    """


def updatePopulations():

    for name in fieldNames:
        wardCursor = arcpy.da.SearchCursor(candidateWards, [wardNameField])
        for ward in wardCursor:
            # Select BGs inside of ward
            query = wardNameField + " =" + str(ward[0])
            arcpy.MakeFeatureLayer_management(
                candidateWards, "tempLayer", query)
            arcpy.SelectLayerByLocation_management(
                "blockGroupLayer", "have_their_center_in", "tempLayer")

            # Calculate percentages
            bgCursor = arcpy.da.SearchCursor("blockGroupLayer", [name])
            total = 0
            for bg in bgCursor:
                total += bg[0]

            Wards[str(ward[0])][name] = total
        del wardCursor
        del bgCursor
        # Add and update fields in shapefile
        arcpy.AddField_management(candidateWards, name, "LONG")

        wardCursor = arcpy.da.UpdateCursor(
            candidateWards, [wardNameField, name])

        for ward in wardCursor:
            ward[1] = float(Wards[str(ward[0])][name])
            wardCursor.updateRow(ward)
        del wardCursor


# Initialize progress bar
pbar = tqdm(total=100, desc="Progress")

# Import libraries and set workspace variables
pbar.update(25)

arcpy.env.workspace = PATH
arcpy.env.overwriteOutput = True

arcpy.MakeFeatureLayer_management(blockGroups, "blockGroupLayer")
candidateWards = str(sys.argv[1])
wardNameField = str(sys.argv[2])
# Initialize dictionary data structure with wards as keys
Wards = {}
wardCursor = arcpy.da.SearchCursor(candidateWards, [wardNameField])
for ward in wardCursor:
    Wards[str(ward[0])] = {}
del wardCursor


pbar.update(25)
# Population
calculatePopulations()

# Calculate the total population of the area (always will be 311,273)
totalPopulation = 0
for ward in Wards:
    totalPopulation += Wards[ward]["totalPopulation"]

# Calculate relative deviation for each ward
IdealPop = totalPopulation/numDists
deviations = []

for ward in Wards:
    deviation = float((Wards[ward]["totalPopulation"] - IdealPop))/IdealPop
    deviations.append(deviation)

deviations.sort()

# Calculate largest negative and positive deviation
largestPosDeviation = 0

if (deviations[-1] > 0):
    largestPosDeviation = deviations[-1]

largestNegDeviation = 0
if (deviations[0] < 0):
    largestNegDeviation = deviations[0]

# Calculate overall range and output result
overallRange = largestPosDeviation + abs(largestNegDeviation)
if (overallRange < 0.1):
    print ("\n \n POPULATION: Equal population criteria satisfied with an overal range of " +
           str(overallRange) + ".")
else:
    print ("\n \n POPULATION: Equal population criteria NOT satisfied with an overal range of " +
           str(overallRange) + ".")

pbar.update(25)
# Compactness
calculateCompactness()
total = 0
for ward in Wards:
    total += Wards[ward]["ppValue"]
avgPPValue = (total*1.0)/len(Wards)
print "COMPACTNESS: Average Polsby-Popper test value is " + \
    str(avgPPValue) + "."
pbar.update(25)
# Cohesion
print "COHESION:"
print "\t Average census block group splits is " + \
    str(calculateCohesion(blockGroups)) + "."
print "\t Average neighborhood splits is " + \
    str(calculateCohesion(neighborhoods)) + "."
print "\t Average park splits is " + str(calculateCohesion(parks)) + "."

# Minority criteria
print "MINORITY CRITERIA"
print "\t Minority criteria (6 wards) satisfied at 40%: " + \
    str(calculateMinority(40, 6, "Black_alon")) + "."
print "\t Minority criteria (6 wards) satisfied at 45%: " + \
    str(calculateMinority(45, 6, "Black_alon")) + "."
print "\t Minority criteria (6 wards) satisfied at 50%: " + \
    str(calculateMinority(50, 6, "Black_alon")) + "."
print "\t Minority criteria (6 wards) satisfied at 55%: " + \
    str(calculateMinority(55, 6, "Black_alon")) + "."
print "\t Minority criteria (7 wards) satisfied at 40%: " + \
    str(calculateMinority(40, 7, "Black_alon")) + "."
print "\t Minority criteria (7 wards) satisfied at 45%: " + \
    str(calculateMinority(45, 7, "Black_alon")) + "."
print "\t Minority criteria (7 wards) satisfied at 50%: " + \
    str(calculateMinority(50, 7, "Black_alon")) + "."
print "\t Minority criteria (7 wards) satisfied at 55%: " + \
    str(calculateMinority(55, 7, "Black_alon")) + "."

updatePopulations()
pbar.close()
