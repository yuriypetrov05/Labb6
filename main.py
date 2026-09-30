class Track:
    def __init__(self, trackid, songid, artist, title):
        self.trackid = trackid
        self.songid = songid
        self.artist = artist
        self.title = title

    #inbyggad less than definerar vad som göra att ett Track-objekt är mindre än ett annan
    def __lt__(self, other):
        return self.artist < other.artist

def readfile(filename):
    track_list = []
    #utf-8 behövs
    with open(filename, "r", encoding="utf-8") as f:
        #Dela upp raderna vid <SEP>
        for line in f:
            parts = line.strip().split("<SEP>")
            if len(parts) == 4:
                #Skapa objekt och lägg till de i listan
                new_track = Track(parts[0], parts[1], parts[2], parts[3])
                track_list.append(new_track)
    return track_list
"""
1.)Parameter stmt = statement är funktionen som ska köras efter en tidsperiod
2.)Parameter number =  är hur många ggr koden i stmt ska köras.
timeit kör den flera ggr för att få rättvisande genomsnitt och undvika störningar
3.)Vad timeit tar tid på? = Den mäter "wall-lock time" och exkaverar koden number
4.)anropen timeit returnerar den totala tiden i sekunder (vilket är ett float)
"""
def linsok(lista, testartist):
    for track in lista:
        if track.artist == testartist:
            return True
    return  False
#Binärsök anpassad för Track-objekt
def binsok(lista, testartist):
    first = 0
    last = len(lista) - 1

    while first <= last:
        midpoint = (first + last) // 2
        if lista[midpoint].artist == testartist:
            return True
        elif testartist < lista[midpoint].artist:
            last = midpoint - 1
        else:
            first = midpoint + 1
    return False



#---Tidtagningskoden för sökning:---
import timeit

def main_search():
    filename = "unique_tracks.txt" # Eller unique_quarter.txt när du testar
    full_lista = readfile(filename)
    
    # Testa för olika n
    for n in [250000, 500000, 1000000]:
        if n > len(full_lista):
            break
            
        lista = full_lista[0:n]
        print(f"\n--- Antal element = {n} ---")
        
        # Vi väljer det sista elementet i listan att söka efter (Värsta fallet för linjärsökning!)
        sista = lista[-1]
        testartist = sista.artist
        
        # 1. Linjärsökning
        linjtid = timeit.timeit(stmt=lambda: linsok(lista, testartist), number=100)
        print("Linjärsökningen tog", round(linjtid, 4) , "sekunder (100 ggr)")
        
        # 2. Binärsökning (Kräver sorterad lista först!)
        lista_sorterad = sorted(lista)
        bintid = timeit.timeit(stmt=lambda: binsok(lista_sorterad, testartist), number=100)
        print("Binärsökningen tog", round(bintid, 4) , "sekunder (100 ggr)")
        
        # 3. Sökning i Hashtabell (Dictionary)
        # Vi bygger först upp hashtabellen (detta tar vi inte tid på under själva sökningen)
        hash_dict = {track.artist: track for track in lista}
        hashtid = timeit.timeit(stmt=lambda: testartist in hash_dict, number=100)
        print("Hashtabellsökningen tog", round(hashtid, 4) , "sekunder (100 ggr)")

# Kör med: main_search()

# Långsam metod (O(n^2))
def insertion_sort(lista):
    # Kopiera listan så vi inte ändrar originalet om vi vill sortera igen
    arr = lista.copy() 
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Snabb metod (O(n log n))
def merge_sort(lista):
    if len(lista) <= 1:
        return lista
        
    mid = len(lista) // 2
    left = merge_sort(lista[:mid])
    right = merge_sort(lista[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def main_sort():
    filename = "unique_tracks.txt"
    full_lista = readfile(filename)
    
    # Här varnar jag: Insertion sort kommer ta EXTREMT lång tid på 100 000 och 1 000 000. 
    # Du kommer antagligen bara vilja köra den för 1000 och 10 000.
    for n in [1000, 10000]: 
        lista = full_lista[0:n]
        print(f"\n--- Sortering Antal element = {n} ---")
        
        slow_time = timeit.timeit(stmt=lambda: insertion_sort(lista), number=1)
        print("Insertion Sort (Långsam) tog", round(slow_time, 4) , "sekunder")
        
        fast_time = timeit.timeit(stmt=lambda: merge_sort(lista), number=1)
        print("Merge Sort (Snabb) tog", round(fast_time, 4) , "sekunder")
        
        # Jämför även med Pythons inbyggda (som är Timsort - otroligt snabb)
        python_time = timeit.timeit(stmt=lambda: sorted(lista), number=1)
        print("Pythons inbyggda .sort() tog", round(python_time, 4) , "sekunder")

# Kör med: main_sort()
    