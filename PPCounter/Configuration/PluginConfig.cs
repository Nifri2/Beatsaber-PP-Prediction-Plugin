using System.Runtime.CompilerServices;
using IPA.Config.Stores;

[assembly: InternalsVisibleTo(GeneratedStore.AssemblyVisibilityTarget)]
namespace PPCounter.Settings
{
    internal class PluginConfig
    {
        public static PluginConfig Instance { get; set; }
        public virtual bool ppBuildsUp { get; set; } = false;
        public virtual int port { get; set; } = 5000;
    }
}
