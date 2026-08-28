package main

import (
	"fmt"
)

func Sqrt(x float64) float64 {
	var z float64 = 1
	// this also works, and its more modern:
	// for i := range 10    or for range 10 (since we dont need to access i inside the loop)
	for i := 0; i < 10; i++ {
		fmt.Println(z)
		if (z * z) == x {
			return z
		} else {
			z -= (z*z - x) / (2 * z)
		}

	}
	return z
}
