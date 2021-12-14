using IPA;
using IPA.Config;
using IPA.Config.Stores;
using IPALogger = IPA.Logging.Logger;
using PPCounter.Settings;


namespace PPCounter
{
    [Plugin(RuntimeOptions.SingleStartInit)]
    public class Plugin
    {
        internal static Plugin Instance { get; private set; }
        internal static IPALogger Log { get; private set; }

        [Init]
        public void Init(Config conf, IPALogger logger)
        {
            Instance = this;
            Log = logger;
            PluginConfig.Instance = conf.Generated<PluginConfig>();
            
            Log.Info("[!] PPCounter initialized.");
        }

        [OnStart]
        public void OnApplicationStart() { }

        [OnExit]
        public void OnApplicationQuit() {  }
    }
}
