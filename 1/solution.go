package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func stringToNumber(s string) string {
	switch s {
	case "one":
		return "1"
	case "two":
		return "2"
	case "three":
		return "3"
	case "four":
		return "4"
	case "five":
		return "5"
	case "six":
		return "6"
	case "seven":
		return "7"
	case "eight":
		return "8"
	case "nine":
		return "9"
	default:
		return s
	}
}

func solve(regex string) int {
	file, _ := os.Open("input")
	scanner := bufio.NewScanner(file)
	r, _ := regexp.Compile(regex)

	var calibrationLibrary = 0
	for scanner.Scan() {
		lineValues := r.FindAllString(scanner.Text(), -1)
		var secondIdx = 0
		for i, value := range lineValues {
			lineValues[i] = stringToNumber(value)
		}
		if len(lineValues) > 1 {
			secondIdx = len(lineValues) - 1
		}
		var curValue, _ = strconv.Atoi(lineValues[0] + lineValues[secondIdx])
		calibrationLibrary += curValue
	}
	return calibrationLibrary
}
func main() {
	fmt.Println("First part: ", solve((`(\d){1}`)))
	fmt.Println("Second part: ", solve((`(one|two|three|four|five|six|seven|eight|nine|\d)`)))
}
