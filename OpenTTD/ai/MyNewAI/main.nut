class MyNewAI extends AIController {
    function Start();
}

function MyNewAI::Start() {
    while (true) {
        AILog.info("I am a very new AI with a ticker called MyNewAI and I am at tick " + this.GetTick());
        this.Sleep(50);
    }
}