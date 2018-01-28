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
        refineries.Valuate(AIIndustry.GetDistanceManhattanToTile, AIIndustry.GetLocation(MyRig));
        refineries.Sort(AIList.SORT_BY_VALUE, true);
        local myRef = refineries.Begin();
        AISign.BuildSign(AIIndustry.GetLocation(myRef), "destination");
    }
}