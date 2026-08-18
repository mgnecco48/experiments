package main

import (
	"charm.land/lipgloss/v2"
	"example.com/greetings"
	// "fmt"
)

func main() {
	message := greetings.Greet("")

	var style = lipgloss.NewStyle().
		Bold(true).
		Italic(true).
		Blink(true).
		Foreground(lipgloss.BrightBlack).
		Background(lipgloss.BrightYellow).
		PaddingTop(1).
		PaddingBottom(1).
		PaddingRight(1).
		PaddingLeft(1)

	lipgloss.Println(style.Render(message))

}
