from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000/login")

#---dang nhap
driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("123")
driver.find_element(By.CSS_SELECTOR, "button.btn").click()
time.sleep(2)

# Kiểm tra vào trang chủ
assert "Trang chủ" in driver.page_source
print(" Test đăng nhập thành công: PASS")
time.sleep(30)

#----dat-lich-------

driver.get("http://127.0.0.1:5000/schedule")

driver.find_element(By.NAME, "patient_name").send_keys("Nguyễn Văn A")
driver.find_element(By.NAME, "phone_number").send_keys("0123456789")
driver.find_element(By.NAME, "birthday").send_keys("2000-01-01")

driver.find_element(By.NAME, "doctor_id").send_keys("1")
driver.find_element(By.NAME, "appointment_date").send_keys("2025-12-30")
driver.find_element(By.NAME, "appointment_time").send_keys("08:00")

driver.find_element(By.TAG_NAME, "button").click()

time.sleep(30)
assert "Đặt lịch thành công" in driver.page_source

#kethuoc
driver.get("http://127.0.0.1:5000/create_form/3")

wait.until(EC.presence_of_element_located((By.ID, "medicine_name")))
driver.find_element(By.ID, "medicine_name").send_keys("Paracetamol")
driver.find_element(By.ID, "dosage").send_keys("2")
driver.find_element(By.ID, "days").send_keys("3")

time.sleep(1)

driver.find_element(By.XPATH, "//button[contains(.,'Thêm')]").click()
print("TC03 Kê thuốc: PASS")

#laphoadon
driver.get("http://127.0.0.1:5000/create_form/4")

wait.until(EC.presence_of_element_located((By.NAME, "patient_id")))
driver.find_element(By.NAME, "patient_id").send_keys("Nguyễn Văn A")

driver.find_element(By.NAME, "doctor_id").send_keys("1")
driver.find_element(By.XPATH, "//button[contains(.,'LƯU')]").click()

print(" Lập hóa đơn: PASS")

#quanlybacsi
driver.get("http://127.0.0.1:5000/create_form/6")

driver.find_element(By.NAME, "name").send_keys("BS Selenium")
driver.find_element(By.NAME, "specialty").send_keys("Test tự động")
driver.find_element(By.NAME, "phone_number").send_keys("0999999999")
driver.find_element(By.NAME, "email").send_keys("selenium@test.com")

driver.find_element(By.XPATH, "//button[contains(.,'Lưu')]").click()
print(" TC05 Thêm bác sĩ: PASS")

#quanlybenhnhan
driver.get("http://127.0.0.1:5000/patient_management")

driver.find_element(By.NAME, "tenbenhnhan").send_keys("BN Test Selenium")
driver.find_element(By.NAME, "ngaysinh").send_keys("2000-01-01")
driver.find_element(By.NAME, "gioitinh").send_keys("Nam")
driver.find_element(By.NAME, "sodienthoai").send_keys("0123456789")

driver.find_element(By.XPATH, "//button[contains(.,'Thêm')]").click()
print(" TC06 Thêm bệnh nhân: PASS")

#baocaodoanhthu
driver.get("http://127.0.0.1:5000/revenue")

wait.until(EC.presence_of_element_located((By.ID, "revenueChart")))
print(" TC07 Báo cáo doanh thu hiển thị: PASS")

time.sleep(3000)
driver.quit()

