from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pymysql as db
import time



class tiaJobs:

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.driver = webdriver.Firefox()
	
	def closeBrowser(self):
		self.driver.close()

	def login(self):
		driver = self.driver

		driver.get("https://www.techinasia.com/login")
		uname_element = driver.find_element_by_xpath("//div/div[4]/div/div/div/div/div[2]/form/input")
		uname_element.clear()
		uname_element.send_keys(self.username)
		pass_element = driver.find_element_by_xpath("//div/div[4]/div/div/div/div/div[2]/form/div/input")
		pass_element.clear()
		pass_element.send_keys(self.password)
		pass_element.send_keys(Keys.RETURN)

	def scrapJobs(self):
		driver = self.driver
		link = "https://www.techinasia.com/jobs/search?query="+ jenKerja +"&country_name[]=Indonesia"
		driver.get(link)
		#array_hrefnya = []			 
		for i in range (1,201):
			try:
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				hrefnya = driver.find_element_by_xpath("//html/body/div[1]/div/div[4]/div/div[2]/div/div/div[2]/div/div[5]/article["+str(i)+"]/div/div[1]/div[2]/div[1]/span/b/a")		
				linknya = hrefnya.get_attribute("href")
				#array_hrefnya.append(linknya)
				try:
					quey = "INSERT INTO `linktia` (`id_array`, `link`) VALUES (%s, %s)"
					data = [i]
					cur.execute(quey,(data, linknya))
					conn.commit()
					print("data berhasil masuk")				
				except Exception:
					print("data gagal masuk")
			except Exception:
				print("sepertinya habis")
				break
		self.closeBrowser()

	def applyJob(self):
		driver = self.driver	

		try:
			query = "SELECT `link` FROM `linktia` WHERE `status` = %s"
			cur.execute(query, ("0"))
			result_link = [item[0] for item in cur.fetchall()]	
			panjang_list_link = len(result_link)
		except Exception:
			print("Gagal mengambil link")
			tiaJobs.closeBrowser()		

		for idarray in range(0,panjang_list_link):
			try:
				#try
				upstatus = "UPDATE `linktia` SET `status`= %s WHERE `link` = %s"
				cur.execute(upstatus,("1", result_link[idarray]))
				conn.commit()
				#except Exception:
					#break
				driver.get(result_link[idarray] + "/applied/")								
				uname_element = driver.find_element_by_xpath("//div/div[4]/div/div/div/div/div[2]/form/input")
				uname_element.clear()
				uname_element.send_keys(self.username)
				pass_element = driver.find_element_by_xpath("//div/div[4]/div/div/div/div/div[2]/form/div/input")
				pass_element.clear()
				pass_element.send_keys(self.password)
				pass_element.send_keys(Keys.RETURN)				
				print("Berhasil mendaftar pada array ke :" + str(idarray))
				time.sleep(5)
				
			except Exception:
				print("Gagal mendaftar pada array ke :" + str(idarray))
				print("Gagal mengambil link")
				
		
		


#--------------------------Database koneksi-------------------------
conn = db.connect('localhost','root','','tes_rest_api')
cur = conn.cursor()
#-------------------------------------------------------------------
email = 'Put Your Email Here'
passw = 'Put Your Password Here'
TJobs = tiaJobs(email,passw)
jenKerja = input("Masukkan jenis pekerjaan yang diinginkan : ")
TJobs.login()
TJobs.scrapJobs()
TJobs.applyJob()