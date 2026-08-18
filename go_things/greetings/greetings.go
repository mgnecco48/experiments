package greetings

import (
	"errors"
	"fmt"
)

func Greet(name string) (string, error) {
	message := fmt.Sprintf("Hello %v,\nNice to meet you!!!", name)
	if name == "" {
		return "", errors.New("Empty name")
	}
	return message, nil
}
