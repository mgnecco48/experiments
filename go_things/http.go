package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

func getTasks(url string) string {
	c := &http.Client{Timeout: 10 * time.Second}
	resp, err := c.Get(url)
	if err != nil {
		fmt.Println("Something went wrong")
		os.Exit(1)
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Could not read response body")
		os.Exit(1)
	}

	return string(body)
}
