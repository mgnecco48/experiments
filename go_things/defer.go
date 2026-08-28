package main

import (
	"fmt"
	"time"
)

func time_travel() {

	first := func() int {
		first := time.Now().Nanosecond()
		return first
	}
	second := func() int {
		second := time.Now().Nanosecond()
		return second
	}

	fmt.Printf("This should be first: %v, its of type %T\n", first(), first())
	time.Sleep(time.Second)
	fmt.Printf("This should be second: %v, its of type %T\n", second(), second())

}
