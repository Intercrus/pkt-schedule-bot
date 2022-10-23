from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

from gspread import service_account

from re import search, match

from src.misc.full_names import groups, teachers, lessons

from environs import Env


CACHE = {}

previous_links = {}
previous_month = ""

env = Env()
env.read_env(".env")


def get_links(root: str = env.str("PATH_TO_ROOT_FOLDER")) -> dict:
    global previous_links, previous_month

    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "src/misc/service_account.json",
        "https://www.googleapis.com/auth/drive"
    )

    drive = GoogleDrive(gauth)

    months = drive.ListFile({
        "q": f"'{root}' in parents and trashed=false",
        "orderBy": "title"
    }).GetList()

    current_month = months[-1]['id']
    if current_month != previous_month:
        previous_links = {}
    previous_month = current_month

    links = drive.ListFile({
        "q": f"'{months[-1]['id']}' in parents and trashed=false"
    }).GetList()

    return {link["alternateLink"]: link["modifiedDate"] for link in links}


def get_data(link: str) -> list:
    gauth = service_account("src/misc/service_account.json")
    sheets = gauth.open_by_url(link)
    worksheet = sheets.get_worksheet(0)

    output_data = worksheet.get_all_values()

    # O(n)
    if "РАЗГОВОРЫ О ВАЖНОМ" in output_data[0]:
        output_data.pop(0)

    return output_data


def get_schedule_by_group(data: list, group: str) -> list:
    data.append(['', '', '', '', '', '', '', '', '', '', '', '', '', ''])

    rows_groups = [
        (data[0], (1, 8)),  # (row_groups, (from, to))
        (data[8], (9, 16)),
        (data[16], (17, 24)),
        (data[24], (25, 32))
    ]

    def find_group(year: int, rows_groups: list) -> tuple:
        row_groups = rows_groups[year - 1][0]
        for i in range(1, len(row_groups)):
            if search(fr"\b{group}\b", row_groups[i]):
                return year - 1, i

        row_groups = rows_groups[year][0]
        for j in range(1, len(row_groups)):
            if search(fr"\b{group}\b", row_groups[j]):
                return year, j

    schedule = []

    row_groups_index, group_index = find_group(int(group[0]), rows_groups)

    from_, to_ = rows_groups[row_groups_index][1]
    for row_index in range(from_, to_):
        subject = data[row_index][group_index]
        if subject.strip():
            schedule.append(subject)

    return schedule


def get_schedule_by_teacher(data: list, teacher: str) -> list:
    def find_group(row: int, cell: int) -> str:
        if 0 <= row <= 7:
            return data[0][cell]
        elif 8 <= row <= 15:
            return data[8][cell]
        elif 16 <= row <= 23:
            return data[16][cell]
        elif 24 <= row <= 31:
            return data[24][cell]

    schedule = []

    for row_index in range(len(data)):
        row = data[row_index]
        for cell_index in range(len(row)):
            cell = row[cell_index]

            if not cell:
                continue

            if match(r"^\d{2}.\d{2}.\d{4}", cell):
                break

            if search(fr"\b{teacher}\b", cell):
                group = find_group(row_index, cell_index)
                schedule.append((group, cell))

            if not any(row):
                break

    return sorted(schedule, key=lambda x: x[1][0])


def format_schedule(input_schedule: list, is_group: bool, date) -> list:
    weekdays_call_schedule = {
        "1": "08:30—09:50",
        "2": "10:00—11:20",
        "3": "11:50—13:10",
        "4": "13:30—14:50",
        "5": "15:10—16:30",
        "6": "16:40—18:00",
        "7": "18:10—19:30"
    }

    saturday_call_schedule = {
        "1": "08:30—09:40",
        "2": "09:50—11:00",
        "3": "11:10—12:20",
        "4": "12:30—13:40",
        "5": "13:50—15:00",
        "6": "15:10—16:20",
        "7": "16:30—17:40"
    }

    if date.capitalize() == "Суббота":
        call_schedule = saturday_call_schedule
    else:
        call_schedule = weekdays_call_schedule

    output_schedule, group = [], ""

    for subject in input_schedule:
        if not is_group:
            group, subject = subject[0], subject[1]

        lesson = subject[:subject.find("  ")]

        string_without_lesson = subject[len(lesson):]

        pattern_a = r"\d+[а]\/\d+[а]|\d+[а]\/\d+|\d+\/\d+[а]|\d\d[а]|\d[а]"

        pattern_other = r"\d+\/\d+|\d\d|\d|zoom|discord|ДО|экск"

        audience = search(fr"{pattern_a}|{pattern_other}",
                          string_without_lesson)
        if audience is None:
            audience = ""
        else:
            audience = audience.group(0)

        string_without_audience = string_without_lesson.replace(audience, "")

        teacher = string_without_audience.strip()

        full_name_teacher = teachers.get(teacher[:-3])
        if full_name_teacher:
            teacher = f"{teacher[:-3]} {full_name_teacher}"

        full_name_lesson = lessons.get(lesson[2:])
        if full_name_lesson:
            lesson = lesson[:2] + full_name_lesson

        try:
            if is_group:
                output_schedule.append(
                    f"""
    {call_schedule[subject[0]]}
    {lesson[:2]} <b>{lesson[2:]}</b>
        <i> {teacher}</i>
        <a href="https://koopteh.onego.ru/student/lessons/"> {audience}</a>"""
                )
            else:
                output_schedule.append(
                    f"""
    {call_schedule[subject[0]]}
    {lesson[:2]} <b>[{group}] — {lesson[2:]}</b>
        <i> {teacher}</i>
        <a href="https://koopteh.onego.ru/student/lessons/"> {audience}</a>"""
                )
        except KeyError:
            output_schedule.append(
                "\nБот не смог найти пару.\nСообщите, пожалуйста, @Intercrus об ошибке.\nПолное расписание лучше посмотреть на сайте техникума"
            )

    return output_schedule


async def update_schedule_cache():
    global CACHE, previous_links

    current_links = get_links()

    links = {}

    if len(current_links) != len(previous_links):
        for link, last_modified in current_links.items():
            if link not in previous_links:
                links[link] = last_modified
    else:
        for link, last_modified in current_links.items():
            if last_modified != previous_links[link]:
                links[link] = last_modified

    for link, last_modified in links.items():
        try:
            data = get_data(link)
        except TypeError:
            continue

        schedule_day = match(r'^\d{2}.\d{2}.\d{4}', data[0][0])
        schedule_day_name = data[0][0][schedule_day.end():].strip()

        CACHE[schedule_day.group()] = {
            "groups": {

            },
            "teachers": {

            }
        }

        for group in groups:
            schedule_by_group = get_schedule_by_group(data, group)
            format_schedule_by_group = format_schedule(schedule_by_group, True, schedule_day_name)
            CACHE[schedule_day.group()]["groups"][group] = format_schedule_by_group

        for teacher in teachers:
            schedule_by_teacher = get_schedule_by_teacher(data, teacher)
            format_schedule_by_teacher = format_schedule(schedule_by_teacher, False, schedule_day_name)
            CACHE[schedule_day.group()]["teachers"][teacher] = format_schedule_by_teacher

        previous_links[link] = last_modified

    print("Complete")
