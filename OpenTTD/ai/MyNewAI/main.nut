class MyNewAI extends AIController {
    function Start();
}

function MyNewAI::Start() {
    while (true) {
        local cargos = AICargoList();
        local oil;
        foreach (cargo, value in cargos) {
            if (AICargo.GetCargoLabel(cargo) == "OIL_") {
                oil = cargo;
                break;
            }
        }
        local oilrigs = AIIndustryList_CargoProducing(oil);
        oilrigs.Valuate(AIIndustry.HasDock);
        oilrigs.KeepValue(1);

        oilrigs.Valuate(AIIndustry.GetLastMonthProduction, oil);
        local myRig = oilrigs.Begin();
        AISign.BuildSign(AIIndustry.GetLocation(myRig), "origin");

        local refineries = AIIndustryList_CargoAccepting(oil);
        refineries.Valuate(AIIndustry.GetDistanceManhattanToTile, AIIndustry.GetLocation(myRig));
        refineries.Sort(AIList.SORT_BY_VALUE, true);
        local myRef = refineries.Begin();
        AISign.BuildSign(AIIndustry.GetLocation(myRef), "destination");

        local myDock = this.BuildDock(myRef);
        local buoys = this.BuildBuoy(myDock, myRig);
    }
}

function MyNewAI::BuildDock(industry) {
    local dockLocation;
    local accepting = AITileList_IndustryAccepting(industry, 4);

    accepting.Valuate(AITile.IsCoastTile);
    accepting.KeepValue(1);

    foreach (myTile, value in accepting) {
        local slope = AITile.GetSlope(myTile);
        if (AIMarine.BuildDock(myTile, AIStation.STATION_NEW)) {
            dockLocation = myTile;
            break;
        }
    }
}

function MyNewAI::BuildBuoys(dock, rig) {
    local rigStation = AIIndustry.GetDockLocation(myRig);
    local distance = AIMap.DistanceMax(dock, rigStation);
    AILog.Info("Two stations are " + distance + " tiles apart.");

    local xDistance = AIMap.GetTileX(rigStation) - AIMap.GetTileX(dock);
    local yDistance = AIMap.GetTileY(rigStation) - AIMap.GetTileY(dock);
    AILog.Info("X distance: " + xDistance);
    AILog.Info("Y distance: " + yDistance);

    local numSegments = distance / 20;
    local xSegSize = xDistance / numSegments;
    local ySegSize = yDistance / numSegments;
    AILog.Info("X segment size: " + xSegSize);
    AILog.Info("Y segment size: " + ySegSize);

    local buoys = AIlist();
    local xLoc = AIMap.GetTileX(dock);
    local yLoc = AIMap.GetTileY(dock);
    for (local i = 0; i < numSegments; i++) {
        xLoc = xLoc + xSegSize;
        yLoc = yLoc + ySegSize;
        local tile = AIMap.GetTileIndex(xLoc, yLoc);
        local buoy = this.BuildBuoy(xLoc, yLoc);
        if (buoy) {
            buoys.AddItem(buoy, 0)
        }
    }
    return buoys;    
}

function MyNewAI::BuildBuoy(x, y) {
    local tile = AIMap.GetTileIndex(x, y);
    if (AIMarine.BuildBuoy(tile)) {
        return AIWaypoint.GetWaypointID(tile);
    } else {
        return false;
    }
}