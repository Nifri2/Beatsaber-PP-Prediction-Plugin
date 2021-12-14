using System;
using System.Net;
using PPCounter.Settings;

namespace PPCounter.Util
{
    class Model
    {
        private string URL = "http://127.0.0.1:{port}/predict".Replace("{port}", PluginConfig.Instance.port.ToString());
        private string json = @"{ ""stars"": {stars}, ""acc"": {acc} }";
        private WebClient wc = new WebClient();

        internal Model() { }

        public decimal Request(decimal acc, float stars)
        {
            wc.Headers[HttpRequestHeader.ContentType] = "application/json";
            string response = wc.UploadString(URL, json.Replace("{stars}", stars.ToString()).Replace("{acc}", acc.ToString()));
            var a = response.Split(' ', '}');
            return Convert.ToDecimal(a[1]);
        }
    }
}
