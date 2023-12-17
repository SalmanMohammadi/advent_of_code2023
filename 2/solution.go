package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func solve_part_one() int {
	file, _ := os.Open("input")
	scanner := bufio.NewScanner(file)
	var gameIDTotal = 0
	var colourMap = map[string]int{
		"red":   12,
		"green": 13,
		"blue":  14,
	}
out:
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ":")
		gameID, _ := strconv.Atoi(strings.Split(line[0], " ")[1])
		var sets = strings.Split(line[1], ";")
		for _, set := range sets {
			for colour, colourMax := range colourMap {
				if i := strings.Index(set, colour); i > -1 {
					colourCount, _ := strconv.Atoi(strings.Replace(set[i-3:i], " ", "", -1))
					if colourCount > colourMax {
						continue out
					}
				}
			}

		}
		gameIDTotal += gameID
	}
	return gameIDTotal
}

func solve_part_two() int {
	file, _ := os.Open("input")
	scanner := bufio.NewScanner(file)
	var powerTotal = 0
	var colourMap = map[string]int{
		"red":   12,
		"green": 13,
		"blue":  14,
	}
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ":")
		var sets = strings.Split(line[1], ";")
		var maxCubes = map[string]int{
			"red":   0,
			"green": 0,
			"blue":  0,
		}
		for _, set := range sets {
			for colour, _ := range colourMap {
				if i := strings.Index(set, colour); i > -1 {
					colourCount, _ := strconv.Atoi(strings.Replace(set[i-3:i], " ", "", -1))
					if colourCount > maxCubes[colour] {
						maxCubes[colour] = colourCount
					}
				}
			}

		}
		var minimumPower = 1
		for _, colourCount := range maxCubes {
			minimumPower *= colourCount
		}
		powerTotal += minimumPower
	}
	return powerTotal
}
func main() {
	fmt.Println("First part: ", solve_part_one())
	fmt.Println("Second part: ", solve_part_two())

}
