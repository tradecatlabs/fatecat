package main

import (
	"fmt"
	"net/http"

	bazi "github.com/warrially/BaziGo"
)

type Myhandler struct{}

// HTTP 版本

func main() {
	http.HandleFunc("/", IndexHandler)
	http.ListenAndServe(":7890", nil)
}
func IndexHandler(w http.ResponseWriter, _ *http.Request) {
	pBazi := bazi.GetBazi(1995, 6, 16, 19, 7, 0, 0)
	fmt.Fprintln(w, pBazi.ToHTML())
}
