import pygame
import random
import time
import sys

WIDTH = HEIGHT = 500
screen = 0

def getShuffledContinousList(max):
    numbers = [i+1 for i in range(max)]
    random.shuffle(numbers)
    return numbers

def swapNumbers(list,pos1,pos2):
    temp = list[pos1]
    list[pos1] = list[pos2]
    list[pos2] = temp

def renderList(array):
    unitHeight = HEIGHT/len(array)
    barWidth = WIDTH/len(array)
    screen.fill((0,0,0))

    for i in range(0,len(array)):
        barHeight = unitHeight * array[i]
        pygame.draw.rect(screen,(255,255,255),(i*barWidth,HEIGHT-barHeight,barWidth,barHeight))

    pygame.display.flip()


def bubbleSort(array):
    swapped = True

    while swapped:
        swapped = False
        for i in range(len(array) -1):
            if array[i] > array[i+1]:
                swapNumbers(array,i,i+1)
                renderList(array)
                swapped = True

    return array

def insertionSort(array):
    for i in range(len(array)):
        j = i
        while j > 0 and array[j-1]>array[j]:
            swapNumbers(array,j,j-1)
            renderList(array)
            j -= 1

    return array

def selectionSort(array):
    for i in range(len(array)):
        min = i

        for j in range(i,len(array)):
            if array[j] < array[min]:
                min = j

        if not min == i:
            swapNumbers(array,min,i)
            renderList(array)

    return array

def quicksort(array,low,high):
    if low < high:
        pivot = array[high]

        i = low-1

        for j in range(low,high+1):
            if array[j] < pivot:
                i+=1
                swapNumbers(array,i,j)
                renderList(array)

        swapNumbers(array,i+1,high)
        renderList(array)

        pivot = i+1

        quicksort(array,low,pivot-1)
        quicksort(array,pivot+1,high)

    return array

def mergeSort(array,low,high):
    if low < high:
        middle = int((low+high)/2)
        mergeSort(array,low,middle)
        mergeSort(array,middle+1,high)

        i = 0
        j = 0
        merged = []
        left = array[low:middle+1]
        right = array[middle+1:high+1]

        #merge the arrays
        while(i < len(left) and j < len(right)):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        while(i < len(left)):
            merged.append(left[i])
            i += 1

        while(j < len(right)):
            merged.append(right[j])
            j += 1

        #put merged array back into array
        k=low
        for n in merged:
            renderList(array)
            array[k] = n
            k += 1


    return array

if __name__ == '__main__':

    itemCount = 0
    failed = False

    if len(sys.argv) < 3:
        print('enter all arguments')
        print('first argument: bubblesort, selectionsort, insertionsort, mergesort, quicksort')
        print('second argument: number of items to sort')
        failed = True
    else:
        try:
            itemCount = int(sys.argv[2])
        except ValueError:
            print('invalid second argument')
            failed = True

    if not failed:

        algorithm = sys.argv[1]

        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Sorting')
        background_colour = (0,0,0)
        screen.fill(background_colour)

        array = getShuffledContinousList(itemCount)

        if algorithm == 'bubblesort':
            bubbleSort(array)
        elif algorithm == 'selectionsort':
            selectionSort(array)
        elif algorithm == 'insertionsort':
            insertionSort(array)
        elif algorithm == 'mergesort':
            mergeSort(array,0,len(array)-1)
        elif algorithm == 'quicksort':
            quicksort(array,0,len(array)-1)
        else:
            print('invalid sorting algorithm')

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  running = False
