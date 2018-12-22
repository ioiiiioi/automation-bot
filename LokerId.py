"""
program ini merupakan aplikasi bot sederhana yang bertujuan untuk mengumpulkan data lowongan pekerjaan dari web Loker.id.
data yang dikumpulkan akan disimpan terlebih dahulu pada fitur Bookmark Loker.id agar tidak diperlukan membuat database.
setelah data tersimpan, bot akan melakukan apply pada lowongan tersebut secara otomatis.
untuk menjalankanya, diperlukan driver geckowebdriver yang terinstall pada OS.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql as db
import time
import random

#---------------------------------------------------------------------
#https://www.loker.id/cari-lowongan-kerja?q=backend+developer&lokasi=0&category=information-technology&pendidikan=sarjana-s1
class KarirID:   

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closeBrowser(self):
        self.driver.close()

    def koneksi():
        conn = db.connect('localhost', 'root', '', 'test_rest_api')
        cur = conn.cursor()
        return conn, cur

    def login(self):
        try:
            driver = self.driver
            driver.get("https://www.loker.id/login")                        
            time.sleep(2)
            user_name_elem = driver.find_element_by_xpath("//input[@name='acf[field_574b31195165b]']")
            user_name_elem.clear()
            user_name_elem.send_keys(self.username)
            password_elem = driver.find_element_by_xpath("//input[@name='acf[field_574b311951bc8]']")
            password_elem.clear()
            password_elem.send_keys(self.password)
            password_elem.send_keys(Keys.RETURN)  
            time.sleep(2)
        except Exception:
            print("ada yang salah nih di login")

    def cari_kerja(self):
        driver = self.driver        
        driver.get("https://www.loker.id/cari-lowongan-kerja?q=&lokasi=0&category=information-technology&pendidikan=sarjana-s1")
        #----------------------------Untuk Page 1---------------------------------
        for i in range(2,11):
            try:                
                tombol_simpan = driver.find_element_by_xpath("//html/body/div[2]/div/div[2]/div/div["+ str(i) +"]/div[2]/div[2]")
                
                tombol_simpan.click()                
                time.sleep(random.randint(1,4))                
                tombol_verif = driver.find_element_by_xpath("//html/body/div[6]/div[7]/div/button")
                tombol_verif.click()
                print("Berhasil Di Bookmark")
                
            except Exception:
                print("sudah di bookmark")
                continue
        #----------------------------Untuk Page 2 - 18 ---------------------------------   
        for j in range(2,19):
            try:
                driver.get("https://www.loker.id/cari-lowongan-kerja/page/"+ str(j) +"?q&lokasi=0&category=information-technology&pendidikan=sarjana-s1")
                for k in range(2,11):
                    try:
                        tombol_simpan = driver.find_element_by_xpath("//html/body/div[2]/div/div[2]/div/div["+ str(k) +"]/div[2]/div[2]")               
                        tombol_simpan.click()                
                        time.sleep(random.randint(1,4))                
                        tombol_verif = driver.find_element_by_xpath("//html/body/div[6]/div[7]/div/button")
                        tombol_verif.click()
                        print("Berhasil Di Bookmark")
                    except Exception:
                        print("sudah di bookmark")
                        continue
            except Exception:
                print("ada yang salah")
                continue

    def book(self):
        deskripsi_diri = "deskripsi diri anda"
        driver = self.driver
        driver.get("https://www.loker.id/bookmark")
        halaman_lowongan = []
        #----------------------------Untuk Page 1---------------------------------
        for i in range(1,11):
            try:
                simpan_halaman_loker = driver.find_element_by_xpath("//html/body/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr["+ str(i) +"]/td[1]/h5/a")
                link_halaman = simpan_halaman_loker.get_attribute('href')
                halaman_lowongan.append(link_halaman)
                #print("Link loker ke-"+ str(i) + "ialah" + halaman_lowongan[i])
            except Exception:
                print("ada yang salah di rekursif saat mengambil link halaman")

        #print(halaman_lowongan)

        for j in range(0,len(halaman_lowongan)):
            driver.get(halaman_lowongan[j])
            
            try:
                button_lamar_pekerjaan=driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[3]/a")
                button_lamar_pekerjaan.click()
            except Exception:
                print("Lamaran telah dikirim sebelumnya")
                continue
            time.sleep(5)
            #pilih_resume = driver.find_element_by_xpath("//html/body/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[3]/div/div/div/form/div[1]/div[3]/div[1]/div[2]/div/a")
            pilih_resume = driver.find_element_by_xpath("//html/body/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[3]/div/div/div/form/div[1]/div[3]/div[1]/div[2]/span/span[1]/span/span[2]")
            pilih_resume.click()
            time.sleep(3)
            
            #-------------Opsional 1-----------------------------
            """
            resum = driver.find_element_by_xpath("//input[@id='s2id_autogen1_search']")                        
            resum.send_keys("nama reseume anda")
            resum.send_keys(Keys.ENTER)
            """
            
            #------------Opsional 2------------------------------------
            resum = driver.find_element_by_xpath("//ul[@id='select2-acf-field_57a6d61c2671c-results']")
            resum.click()

            deskrip = driver.find_element_by_xpath("//textarea[@id='acf-field_57af7454a90bf']")
            deskrip.send_keys(deskripsi_diri)
            #time.sleep(10)
            button_kirim = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[3]/div/div/div/form/div[2]/button[2]")
            button_kirim.click()
            print("lamaran " +str(j)+" Berhasil di kirim")
            
        for k in range(0,len(halaman_lowongan)):
            try:
                time.sleep(1)
                del halaman_lowongan[0]

            except Exception:
                print("Error saat menghapus list halaman_lowongan" + str(k))

                
        #----------------------------Untuk Page 2 Dst---------------------------------
        for x in range(2,99):
            try:
                driver.get("https://www.loker.id/bookmark/page/"+str(x))
                print("=================================Halaman "+str(x)+"===========================")        
                print("    ")    
                for i in range(1,11):
                    try:
                        simpan_halaman_loker = driver.find_element_by_xpath("//html/body/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr["+ str(i) +"]/td[1]/h5/a")
                        link_halaman = simpan_halaman_loker.get_attribute('href')
                        halaman_lowongan.append(link_halaman)
                        #print("Link loker ke-"+ str(i) + "ialah" + halaman_lowongan[i])
                    except Exception:
                        print("ada yang salah di rekursif saat mengambil link halaman")
                        break

                #print(halaman_lowongan)

                for j in range(0,len(halaman_lowongan)):
                    driver.get(halaman_lowongan[j])
                    
                    try:
                        button_lamar_pekerjaan=driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[3]/a")
                        button_lamar_pekerjaan.click()
                    except Exception:
                        print("Lamaran telah dikirim sebelumnya")
                        continue
                    try:
                        #pilih_resume = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[3]/div/div/div/form/div[1]/div[3]/div[1]/div[2]/div/a")
                        pilih_resume = driver.find_element_by_xpath("//html/body/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[3]/div/div/div/form/div[1]/div[3]/div[1]/div[2]/span/span[1]/span/span[2]")
                        pilih_resume.click()
                        time.sleep(3)
                        
                        #-------------Opsional 1-----------------------------
                        """
                        resum = driver.find_element_by_xpath("//input[@id='s2id_autogen1_search']")                        
                        resum.send_keys("nama resume anda")
                        resum.send_keys(Keys.ENTER)
                        """
                        
                        #------------Opsional 2------------------------------------
                        resum = driver.find_element_by_xpath("//ul[@id='select2-acf-field_57a6d61c2671c-results']")
                        resum.click()

                        deskrip = driver.find_element_by_xpath("//textarea[@id='acf-field_57af7454a90bf']")
                        deskrip.send_keys(deskripsi_diri)
                        #time.sleep(10)
                        button_kirim = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[3]/div/div/div/form/div[2]/button[2]")
                        button_kirim.click()
                        print("lamaran " +str(j)+" Berhasil di kirim")
                    except Exception:
                        print("ada yang salah dimari")
                        break

                for y in range(0,len(halaman_lowongan)):
                    try:
                        time.sleep(1)
                        del halaman_lowongan[0]                        
                    except Exception:                        
                        print("Error saat menghapus list halaman_lowongan bagian 2 dst")
            except Exception:
                print("Halaman udah habis")
                break

Nama = 'Masukkan Nama resume anda disini'
User_anda = 'Masukkan username akun karir.id anda di sini'
Pass_anda = 'Masukkan password akun karir.id anda di sini'
akun = KarirID(User_anda, Pass_anda)
akun.login()
akun.book()
akun.cari_kerja()




