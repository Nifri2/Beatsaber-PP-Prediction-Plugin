package main

import (
	_ "embed"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"strconv"

	"github.com/gorilla/mux"
)

//go:embed fixed.csv
var fContent string

type pp struct {
	PP   string `json:"pp"`
	Meta data   `json:"meta"`
}

type data = struct {
	Stars  float64   `json:"stars"`
	Acc    float64   `json:"acc"`
	Params urlparams `json:"params"`
}

type urlparams struct {
	Stars string     `json:"stars"`
	Acc   string     `json:"acc"`
	All   url.Values `json:"all"`
}

var lookupTable map[string][]map[string]string

func predict_endpoint(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := r.URL.Query()
	urlparams := urlparams{
		params["stars"][0],
		params["acc"][0],
		params,
	}
	stars, err := strconv.ParseFloat(urlparams.Stars, 32)
	if err != nil {
		log.Fatal(err)
	}

	acc, err := strconv.ParseFloat(urlparams.Acc, 32)
	if err != nil {
		log.Fatal(err)
	}

	data := data{
		stars,
		acc,
		urlparams,
	}
	prediction := predict(data)
	log.Print(r.Method, r.URL, prediction)

	json.NewEncoder(w).Encode(prediction)
}

func predict(d data) pp {
	var prediction string
	for _, v := range lookupTable[d.Params.Stars] {
		if _, ok := v[d.Params.Acc]; ok {
			prediction = v[d.Params.Acc]
			break
		}
	}
	i, _ := strconv.ParseFloat(prediction, 32)
	prediction = strconv.FormatFloat(i, 'f', 2, 64)
	return pp{
		PP:   prediction,
		Meta: d,
	}
}

func routes(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "{\"message\":\"Welcome home great slayer\"}")
}

func loadData() map[string][]map[string]string {
	file, err := os.Open("dataset.csv")
	if err != nil {
		log.Fatal(err)
	}
	reader := csv.NewReader(file)
	reader.Comma = ';'
	records, err := reader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	csvdata := map[string][]map[string]string{}
	for i, v := range records {
		if i == 0 {
			continue
		}
		val, err := strconv.ParseFloat(v[1], 32)
		if err != nil {
			log.Fatal(err)
		}
		va := strconv.FormatFloat(val, 'f', 2, 64)

		if _, ok := csvdata[string(v[0])]; ok {
			csvdata[string(v[0])] = append(csvdata[string(v[0])], map[string]string{
				va: string(v[2]),
			})
		} else {
			csvdata[string(v[0])] = []map[string]string{}
		}
	}
	log.Print("Loaded " + strconv.Itoa((len(csvdata))) + " Features")
	return csvdata
}

func dumpCSV() {
	var check bool = false
	files, err := ioutil.ReadDir("./")
	if err != nil {
		log.Fatal(err)
	}

	for _, f := range files {
		if f.Name() == "dataset.csv" {
			check = true
		}
	}

	if !check {
		log.Print("No dataset file found, dumping...")
		err := ioutil.WriteFile("dataset.csv", []byte(fContent), 0777)
		if err != nil {
			log.Fatal(err)
		}
	}
}

func main() {
	log.Print("Starting PP Predict API....")
	dumpCSV()
	lookupTable = loadData()
	log.Print("Lets go!")

	router := mux.NewRouter().StrictSlash(true)

	router.HandleFunc("/predict", predict_endpoint)
	router.HandleFunc("/", routes)
	log.Fatal(http.ListenAndServe(":8080", router))
}
