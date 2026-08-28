package main

import (
	"fmt"
	"math/rand"
)

func main() {
	fmt.Print("Hello World\n")
	fmt.Println("hello", rand.Intn(10))

	small_list := []int{}
	fmt.Println("=====")

	for i := 0; i < 10; i++ {

		number := rand.Intn(10)

		small_list = append(small_list, number)
		fmt.Println(small_list[i])
	}

	fmt.Println(Sqrt(121))
	get_os()

	fmt.Println("===============")
	time_travel()

	fmt.Println("===============")

	fmt.Println(getTasks("http://127.0.0.1:8000/tasks"))
}
