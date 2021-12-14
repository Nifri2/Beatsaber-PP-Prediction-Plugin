using System;
using System.Threading.Tasks;
using UnityEngine;
using SongDetailsCache;
using SongDetailsCache.Structs;


namespace PPCounter.Util
{
    class Utilities
    {
        private Model modelHandler = new Model();
        private SongArray songArr;
        private SongDetails songDetails;

        public int Notes { get; set; }
        public float Stars { get; set; }

        internal Utilities() { }

        //also gets notes and stars lol
        public bool GetRanked(string hash, string diff)
        {
            if(songDetails == null) {
                this.songDetails = SongCache().Result;
                this.songArr = songDetails.songs; }
            songArr.FindByHash(hash, out var song);

            song.GetDifficulty(out var difficulty, GetDifficulty(diff));
            Stars = difficulty.stars;
            Notes = (int)difficulty.notes; 


            var rankedStatus = song.rankedStatus;
            Debug.Log("[!]PPCounter: RANKED STATUS = " + rankedStatus.ToString());
            switch (rankedStatus)
            {
                case RankedStatus.Unranked:
                    return false;
                case RankedStatus.Ranked:
                    return true;
                case RankedStatus.Qualified:
                    return true;
                default:
                    return false;
            }
        }

        public decimal GetPP(decimal acc)
        {
            return modelHandler.Request(acc, Stars);
        }

        public string GetHash(string ID)
        {
            var split = ID.Split('_');
            return split[2];
        }

        public MapDifficulty GetDifficulty(string diff)
        {
            switch (diff)
            {
                case "Easy":
                    return MapDifficulty.Easy;
                case "Normal":
                    return MapDifficulty.Normal;
                case "Hard":
                    return MapDifficulty.Hard;
                case "Expert":
                    return MapDifficulty.Expert;
                case "ExpertPlus":
                    return MapDifficulty.ExpertPlus;
                case "Expert+":
                    return MapDifficulty.ExpertPlus;
                default:
                    throw new UnknownDifficulty();
            }
        }

        private Task<SongDetails> SongCache()
        {
            var songDetails = SongDetails.Init();
            return songDetails;
        }
    }
    class UnknownDifficulty : Exception
    {
        public UnknownDifficulty()
        {
            Debug.LogError("Unknown Difficulty");
        }
    }
}
