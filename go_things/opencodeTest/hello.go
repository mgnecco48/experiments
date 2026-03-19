package main

import (
	"fmt"
	"time"
)

func main() {
	lines := []string{
		"  _   _          _   _            __        __                 _       _ ",
		" | | | |   ___  | | | |   ___     \\ \\      / /   ___    _ __  | |   __| |",
		" | |_| |  / _ \\ | | | |  / _ \\     \\ \\ /\\ / /   / _ \\  | '__| | |  / _` |",
		" |  _  | |  __/ | | | | | (_) |     \\ V  V /   | (_) | | |    | | | (_| |",
		" |_| |_|  \\___| |_| |_|  \\___/       \\_/\\_/     \\___/  |_|    |_|  \\__,_||",
		"",
	}

	colors := []int{37, 33, 31, 33, 37}
	reset := "\033[0m"

	for frame := 0; frame < 60; frame++ {
		fmt.Print("\033[H\033[2J")
		for _, line := range lines {
			for i, r := range line {
				idx := (i + frame) % len(colors)
				fmt.Printf("\033[%dm%c%s", colors[idx], r, reset)
			}
			fmt.Println()
		}
		time.Sleep(100 * time.Millisecond)
	}
}
