from playwright.sync_api import Playwright, Page
from utility import get_current_day_date, get_current_day

def login(page: Page, url: str, user: str, password: str) -> None:
    page.goto(url)
    page.fill("#username", user)
    page.fill("#password", password)
    page.click("#loginbtn")


def popup_password_handler(page: Page) -> str:
    new_page = page.value
    student_passwd = new_page.locator(".student-password").inner_text()
    print(student_passwd)
    new_page.close()
    return student_passwd


def goto_course_attendance_page(page: Page, course: str) -> None:
    page.get_by_title(course).click()
    page.get_by_text("Lecture/Lectorial Attendance").click()
    page.get_by_text("Weeks").click()


def get_student_passwords(attendance: dict, page: Page, course: str) -> None:
    attendance_row = page.get_by_role("row", name=get_current_day_date())
    if not attendance_row.is_visible():
        print(f"{get_current_day_date()} not found for {course}")
        page.get_by_text("202501sg-Spring").click()
        return

    with page.expect_popup() as popup_page:
        attendance_row.locator("span").get_by_role("link").click()

    stu_passwd = popup_password_handler(popup_page)
    attendance[course] = stu_passwd


def run(playwright: Playwright, login_info: dict, attendance: dict, day: dict) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=400)
    page = browser.new_page(viewport={"width": 1280, "height": 840})

    login(page, login_info["url"], login_info["user"], login_info["password"])

    today = get_current_day()
    if today == "Mon":
        goto_course_attendance_page(page, day[today])
        get_student_passwords(attendance, page, day[today])

    else:
        for course in day[today]:

            goto_course_attendance_page(page, course)
            get_student_passwords(attendance, page, course)

            page.get_by_text("202501sg-Spring").click()
            # page.wait_for_timeout(1000)

    browser.close()
