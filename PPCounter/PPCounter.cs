using System;
using CountersPlus.Counters.Custom;
using PPCounter.Util;
using TMPro;
using PPCounter.Settings;
using CountersPlus.Counters.Interfaces;

namespace PPCounter
{
    class PPCounter : BasicCustomCounter, INoteEventHandler, IScoreEventHandler
    {
        private GameplayCoreSceneSetupData gameplayCoreScene;
        private Utilities ppUtils = new Utilities();
        private TMP_Text counter;

        private int score = 1;
        private int maxScore = 1;
        private bool IsRanked;

        internal PPCounter(GameplayCoreSceneSetupData gameplayCoreScene)
        {
            this.gameplayCoreScene = gameplayCoreScene;
        }

        public override void CounterInit()
        {
            IDifficultyBeatmap diff = gameplayCoreScene.difficultyBeatmap;
            IBeatmapLevel level = diff.level;
            var diffName = diff.difficulty.Name();
            var hash = ppUtils.GetHash(level.levelID);
            this.IsRanked = ppUtils.GetRanked(hash, diffName);
            if (!IsRanked) { return; }

            counter = CanvasUtility.CreateTextFromSettings(Settings);
            counter.fontSize = 3;
            UpdateText(0);
        }

        public void UpdateText(decimal val)
        {
            counter.text = Math.Round(val, 2).ToString() + "pp";
        }

        public override void CounterDestroy() {  }

        public void OnNoteCut(NoteData data, NoteCutInfo info)
        {
            if (!IsRanked) { return; }
            if (!PluginConfig.Instance.ppBuildsUp) {
                var valF = ((float)score / maxScore) * 100;
                var valD = Math.Round((decimal)valF, 2);
                UpdateText(ppUtils.GetPP(valD));
            }
            else {
                var valF = (float)score / ((ppUtils.Notes * 115) * 8);
                var valD = Math.Round((decimal)valF, 2);
                UpdateText(ppUtils.GetPP(valD));
            }
        }

        public void OnNoteMiss(NoteData data){  }

        public void ScoreUpdated(int modifiedScore) { score = modifiedScore; }

        public void MaxScoreUpdated(int maxModifiedScore) { maxScore = maxModifiedScore; }
    }
}
