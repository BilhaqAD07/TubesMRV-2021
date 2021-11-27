from sys import exit
import numpy

# Fungsi ini digunakan untuk meng-input matriks dari file
# Edit isi file inputA.txt dan inputB.txt jika ingin mengedit matriks
def inputpersFile():
    x = numpy.loadtxt("bin\inputMatA.txt", dtype='f', delimiter=' ')
    y = numpy.loadtxt("bin\inputMatB.txt", dtype='f', delimiter=' ')
    return x, y

# Fungsi meng-input matriks dari Terminal
def inputpersManual():
    n = int(input("Input ukuran Matriks(n x n) : "))
    x = numpy.zeros((n,n), float)
    y = numpy.zeros(n, float)

    print("Input elemen Matriks A : ")
    for i in range(n):
        for j in range(n):
            x[i][j] = float(input("Koefisien x[%d][%d] -> " %(i,j)))

    print("Input elemen matriks B : ")
    for i in range(n):
        y[i] = float(input("Konstanta y[%d] - > " %(i)))

    return x, y

# Mendefinisikan fungsi memproses SPL eliminasi Gauss
def gauss():
    x, y = menuInput()
    n = len(y)  # Menentukan panjang dari inputan yang ada di variabel y
    A = numpy.column_stack((x,y))
    X = numpy.zeros(n, float)

    # Eliminasi dengan cara strategi pivoting
    for i in range(0, n):
        # Mengecek apakah ada kolom dengan nilai maks
        maksBaris = i
        maksEl1 = abs(A[i][i])

        for k in range(i+1, n):
            # Mengecek perbaris dan membangdingkannya dengan kondisi baris pertama tidak boleh bernilai 0
            if maksEl1 == 0 or abs(A[k][i]):
                maksBaris = k
                maksEl1 = abs(A[k][i])
        # Perulangan dibawah ini berfungsi dalam menukar baris terakhir dengan baris yang terdapat nilai 0 dengan dilakukan pengecekan kolom/kolom
        for k in range(i, n+1):
            temp = A[maksBaris][k]
            A[maksBaris][k] = A[i][k]
            A[i][k] = temp
        # Perulangan dibawah ini berfungsi untuk membuat baris yang dibawah 1 utama bernilai 0
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i != j:
                    A[k][j] += c*A[i][j]
                else:
                    A[k][j] = 0
    
    # Menemukan solusi dengan subtitusi mundur
    X = [0 for i in range (n)]
    for i in range(n-1, -1, -1):
        if A[i][i] != 0:
            X[i] = A[i][n]/A[i][i]
            for k in range(i-1, -1, -1):
                A[k][n] -= A[k][i]*X[i]
        else:
            return [0 for i in range(n)]
    x, y = numpy.hsplit(A, [n])
    return x, X

 # Mendefinisikan fungsi Gauss-Jordan
def gaussJordan():
    x, y = menuInput()
    n = len(y)

    for i in range(n):
        # Melakukan Pivoting dengan pengecekan baris ke bawah
        if numpy.fabs(x[i,i]) == 0:
            for j in range(i+1,n):
                if numpy.fabs(x[j,i]) > numpy.fabs(x[i,i]):
                    for k in range(i, n):
                        x[i,k], x[j.k] = x[j,k], x[i,k]
                    y[i], y[j] = y[j], y[i]
                    break

        pivot = x[i,i]
        for j in range(i, n):
            x[i, j] /= pivot
        y[i] /= pivot

        # Mulai Subtitusi
        for j in range(n):
            if j == i or x[j,i] == 0: continue
            faktor = x[j,i]
            for k in range(i,n):
                x[j, k] -= faktor * x[i,k]
            y[j] -= faktor * y[i]
    return x, y

def solusiHasil(A, B): # Fungsi ini diatur untuk mengecek apakah terdapat solusi banyak atau tidak ada solusi
    i = len(B)-1
    if numpy.all(numpy.isinf(B)):
        print("-----------------------")
        print("Hasil: Tidak ada Solusi")

        with open('bin\outputHasil.txt', 'a') as out:
            print("-----------------------", file = out)
            print("Hasil: Tidak ada Solusi", file = out)
        return

    elif numpy.all(numpy.isnan(B)):
        print("-----------------------")
        print(" Hasil: Solusi Banyak")

        with open('bin\hasil.txt', 'a') as out:
            print("-----------------------", file = out)
            print("Hasil: Solusi Banyak", file = out)
        return

    # Code dibawah ini akan berjalan apabila matriks ada solusi namun tidak solusi banyak
    print("Bentuk Matriks setelah di OBE : ")
    print(A)
    print()
    print("Matriks Hasil Eliminasi : ")
    for j in range(len(B)):
        print("x%d = %0.1f" %(j+1, B[j]) ,  end='\n')

    with open('bin\hasil.txt', 'ab') as out:
        numpy.savetxt(out,A,fmt='%0.1f',delimiter = ' ', header='Matrix A Setelah OBE : ')
        numpy.savetxt(out,B,fmt='%0.1f',delimiter = '\n', header='Hasil Eliminasi',footer='---------------------------------------------')

def mainMenu():
    print("--------- SELAMAT DATANG ---------")
    print("-      Gauss & Gauss-Jordan      -")
    print("-            Created By :        -")
    print("-      Bilhaq Avi Dewantara      -")
    print("-      Gery Melia Suwanda        -")
    print("-      Fadhilah Fauza Hamda      -")
    print("------- MENU UTAMA PROGRAM -------")
    print("-      [1]. SPL Gauss            -")
    print("-      [2]. SPL Gauss-Jordan     -")
    print("-      [99]. Keluar Program      -")
    print("----------------------------------")
    pilih = int(input("Pilihan Anda(1/2/99) : "))
    if pilih == 1:
        x, y = gauss()
    elif pilih == 2:
        x, y = gaussJordan()
    elif pilih == 99:
        print("Program berhenti, Terima Kasih:)")
        exit()
    else:
        print("Input Salah, Tolong Ulang Kembali..")
        mainMenu()
    return x, y

def menuInput():
    print("------ MENU INPUT PROGRAM ------")
    print("-   [1]. Input dari File       -")
    print("-   [2]. Input dari Terminal   -")
    print("-   [99]. Kembali ke Menu      -")
    print("--------------------------------")
    pilih = int(input("Pilihan Anda(1/2/99) : "))
    if pilih == 1:
        x, y = inputpersFile()
    elif pilih == 2:
        x, y = inputpersManual()
    elif pilih == 99:
        x, y = mainMenu()
    else:
        print("Silahkan Coba Lagi..")
        menuInput()
    return x, y
        

# Diibaratkan sebagai Fungsi main di C++, dengan memanggil fungsi" diatas
X, B = mainMenu()
solusiHasil(X, B)
