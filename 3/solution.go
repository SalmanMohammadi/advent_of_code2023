package main

import (
	"fmt"
	"os"
	"regexp"
	"slices"
	"strconv"
	"strings"
)

var lineLength = 0
var numLines = 0

func clipToLine(y int) int {
	return min(max(0, y), lineLength-1)
}

func convertIndexToOneD(i int, j int) int {
	return (lineLength * i) + j
}

func convertIndexToTwoD(i int) (int, int) {
	return i / lineLength, i % lineLength
}

func getPartAdjacencyIndexes(start int, end int) []int {
	// numbers aren't going to span multiple lines, so we can fix i
	i, startJ := convertIndexToTwoD(start)
	_, endJ := convertIndexToTwoD(end)

	// this could be a map instead, so we don't duplicate for corner cases,
	// but added code complexity not worth.
	var idxs []int
	// add diagonals
	idxs = append(idxs, convertIndexToOneD(min(i+1, numLines-1), min(endJ+1, lineLength-1)))
	idxs = append(idxs, convertIndexToOneD(max(i-1, 0), min(endJ+1, lineLength-1)))

	idxs = append(idxs, convertIndexToOneD(min(i+1, numLines-1), max(startJ-1, 0)))
	idxs = append(idxs, convertIndexToOneD(max(i-1, 0), max(startJ-1, 0)))
	// add horizontals
	idxs = append(idxs, convertIndexToOneD(i, max(startJ-1, 0)))
	idxs = append(idxs, convertIndexToOneD(i, min(endJ+1, lineLength)))
	// add vertical indexes directly above and blow
	// this is wasteful for edge cases (worst cases are corner numbers)
	for j := startJ; j <= endJ; j++ {
		idxs = append(idxs, convertIndexToOneD(min(i+1, numLines-1), j))
		idxs = append(idxs, convertIndexToOneD(max(i-1, 0), j))
	}
	return idxs
}

func getGearAdjacencyIndexes(idx int) []int {
	// index should be the starting position of the gear
	// numbers aren't going to span multiple lines, so we can fix i
	i, j := convertIndexToTwoD(idx)
	var idxs []int
	// add top row
	idxs = append(idxs, convertIndexToOneD(min(i-1, numLines-1), max(j-3, 0)))

	// middle row
	idxs = append(idxs, convertIndexToOneD(i, max(j-3, 0)))
	// idxs = append(idxs, convertIndexToOneD(i, min(j+1, lineLength)))

	// add bottom row
	idxs = append(idxs, convertIndexToOneD(max(i+1, 0), max(j-3, 0)))

	// sort for left-to-right search
	slices.Sort(idxs)
	return idxs
}

func solvePartOne() int {
	dat, _ := os.ReadFile("input")
	data := string(dat)
	dataSplit := strings.Split(data, "\n")
	lineLength = len(dataSplit[0])
	numLines = len(dataSplit)

	data = strings.Replace(data, "\n", "", -1)
	regexNumbers, _ := regexp.Compile(`(\d+)`)
	regexSymbols, _ := regexp.Compile(`[^a-zA-Z0-9\s\.]`)
	idxs := regexNumbers.FindAllStringIndex(data, -1)
	var partTotal int = 0
	for _, ids := range idxs {
		for _, adjacentId := range getPartAdjacencyIndexes(ids[0], ids[1]-1) {
			if regexSymbols.MatchString(string(data[adjacentId])) {
				partNumber, _ := strconv.Atoi(string(data[ids[0]:ids[1]]))
				partTotal += partNumber
				break
			}
		}
	}
	return partTotal
}

func solvePartTwo() int {
	dat, _ := os.ReadFile("input")
	data := string(dat)
	dataSplit := strings.Split(data, "\n")
	lineLength = len(dataSplit[0])
	numLines = len(dataSplit)
	fmt.Println("lenl, len", lineLength, numLines)
	data = strings.Replace(data, "\n", "", -1)
	// regexParts, _ := regexp.Compile(`(\d{3})`)
	regexGears, _ := regexp.Compile(`\*`)
	idxs := regexGears.FindAllStringIndex(data, -1)
	var totalGearRatios int = 0
GearLoop:
	for _, ids := range idxs {
		// fmt.Println("gear id", idxs[0])
		var validParts []int
		adjacentIdxs := getGearAdjacencyIndexes(ids[0])
	AdjacentLoop:
		for _, adjacentId := range adjacentIdxs {

			// adjacentI, adjacentJ := convertIndexToTwoD(adjacentId)
			// adjacentParts := map[int]bool{}
			// fmt.Println(adjacentId, max(adjacentId-3, 0), min(adjacentId+3, lineLength-1), clipToLine(adjacentId-3), clipToLine(adjacentId+3)) //, data[max(adjacentId-3, 0):min(adjacentId+3, lineLength-1)])
			// matched, _ := regexParts.MatchString(data[adjacentId-3 : adjacentId+3])

			x, y := convertIndexToTwoD(adjacentId)
			// fmt.Println("cur id", x, y)
		RowLoop:
			for i := 0; i <= 4; i++ {
				for j := 3; j >= 1; j-- {
					// fmt.Println("i", i, "j", j, y, data[convertIndexToOneD(x, clipToLine(y+i)):convertIndexToOneD(x, clipToLine(y+i+j))])
					if num, err := strconv.Atoi(string(data[convertIndexToOneD(x, clipToLine(y+i)):convertIndexToOneD(x, clipToLine(y+i+j))])); err == nil {
						// fmt.Println("found valid part", num, i)
						validParts = append(validParts, num)
						if i == 0 || ((i == 1) && (len(strconv.Itoa(num)) == 2)) {
							i += 2
							continue RowLoop
						}
						if i <= 2 {
							i++
							continue RowLoop
						}
						continue AdjacentLoop
					} else {
						if (i < 1) || (i == 1) && j <= 2 {
							continue RowLoop
						}
					}
				}
			}
		}
		if len(validParts) != 2 {
			continue GearLoop
		}
		fmt.Println("validparts", validParts, len(validParts))
		var gearTotal int = 1
		for _, partNumber := range validParts {
			gearTotal *= partNumber
		}
		totalGearRatios += gearTotal

	}
	return totalGearRatios
}

func main() {
	fmt.Println("First part: ", solvePartOne())
	// fmt.Println("Second part: ", solvePartTwo())
	// 84883664
}
