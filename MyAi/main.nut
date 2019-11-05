require("version.nut");


class MyAI extends AIController {
	towns_used = null;
	passenger_cargo_id = null;


	// Constructor for AI (there's a time limit on this)
	function constructor();
	// For things we want to initialise
	function Init();
	// Main driver
	function Start();
	// Required functions
	function Save();
	function Load(version, tbl);

	function FindAirportSpot(airportType, center_tile);
	function BuildAirport();
	
}

// Function to load required data
function MyAI::Init() {
	this.towns_used = AIList();
	// Get the id for passenger cargo
	local cargo = AICargoList();
	foreach (i in cargo) {
		if (AICargo.HasCargoClass(i, AICargo.CC_PASSENGERS)) {
			this.passenger_cargo_id = i;
			break;
		}
	}
	AICompany.SetLoanAmount(AICompany.GetMaxLoanAmount());
}

function MyAI::BuildAirport() {
	local airport_type = AIAirport.AT_SMALL;

	local tile_1 = this.FindAirportSpot(airport_type, 0);
	if (tile_1 < 0) {
		return -1;
	}
	local tile_2 = this.FindAirportSpot(airport_type, tile_1);
	if (tile_2 < 0) {
		this.towns_used.RemoveValue(tile_1)
		return -1;
	}
	AIAirport.BuildAirport(tile_1, airport_type, AIStation.STATION_NEW);
	AIAirport.BuildAirport(tile_2, airport_type, AIStation.STATION_NEW);
}

function MyAI::FindAirportSpot(airportType, center_tile) {
	// Airport specs
	local airport_x, airport_y, airport_rad;

	airport_x = AIAirport.GetAirportWidth(airportType);
	airport_y = AIAirport.GetAirportHeight(airportType);
	airport_rad = AIAirport.GetAirportCoverageRadius(airportType);

	// Get list of all towns
	local town_list = AITownList();
	// Remove towns already in use
	town_list.RemoveList(this.towns_used);
	
	foreach (town in town_list) {
		AILog.Info("Going to sleep");
		Sleep(1);

		local tile = AITown.GetLocation(town);

		local list = AITileList();

		list.AddRectangle(tile - AIMap.GetTileIndex(15, 15), tile + AIMap.GetTileIndex(15, 15));
		// Creates binary list where 1 is a tile where we can build an airport
		list.Valuate(AITile.IsBuildableRectangle, airport_x, airport_y);
		// Keep all tiles where we can build the airport
		list.KeepValue(1);
		// Check if we are already trying to build an airport at this spot
		if (center_tile != 0) {
			list.Valuate(AITile.GetDistanceSquareToTile, center_tile);
			list.KeepAboveValue(625);
		}
		list.Valuate(AITile.GetCargoAcceptance, this.passenger_cargo_id, airport_x, airport_y, airport_rad);
		list.RemoveBelowValue(10);

		// If failed to find a spot
		if (list.Count() == 0) {
			continue;
		} else {
			local test = AITestMode();
			local good_tile = 0;

			foreach (tiles in list) {
				// See if we can build the airport
				local location = AISign.BuildSign(tiles, "Trying to build an airport here");
				Sleep(100)
				AISign.RemoveSign(location);
				if (!AIAirport.BuildAirport(tiles, airportType, AIStation.STATION_NEW)) {
					continue;
				}
				good_tile = tiles;
				break;
			}
			if (good_tile == 0) {
				continue;
			}
		}
		AILog.Info("Found a spot to build an airport");
		this.towns_used.AddItem(town, tiles);
		return tiles;
	}
	return -1;
}

// Main Driver
function MyAI::Start() {

	this.Init();

	// Counter for current tick
	local counter = 0;
	while (true) {
		if (counter % 1000 == 0) {
			AILog.Info("Trying to build an airport");
			this.BuildAirport();
		}
		this.Sleep(100);
		counter += 100;
	}	
}

function MyAI::Save() {
	Log.Info("Saving data to savegame", Log.LVL_INFO);

	// In case (auto-)save happens before we have initialized all data,
	// save the raw _loaded_data if available or an empty table.
	if (!this._init_done) {
		return this._loaded_data != null ? this._loaded_data : {};
	}

	return { 
		some_data = null,
		//some_other_data = this._some_variable,
	};
}


function MyAI::Load(version, tbl) {
	Log.Info("Loading data from savegame made with version " + version + " of the game script", Log.LVL_INFO);

	// Store a copy of the table from the save game
	// but do not process the loaded data yet. Wait with that to Init
	// so that OpenTTD doesn't kick us for taking too long to load.
	this._loaded_data = {}
   	foreach(key, val in tbl) {
		this._loaded_data.rawset(key, val);
	}

	this._loaded_from_version = version;
}
