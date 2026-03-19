package main

import "fmt"

import "github.com/common-nighthawk/go-figure"

func saludar(name string) {
	fmt.Println("Hola Mundo!!")
	message := fmt.Sprintf("Hello, %s!", name)
	ascii := figure.NewColorFigure(message, "larry3d", "purple", true)
	ascii.Print()
}

func main() {
	saludar("Martin")
}

