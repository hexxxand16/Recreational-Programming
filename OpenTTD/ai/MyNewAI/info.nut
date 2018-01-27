class MyNewAI extends AIInfo {
    function GetAuthor() {
        return "Newbie AI Writer";
    }
    
    function GetName() {
        return "MyNewAI";
    }

    function GetDescription() {
        return "An example AI by following the tutorial";
    }

    function GetVersion() {
        return 1;
    }

    function GetDate() {
        return "27/01/2018";
    }

    function CreateInstance() {
        return "MyNewAI";
    }

    function GetShortName() {
        return "XXXX";
    }

    function GetAPIVersion() {
        return "1.0";
    }
}

RegisterAI(MyNewAI());